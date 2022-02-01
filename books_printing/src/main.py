from db.mongodb import connect_to_mongo, close_mongo_connection, get_database
from fastapi import FastAPI, Depends
from loguru import logger
from starlette.middleware.cors import CORSMiddleware

from src.api.v1.cart import carts_router
from src.api.v1.orders import orders_router
from src.config import PROJECT_NAME
from src.db.mongodb_utils import create_indexes

app = FastAPI(title=PROJECT_NAME)

# Set all CORS enabled origins
origins = ['*']

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,  # support for cookie credentials
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup():
    await connect_to_mongo()
    await create_indexes()


@app.on_event("shutdown")
async def shutdown():
    await close_mongo_connection()
    await logger.complete()


@app.get("/health-check")
def health_check():
    return {"status": "OK"}


# ROUTERS
app.include_router(orders_router, prefix='/orders/', tags=['orders'],
                   dependencies=[Depends(get_database)])

app.include_router(carts_router, prefix='/carts/', tags=['cart'],
                   dependencies=[Depends(get_database)])
