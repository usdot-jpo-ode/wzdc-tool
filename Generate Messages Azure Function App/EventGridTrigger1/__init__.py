import os
import json
import logging
import tempfile
import sys
from urllib.request import urlopen
import azure.functions as func
from azure.storage.blob import BlobServiceClient

# sys.path.append(os.path.abspath(os.path.join(os.path.dirname('buildmsgs_and_export.py'))))
logging.getLogger().setLevel(logging.DEBUG)


def main(event: func.EventGridEvent):
    logger = logging.getLogger("logger_name")
    logger.disabled = True

    # Must be here to re-initialize variables every time
    from . import buildmsgs_and_export
    result = json.dumps({
        'id': event.id,
        'data': event.get_json(),
        'topic': event.topic,
        'subject': event.subject,
        'event_type': event.event_type,
    })
    logging.info('Python EventGrid trigger processed an event: %s', result)

    fileName = event.subject.split('/')[-1]
    updateImage = False
    if '--update-image' in fileName:
        updateImage = True

    wzID = fileName.replace('path-data', '').replace('.csv',
                                                     '').replace('--update-image', '')

    csv_path = tempfile.gettempdir() + '/path-data.csv'
    config_path = tempfile.gettempdir() + '/config.json'

    try:

        blob_service_client = BlobServiceClient.from_connection_string(
            os.environ['neaeraiotstorage_storage'], logger=logger)
        container_name = 'workzoneuploads'
        blob_name = event.subject.split('/')[-1]
        logging.debug('CSV: container: ' + container_name +
                      ', blob: ' + blob_name)
        blob_client = blob_service_client.get_blob_client(
            container=container_name, blob=blob_name)
        with open(csv_path, 'wb') as download_file:
            download_file.write(blob_client.download_blob().readall())

        blob_name = 'config' + wzID + '.json'
        container_name = 'publishedconfigfiles'
        logging.debug('Config: container: ' +
                      container_name + ', blob: ' + blob_name)
        blob_client = blob_service_client.get_blob_client(
            container=container_name, blob=blob_name)
        with open(config_path, 'wb') as download_file:
            download_file.write(blob_client.download_blob().readall())

        logging.debug('Wrote local files')

        buildmsgs_and_export.build_messages_and_export(
            wzID, csv_path, config_path, updateImage)

    except Exception as e:
        raise RuntimeError(json.dumps(
            {"data_file": fileName, "wz_id": wzID, "error_message": str(e)}))
