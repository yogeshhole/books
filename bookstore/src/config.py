from environs import Env

from utils.print_common import print_env_info

env = Env()
env.read_env()

PROJECT_NAME = env.str("PROJECT_NAME", None)
PROJECT_PORT = env.int("PROJECT_PORT", 8102)
ENVIRONMENT = env.str("ENVIRONMENT", "local")
DEBUG = env.bool("DEBUG", False)
MONGO_DB = env.str("MONGO_DB", "booksDB")


# LOGGING / SENTRY
HOME = env.str("HOME", None)
LOG_FILE = HOME + '/' + env.str("LOG_FILE", 'books.log')
LOG_LEVEL = env.str("LOG_LEVEL", "info")
LOG_SIZE_MB = env.int("LOG_SIZE_MB", 10)  # max log size in MB, will rotate
LOG_RETENTION = env.int("LOG_RETENTION", 3)  # number of file to keep

if ENVIRONMENT == "local" and DEBUG:
    print_env_info(PROJECT_NAME, PROJECT_PORT, ENVIRONMENT, DEBUG, LOG_LEVEL, MONGO_DB)

# COLLECTIONS
COLLECTION_USERS = "users"
