import json
from typing import Union
from urllib.parse import urlencode

from aiohttp import ClientConnectorError
from calendar_core.config import SERVICE_CREDENTIALS, SERVICE_EVENTS
from calendar_core.utils.requests import request, req
from loguru import logger

from src.config import SERVICE_APPS, APPLE_AUTHORIZATION_URL
from src.models.calendars import ConnectedCalendarCredentialsPatch


async def get_creds_by_primary_calendar_id(creds_req: dict) -> Union[dict, None]:
    """
    GET Calendar OAuth2 credentials and calendarIds from credentials service by calendar list subscription id.
    """
    fn = get_creds_by_primary_calendar_id.__name__
    headers = {"Content-Type": "application/json"}
    logger.info(f"Request params to credentials service is {creds_req}")
    try:
        return await request(
            method="GET",
            url=f"{SERVICE_CREDENTIALS}/internal/c/v1/calendar/credentials?{urlencode(creds_req)}",
            headers=headers,
        )
    except ClientConnectorError as error:
        logger.error(f"In {fn} Exception while connecting to calendar creds service due to {error}")
    except Exception as error:
        logger.error(f"In {fn} Exception while fetching calendar list data due to {error}")
    return None


async def unassign_calendar_from_creds_service_for_user(user_id):
    """
    Unassigned user from calendar list in credentials service
    """
    headers = {"Content-Type": "application/json"}
    fn = unassign_calendar_from_creds_service_for_user.__name__
    try:
        await req(method="delete", url=SERVICE_CREDENTIALS + f"/internal/c/v1/calendar/user/{user_id}", headers=headers)
    except Exception as error:
        logger.error(f"Exception while un-assigning user for calendar from creds service due to {error}")
        raise SystemError(f"Service connection {fn} error: {error}")


async def delete_calendar_from_creds_service(calendar_delete_payload: dict):
    """
    Delete primary calendar from credentials service
    """
    fn = delete_calendar_from_creds_service.__name__
    headers = {"Content-Type": "application/json"}
    try:
        await req(
            method="delete",
            url=f"{SERVICE_CREDENTIALS}/internal/c/v1/calendar",
            data=json.dumps(calendar_delete_payload),
            headers=headers
        )
    except Exception as error:
        logger.error(f"Exception while deleting calendar from creds service due to {error}")
        raise SystemError(f"Service connection {fn} error: {error}")


async def delete_calendar_events_from_calendar_ids(calendar_ids):
    fn = delete_calendar_events_from_calendar_ids.__name__

    headers = {"Content-Type": "application/json"}
    try:
        await req(method="delete", url=f"{SERVICE_EVENTS}/internal/e/v1/events/delete",
                  data=json.dumps(calendar_ids), headers=headers)
    except Exception as error:
        logger.error(f"Exception while deleting calendar from creds service due to {error}")
        raise SystemError(f"Service connection {fn} error: {error}")
    return


async def update_calendar_credentials(payload: ConnectedCalendarCredentialsPatch):
    fn = update_calendar_credentials.__name__
    headers = {"Content-Type": "application/json"}

    try:
        _, _ = await request(method='PATCH', url=f"{SERVICE_CREDENTIALS}/internal/c/v1/calendar/credentials",
                             data=json.dumps(payload.dict()), headers=headers)
    except Exception as error:
        logger.error(f"{fn} Exception while connecting to calendar creds service due to {repr(error)}")
        raise SystemError(f"{error}")
    return


async def get_apple_auth_credentials(payload: dict):
    fn = get_apple_auth_credentials.__name__
    headers = {"Content-Type": "application/x-www-form-urlencoded"}

    try:
        data, _ = await request(method='POST', url=APPLE_AUTHORIZATION_URL,
                                data=json.dumps(payload), headers=headers)
        return data
    except Exception as error:
        logger.error(f"{fn} Exception while connecting to calendar creds service due to {repr(error)}")
        raise SystemError(f"{error}")


async def create_default_timeslot(user_id, calendar_id, default_calendar_id, default_calendar_provider,
                                  workspace_user_id, workspace_id, scheduling_page_id, timezone):
    fn = create_default_timeslot.__name__
    payload = {
        "notificationTimers": [],
        "buffer": 0,
        "dailyLimit": 0,
        "minScheduleNotice": 0,
        "attendeeLimit": 0,
        "timezone": timezone,
        "color": "#8F589D",
        "isActive": True,
        "overlappingSlots": True,
        "title": "15 or 30 Minute Meeting",
        "description": "",
        "durations": [
            30,
            15
        ],
        "defaultCalendarId": default_calendar_id,
        "defaultCalendarProvider": default_calendar_provider,
        "calendarId": calendar_id,
        "availabilities": [
            {
                "date": None,
                "day": 1,
                "startTime": 32400,
                "endTime": 61200,
                "start": None,
                "end": None
            },
            {
                "date": None,
                "day": 2,
                "startTime": 32400,
                "endTime": 61200,
                "start": None,
                "end": None
            },
            {
                "date": None,
                "day": 3,
                "startTime": 32400,
                "endTime": 61200,
                "start": None,
                "end": None
            },
            {
                "date": None,
                "day": 4,
                "startTime": 32400,
                "endTime": 61200,
                "start": None,
                "end": None
            },
            {
                "date": None,
                "day": 5,
                "startTime": 32400,
                "endTime": 61200,
                "start": None,
                "end": None
            }
        ],
        "type": 1,
        "rangeType": 2,
        "defaultLocationType": 0,
        "defaultCustomLocation": "",
        "users": [
            {
                "workspaceUserId": workspace_user_id,
                "isReauthRequired": False,
                "active": True
            }
        ],
        "distribution": 0,
        "locations": [
            {
                "phoneNumber": "",
                "meetingLink": "Zoom Call",
                "meetingPin": "",
                "instructions": "",
                "type": 1
            }
        ],
        "slug": "15-30-meetings",
        "schedulingPageId": scheduling_page_id,
        "startTime": 0,
        "endTime": 0,
        "teamId": None,
        "workspaceId": workspace_id
    }

    headers = {"Content-Type": "application/json"}

    try:
        _, _ = await request(method='POST', url=f"{SERVICE_APPS}/internal/a/v1/timeslots?user_id={user_id}",
                             data=json.dumps(payload), headers=headers)
    except Exception as error:
        logger.error(f"{fn} Exception while connecting to calendar app service due to {repr(error)}")
        raise SystemError(f"{error}")
    return
