from loguru import logger
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.errors import ConnectionFailure

from config import (MONGO_DB, MONGODB_URL, MONGO_MIN_CONNECTIONS_COUNT, MONGO_MAX_CONNECTIONS_COUNT,
                    MONGO_MAX_IDLE_TIME_IN_MINUTE,
                    PROJECT_NAME)
from constants.common import SECS_PER_MIN, MILLISECONDS_PER_SECOND

DB = AsyncIOMotorClient()


async def connect_to_mongo():
    try:
        DB.client = AsyncIOMotorClient(
            MONGODB_URL,
            minPoolSize=MONGO_MIN_CONNECTIONS_COUNT,
            maxPoolSize=MONGO_MAX_CONNECTIONS_COUNT,
            MaxIdleTimeMS=MONGO_MAX_IDLE_TIME_IN_MINUTE * SECS_PER_MIN * MILLISECONDS_PER_SECOND,
            appname=PROJECT_NAME
        )
        logger.info("connected to Mongo.")
    except ConnectionFailure as err:
        logger.error(f'Database connection failure: {err}')
    except Exception as err:
        logger.error(f'Database connection error: {err}')


async def connect_to_mongo_using_loop(io_loop):
    try:
        DB.client = AsyncIOMotorClient(
            MONGODB_URL,
            minPoolSize=MONGO_MIN_CONNECTIONS_COUNT,
            maxPoolSize=MONGO_MAX_CONNECTIONS_COUNT,
            MaxIdleTimeMS=MONGO_MAX_IDLE_TIME_IN_MINUTE * SECS_PER_MIN * MILLISECONDS_PER_SECOND,
            appname=PROJECT_NAME,
            io_loop=io_loop
        )
        logger.info("connected to Mongo. ")
    except ConnectionFailure as err:
        logger.error(f'Database connection failure: {err}')
    except Exception as err:
        logger.error(f'Database connection error: {err}')


async def close_mongo_connection():
    DB.client.close()
    logger.info("Mongo connection closed.")


async def get_database() -> AsyncIOMotorClient:
    return DB.client[MONGO_DB]


async def get_database_by_name(db_name: str) -> AsyncIOMotorClient:
    return DB.client[db_name]


async def drop_collection_by_name(db: AsyncIOMotorClient, collection_name: str):
    result = await db[collection_name].drop()
    logger.info(f' dropped collection {collection_name}: {result}')
    return
