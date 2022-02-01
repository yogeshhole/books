import uvicorn
from loguru import logger

from src.config import ENVIRONMENT, PROJECT_PORT, LOG_FILE, LOG_LEVEL, LOG_SIZE_MB, LOG_RETENTION

logger.add(LOG_FILE, rotation=f"{LOG_SIZE_MB} MB", enqueue=True, retention=LOG_RETENTION, level=LOG_LEVEL.upper())

if __name__ == "__main__":
    logger.debug("starting uvicorn...")
    if ENVIRONMENT == 'local':
        uvicorn.run('src.main:app', host="0.0.0.0", port=PROJECT_PORT, reload=True, use_colors=True, workers=1)
    else:
        uvicorn.run('src.main:app', host="0.0.0.0", port=PROJECT_PORT, reload=True)
