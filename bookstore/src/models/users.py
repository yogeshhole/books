import regex
from enum import IntEnum
from pydantic import constr
from typing import Optional, List

from calendar_core.model.auth import GoogleAuthCode, AuthToken
###################################################################
# Base
###################################################################
from calendar_core.model.base_model import TimestampModelMixin, DBModelMixin, ObjectIdStr
from calendar_core.model.calendars import normalize_email
from calendar_core.model.constants import PlanType
from calendar_core.model.constants import Provider, Day, DashboardViews, UserAvailability
from calendar_core.model.credentials import LoginCredentials, LoginCredentialsDB
from src.models.constants import UserAccountSource

from pydantic import BaseModel, validator, EmailStr

FIRST_LAST_NAME_REGEX = r'^[\p{L}\p{Mn}]+(?:[\p{Nd}\p{L}\p{Mn}\p{S}\p{Pd}\p{Zs}\'_.,]+)*$'


class DefaultCalendar(BaseModel):
    providerCalendarId: str = ""
    provider: int = Provider.CALENDAR.value


class UserPendingVerification(BaseModel):
    token: str
    expiry: int


class UserPendingPasswordReset(BaseModel):
    token: str
    expiry: int


class WorkingHour(BaseModel):
    day: int
    startTime: int
    endTime: int

    @validator('day')
    def valid_day_only(cls, value):
        choices = list(map(int, Day))
        if value and value not in choices:
            raise ValueError(f'day must be one of {choices}')
        return value


class WorkingHours(BaseModel):
    workingHours: List[WorkingHour] = []

    # TODO: enable when decision comes on WHs
    # @validator('workingHours')
    # def check_if_working_hour_exists(cls, working_hours):
    #     if not working_hours:
    #         day_starts_at = datetime(1970, 1, 1, 9, 0, 0)  # 9AM
    #         day_ends_at = datetime(1970, 1, 1, 17, 0, 0)  # 5PM
    #         day_starts_timestamp = int((day_starts_at - datetime(1970, 1, 1)).total_seconds())
    #         day_ends_timestamp = int((day_ends_at - datetime(1970, 1, 1)).total_seconds())
    #
    #         return [WorkingHour(day=day.value, startTime=day_starts_timestamp, endTime=day_ends_timestamp)
    #                 for day in Day if Day.MONDAY <= day <= Day.FRIDAY]
    #     return working_hours


class UserPreferences(WorkingHours):
    # mandatory fields
    timezone: str

    # optional fields
    autoTimezone: bool = True
    timeFormat: str = ""
    onBoarding: Optional[bool] = False

    # should be included in V2?
    startOfWeek: int = Day.SUNDAY.value
    dashboardView: int = DashboardViews.DAY.value
    language: str = ""
    enableTranscription: bool = False
    availability: int = UserAvailability.PUBLIC
    migratedReauth: Optional[bool] = True
    showDeclinedEvents: Optional[bool] = True
    onboardingV3: bool = False

    @validator('startOfWeek')
    def check_start_of_week(cls, v):
        if v == Day.SUNDAY or v == Day.MONDAY or v == Day.SATURDAY:  # following Google
            return v
        raise ValueError(f'Wrong Start of Week {v}')


class JoinReason(IntEnum):
    CALENDAR = 1
    SCHEDULING = 2
    TEAMS = 3


class UserBase(BaseModel):
    email: EmailStr
    firstName: str = ""
    lastName: str = ""
    description: str = ""
    title: str = ""
    company: str = ""
    profilePicture: str = ""
    phoneNumber: str = ""
    isVerified: bool = False
    googleAccountId: Optional[str]
    appleRegisteredClaimId: Optional[str]
    pendingVerifications: Optional[List[UserPendingVerification]]
    pendingPasswordReset: Optional[List[UserPendingPasswordReset]]
    preferences: UserPreferences
    highestWorkspacePlan: int = PlanType.WS_BASIC.value
    joinReason: Optional[int]

    # validators
    _normalize_email_id = validator('email', allow_reuse=True)(normalize_email)

    @validator('joinReason')
    def valid_join_reasons_only(cls, reason):
        if reason is None:
            return None
        if reason not in list(map(int, JoinReason)):
            raise ValueError(f'Join reason must be one of {list(map(lambda r: r.name, JoinReason))}')
        return reason


class UserPreferencesInUpdate(BaseModel):
    timezone: str = None
    timeFormat: str = None
    autoTimezone: bool = None
    onBoarding: bool = None
    onboardingV3: bool = None

    # should be included in V2?
    startOfWeek: int = None
    dashboardView: int = None
    language: str = None
    enableTranscription: bool = None
    availability: int = None
    migratedReauth: bool = None
    showDeclinedEvents: bool = None
    workingHours: List[WorkingHour] = None

    @validator('startOfWeek')
    def check_start_of_week(cls, v):
        if v is None or v == Day.SUNDAY or v == Day.MONDAY or v == Day.SATURDAY:  # following Google
            return v
        raise ValueError(f'Wrong Start of Week {v}')


###################################################################
# DB
###################################################################

class UserDB(TimestampModelMixin, UserBase):
    # Provider Credentials
    loginCredentials: Optional[LoginCredentialsDB]
    deleted: Optional[int]
    sso: Optional[int]
    source: Optional[int] = UserAccountSource.WEBAPP.value
    isAdmin: Optional[bool]
    affiliateId: Optional[ObjectIdStr]
    affiliate: Optional[str]


###################################################################
# In
###################################################################

class User(DBModelMixin, UserDB):
    id: str


class UserInCreate(UserBase):
    loginCredentials: Optional[LoginCredentials]
    password: Optional[str] = ""
    sso: Optional[int]
    source: Optional[int] = UserAccountSource.WEBAPP.value
    createNativeCalendar: Optional[bool] = False
    affiliate: Optional[str]

    class Config:
        anystr_strip_whitespace = True


class UserOutForPartnerStack(BaseModel):
    email: EmailStr
    firstName: Optional[str] = ""
    lastName: Optional[str] = ""
    created: Optional[bool] = False


class UserAuthOutBase(AuthToken, UserOutForPartnerStack):
    pass


class UserAuthOut(BaseModel):
    data: UserAuthOutBase


class UserRegisterOut(BaseModel):
    data: UserOutForPartnerStack


class UserInUpdate(BaseModel):
    firstName: constr(strip_whitespace=True, min_length=1, max_length=70) = None
    lastName: constr(strip_whitespace=True, min_length=0, max_length=70) = None
    description: Optional[str] = None
    title: Optional[str] = None
    company: Optional[str] = None
    profilePicture: Optional[str] = None
    phoneNumber: Optional[str] = None
    preferences: UserPreferencesInUpdate = None
    joinReason: Optional[int] = None

    class Config:
        extra = "ignore"
        anystr_strip_whitespace = True

    @validator('firstName')
    def first_name_exists_apply_regex(cls, v):
        result = v
        if v:
            validate_result = regex.match(FIRST_LAST_NAME_REGEX, v)
            if not validate_result:
                raise ValueError("Special characters are not allowed")
        return result

    @validator('lastName')
    def last_name_exists_apply_regex(cls, v):
        result = v
        if v:
            validate_result = regex.match(FIRST_LAST_NAME_REGEX, v)
            if not validate_result:
                raise ValueError("Special characters are not allowed")
        return result


class UserVerifyInUpdate(BaseModel):
    updated: Optional[int]
    isVerified: bool


class UserGoogleAuthIn(GoogleAuthCode, WorkingHours):
    timezone: str
    autoTimezone: bool = True
    createNativeCalendar: Optional[bool] = False
    affiliate: Optional[str]


class UserPasswordInUpdate(BaseModel):
    resetToken: Optional[str]
    password: str

    class Config:
        anystr_strip_whitespace = True


###################################################################
# Out
###################################################################


class UserOutBase(BaseModel):
    email: str = ""
    firstName: str = ""
    lastName: str = ""
    description: str = ""
    title: str = ""
    company: str = ""
    profilePicture: str = ""
    phoneNumber: str = ""
    isVerified: bool = False
    preferences: UserPreferences
    highestWorkspacePlan: int = PlanType.WS_BASIC.value
    sso: Optional[int]
    source: Optional[int] = UserAccountSource.WEBAPP.value
    joinReason: Optional[int]


class UserWithAnalyticsId(UserOutBase):
    analyticsId: str


class UserAnalyticsOut(BaseModel):
    data: UserWithAnalyticsId


class UserOut(BaseModel):
    data: UserOutBase


###################################################################
# Profile picture
###################################################################


class UserProfilePictureOutBase(BaseModel):
    profilePicture: str = None
    profilePictureFilename: str = None
    size: int = None
    contentType: str = None


class UserProfilePictureOut(BaseModel):
    data: UserProfilePictureOutBase
