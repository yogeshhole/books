from datetime import datetime
from typing import Optional

import aiohttp
from gcloud.aio.storage import Storage
from loguru import logger
from pytz import UTC


async def upload_to_storage_bucket(object_name: str, object_file: bytes, bucket: str, folder: str) -> Optional[dict]:
    """
    Upload files to cloud storage bucket
    folder format: path1/path2 (no beginning or ending "/" for folders)
    """
    try:
        async with aiohttp.ClientSession() as session:
            object_name = f'{folder}/{object_name}'
            # storage_client = Storage(service_file=GCP_STORAGE_CREDENTIALS, session=session)
            # storage will use env GOOGLE_APPLICATION_CREDENTIALS by default
            storage_client = Storage(session=session)
            data = await storage_client.upload(
                bucket=bucket,
                object_name=object_name,
                file_data=object_file
            )

            if data and 'bucket' in data and 'name' in data:
                # v is added to prevent caching on image change using the same name
                v = int(datetime.now(tz=UTC).timestamp())
                # this is the URL for public access if applicable
                # https://cloud.google.com/storage/docs/access-control/making-data-public
                data['publicUrl'] = f"https://storage.googleapis.com/{data.get('bucket')}/{data.get('name')}?v={v}"
            return data
    except Exception as err:
        logger.error(f'GCP storage update error: {err}')
        raise


async def delete_from_storage_bucket(object_name: str, bucket: str, folder: str):
    """
    delete files from cloud storage bucket
    folder format: path1/path2 (no beginning or ending "/" for folders)
    """
    try:
        async with aiohttp.ClientSession() as session:
            object_name = f'{folder}/{object_name}'
            # print(f'{bucket} {object_name}')
            # storage_client = Storage(service_file=GCP_STORAGE_CREDENTIALS, session=session)
            # storage will use env GOOGLE_APPLICATION_CREDENTIALS by default
            storage_client = Storage(session=session)
            await storage_client.delete(
                bucket=bucket,
                object_name=object_name
            )
    except Exception as err:
        logger.warning(f'GCP storage delete error: {err}')



"""  Storage response example:
{
  'kind': 'storage#object',
  'id': 'dev-calendar-public/icons/5e963fe736cf4b7839dfef4d_t.png/1586980797846521',
  'selfLink': 'https://www.googleapis.com/storage/v1/b/dev-calendar-public/o/icons%2F5e963fe736cf4b7839dfef4d_t.png',
  'mediaLink': 'https://www.googleapis.com/download/storage/v1/b/dev-calendar-public/o/icons%2F5e963fe736cf4b7839dfef4d_t.png?generation=1586980797846521&alt=media',
  'name': 'icons/5e963fe736cf4b7839dfef4d_t.png',
  'bucket': 'dev-calendar-public',
  'generation': '1586980797846521',
  'metageneration': '1',
  'contentType': 'image/png',
  'storageClass': 'STANDARD',
  'size': '14808',
  'md5Hash': 'dy/Ie1E8XEj/0YTTSp3VMQ==',
  'crc32c': '/CMvew==',
  'etag': 'CPmn4pWc6+gCEAE=',
  'timeCreated': '2020-04-15T19:59:57.846Z',
  'updated': '2020-04-15T19:59:57.846Z',
  'timeStorageClassUpdated': '2020-04-15T19:59:57.846Z'
}
"""
