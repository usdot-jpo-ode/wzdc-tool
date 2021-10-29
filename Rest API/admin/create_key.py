import os
import json
import uuid
import pyodbc
import hashlib
from datetime import datetime

sql_conn_str = os.environ['sql_connection_string']

cnxn = pyodbc.connect(sql_conn_str)
cursor = cnxn.cursor()

storedProcCreate = 'exec create_key @key = \'{0}\''


def generate_key():
    key = str(uuid.uuid4())
    key_hash = str(hashlib.sha256(key.encode()).hexdigest())
    return key, key_hash


key = str(uuid.uuid4())
key_hash = str(hashlib.sha256(key.encode()).hexdigest())


def create_key():
    key, key_hash = generate_key()

    try:
        cursor.execute(storedProcCreate.format(key_hash))
        cnxn.commit()
    except Exception as e:
        print(e)
        return None

    return key, key_hash


key, key_hash = create_key()
key_obj = {
    'api_key': key,
    'api_url': 'https://wzdc-published-rest-api.azurewebsites.net',
    'instructions': 'Save this key, it can never be recovered. Add this api key to the header of all requests, as auth_key'
}
key_file_name = 'wzdc_api_key_{0}.json'.format(
    datetime.now().strftime("%Y%m%d-%H%M%S"))
with open('wzdc_api_key_{0}.json'.format(datetime.now().strftime("%Y%m%d-%H%M%S")), 'w+') as f:
    f.write(json.dumps(key_obj, indent=2))
print(f'Key file created: {key_file_name}')
