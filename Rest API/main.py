import os
import pymssql
import sys
import hashlib
import uuid
import math
import re

from starlette.responses import Response

from loguru import logger

from starlette.routing import Match

from datetime import datetime, timedelta

from models import Token

from fastapi import FastAPI, Header, HTTPException, status, Request, Query, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from azure.storage.blob import BlobServiceClient


logger.remove()
logger.add(sys.stdout, colorize=True,
           format="<green>{time:HH:mm:ss}</green> | {level} | <level>{message}</level>")


ACCESS_TOKEN_EXPIRE_MINUTES = 30
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token/")

epoch = datetime.utcfromtimestamp(0)

auth_email = os.environ['auth_contact_email']

app = FastAPI(
    title="Work Zone Data Collection Tool Rest API",
    description='This API hosts work zone data collected by the WZDC ' +
    '(work zone data collection) tool. This data includes RSM messages, both in xml and uper (binary) formats. This API ' +
    f'requires an APi key in the header. Contact <a href="mailto: {auth_email}">{auth_email}</a> or visit <a href="https://github.com/TonyEnglish/WZDC-Rest-API">https://github.com/TonyEnglish/WZDC-Rest-API</a> for more information on how to acquire and use an API key.',
    docs_url="/",
)


@app.middleware("http")
async def log_middle(request: Request, call_next):
    logger.debug(f"{request.method} {request.url}")
    logger.info(f"{request.client}")
    routes = request.app.router.routes
    logger.debug("Params:")
    for route in routes:
        match, scope = route.matches(request)
        if match == Match.FULL:
            for name, value in scope["path_params"].items():
                logger.debug(f"\t{name}: {value}")

    logger.debug("Headers:")
    for name, value in request.headers.items():
        logger.debug(f"\t{name}: {value}")

    response = await call_next(request)
    return response


@app.middleware("http")
async def log_request(request, call_next):
    logger.info(f'{request.method} {request.url}')
    response = await call_next(request)
    logger.info(f'Status code: {response.status_code}')
    body = b""
    async for chunk in response.body_iterator:
        body += chunk
    # do something with body ...
    return Response(
        content=body,
        status_code=response.status_code,
        headers=dict(response.headers),
        media_type=response.media_type
    )


def parse_sql_connection_str(conn_str):
    server = None
    database = None
    username = None
    password = None
    params = conn_str.split(';')
    for param in params:
        if param.startswith('Server='):
            server = param.replace('Server=', '').replace(
                'tcp:', '').split(',')[0]
        if param.startswith('Database='):
            database = param.replace('Database=', '')
        if param.startswith('Uid='):
            username = param.replace('Uid=', '')
        if param.startswith('Pwd='):
            password = param.replace('Pwd=', '')

    if not server or not database or not username or not password:
        raise RuntimeError("Invalid connection string")

    return server, username, password, database


storage_conn_str = os.environ['storage_connection_string']
sql_conn_str = os.environ['sql_connection_string']
blob_service_client = BlobServiceClient.from_connection_string(
    storage_conn_str)


# conn = pymssql.connect(*parse_sql_connection_str(sql_conn_str))
# cursor = conn.cursor()

storedProcFindKey = os.environ['stored_procedure_find_key']
# exec create_token @token_hash = '{0}', @type = '{1}', @expires = '{2}'
storedProcCreateToken = os.environ['stored_procedure_create_token']
storedProcFindToken = os.environ['stored_procedure_find_token']

authorization_key_header = 'auth_key'

container_name = os.environ['source_container_name']

file_types_dict = {
    'rsm-xml': {
        'subdir': 'rsm-xml',
        'list_endpoint': 'rsm-xml',
        'name_prefix': 'rsm-xml',
        'file_type': 'xml'
    },
    'rsm-uper': {
        'subdir': 'rsm-uper',
        'list_endpoint': 'rsm-uper',
        'name_prefix': 'rsm-uper',
        'file_type': 'uper'
    },
    'wzdx': {
        'subdir': 'wzdx',
        'list_endpoint': 'wzdx',
        'name_prefix': 'wzdx',
        'file_type': 'geojson'
    }
}


def getCurrentTime():
    return datetime.utcnow()


def parseDateTime(time_str):
    try:
        return datetime.strptime(time_str, '%Y-%m-%d %H:%M:%S.%f')
    except:
        return None


def getExperitationTime():
    return (datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)).strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]


def get_current_token(access_token: str = Depends(oauth2_scheme)):
    key_hash = str(hashlib.sha256(access_token.encode()).hexdigest())
    print(key_hash)
    row = find_token(key_hash)
    time_expires = None
    if row:
        time_expires = find_token(key_hash)[0]
    if not time_expires:
        logger.error(f"Invalid Access Token: Token not found")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token not found. Use /auth/token to get a token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    elif time_expires >= getCurrentTime():
        return True
    else:
        logger.error(f"Invalid Access Token: Token has expired")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired",
            headers={"WWW-Authenticate": "Bearer"},
        )


def get_current_active_token(token_valid: bool = Depends(get_current_token)):
    return token_valid


def find_token(token_hash):

    try:
        conn = pymssql.connect(*parse_sql_connection_str(sql_conn_str))
        cursor = conn.cursor()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unable to connect to SQL server",
        )
    
    cursor.execute(storedProcFindToken.format(token_hash))

    row = cursor.fetchone()

    cursor.close()
    conn.close()

    if row:
        return row
    else:
        return None


@app.post("/auth/token/")
async def get_token(form_data: OAuth2PasswordRequestForm = Depends()):
    logger.info(f"Request Username: {form_data.username}")
    valid = authenticate_key(form_data.password)
    if not valid:
        logger.error(f"Unauthorized Request: Invalid Password Key")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Password Key",
            headers={"WWW-Authenticate": "Bearer"},
        )

    token = Token(
        access_token=str(uuid.uuid4()),
        token_type="Bearer",
        token_expires=getExperitationTime()
    )

    token_hash = str(hashlib.sha256(token.access_token.encode()).hexdigest())

    query = storedProcCreateToken.format(
        token_hash, token.token_type, token.token_expires)

    try:
        conn = pymssql.connect(*parse_sql_connection_str(sql_conn_str))
        cursor = conn.cursor()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unable to connect to SQL server",
        )

    cursor.execute(query)
    conn.commit()

    cursor.close()
    conn.close()

    return token


@app.get("/wzdx", tags=["wzdx-list"])
def get_wzdx_files_list(center: str = Query('', title='Center', description='Center of query location, in the format "lat,long"',
                                            regex='^(-?\\d+(\\.\\d+)?),\\s*(-?\\d+(\\.\\d+)?)$'),
                        distance: float = Query(
                            0, title='Distance', description='Maximum distance (in km) from center location'),
                        county: str = Query(
                            None, title='County', description='County'),
                        state: str = Query(
                            None, title='State', description='State'),
                        zip_code: str = Query(
                            None, title='Zip Code', description='Zip code'),
                        token_valid: bool = Depends(get_current_token)
                        ):
    file_type = 'wzdx'

    check_dist = False
    ref_loc = parseCoordinates(center)
    if not distance == 0 and ref_loc:
        ref_dist = distance
        check_dist = True

    location_params = []

    for val in [{'name': 'county_names', 'value': county},
                {'name': 'state_names', 'value': state},
                {'name': 'zip_code', 'value': zip_code}]:
        if val['value']:
            location_params.append(val)

    if check_dist:
        return getFilesByDistance(file_type, container_name, ref_loc, ref_dist)
    elif county or state or zip_code:
        return getFilesByMetadata(file_type, container_name, location_params)
    else:
        return getFilesByType(file_type, container_name)


@app.get("/wzdx/{file_name}", tags=["wzdx-file"])
def get_wzdx_file(file_name: str, token_valid: bool = Depends(get_current_token)):
    file_type = 'wzdx'

    return getFilesListByName(file_type, file_name, container_name)


@app.get("/rsm-xml", tags=["xml-list"])
def get_rsm_files_list_location_filter(center: str = Query('', title='Center', description='Center of query location, in the format: lat,long',
                                                           regex='^(-?\\d+(\\.\\d+)?),\\s*(-?\\d+(\\.\\d+)?)$'),
                                       distance: float = Query(
                                           0, title='Distance', description='Maximum distance (in km) from center location'),
                                       county: str = Query(
                                           None, title='County', description='County'),
                                       state: str = Query(
                                           None, title='State', description='State'),
                                       zip_code: str = Query(
                                           None, title='Zip Code', description='Zip code'),
                                       token_valid: bool = Depends(
                                           get_current_token)
                                       ):
    file_type = 'rsm-xml'

    check_dist = False
    ref_loc = parseCoordinates(center)
    if not distance == 0 and ref_loc:
        ref_dist = distance
        check_dist = True

    location_params = []

    for val in [{'name': 'county_names', 'value': county},
                {'name': 'state_names', 'value': state},
                {'name': 'zip_code', 'value': zip_code}]:
        if val['value']:
            location_params.append(val)

    if check_dist:
        return getFilesByDistance(file_type, container_name, ref_loc, ref_dist)
    elif county or state or zip_code:
        return getFilesByMetadata(file_type, container_name, location_params)
    else:
        return getFilesByType(file_type, container_name)


@app.get("/rsm-xml/{file_name}", tags=["xml-file"])
def get_rsm_file(file_name: str, token_valid: bool = Depends(get_current_token)):
    file_type = 'rsm-xml'

    return getFilesListByName(file_type, file_name, container_name)


@app.get("/rsm-uper", tags=["uper-list"])
def get_rsm_uper_files_list(center: str = Query('', title='Center', description='Center of query location, in the format: lat,long',
                                                regex='^(-?\\d+(\\.\\d+)?),\\s*(-?\\d+(\\.\\d+)?)$'),
                            distance: float = Query(
                                0, title='Distance', description='Maximum distance (in km) from center location'),
                            county: str = Query(
                                None, title='County', description='County'),
                            state: str = Query(
                                None, title='State', description='State'),
                            zip_code: str = Query(
                                None, title='Zip Code', description='Zip code'),
                            token_valid: bool = Depends(get_current_token)
                            ):
    file_type = 'rsm-uper'

    check_dist = False
    ref_loc = parseCoordinates(center)
    if not distance == 0 and ref_loc:
        ref_dist = distance
        check_dist = True

    location_params = []

    for val in [{'name': 'county_names', 'value': county},
                {'name': 'state_names', 'value': state},
                {'name': 'zip_code', 'value': zip_code}]:
        if val['value']:
            location_params.append(val)

    if check_dist:
        return getFilesByDistance(file_type, container_name, ref_loc, ref_dist)
    elif county or state or zip_code:
        return getFilesByMetadata(file_type, container_name, location_params)
    else:
        return getFilesByType(file_type, container_name)


@app.get("/rsm-uper/{rsm_name}", tags=["uper-file"])
def get_rsm_uper_file(rsm_name: str, token_valid: bool = Depends(get_current_token)):
    file_type = 'rsm-uper'

    return getFilesListByName(file_type, rsm_name, container_name)


def authenticate_key(key):
    try:
        key_hash = str(hashlib.sha256(key.encode()).hexdigest())
        print(key_hash)
        return find_key(key_hash)
    except:
        return False


def get_correct_response(auth_key):
    if not auth_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="No authentication key was specified. If you have a key, please add password: **authentication_key** to your " +
            f"request body. If you do not have a key, email {auth_email} to get a key. For more info on how to use a key, please visit https://github.com/TonyEnglish/WZDC-Rest-API",
        )
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication key",
        )


def find_key(key_hash):

    try:
        conn = pymssql.connect(*parse_sql_connection_str(sql_conn_str))
        cursor = conn.cursor()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unable to connect to SQL server",
        )

    
    cursor.execute(storedProcFindKey.format(key_hash))

    row = cursor.fetchone()

    cursor.close()
    conn.close()

    if row:
        return True
    else:
        return False


def validNumOrNone(values):
    value1, value2 = values
    if re.match('^-?[0-9]e\\+[0-9]{2}$', str(value1)) or re.match('^-?([0-9]*[.])?[0-9]+$', str(value1)):
        value1 = float(value1)
    else:
        return None

    if re.match('^-?[0-9]e\\+[0-9]{2}$', str(value2)) or re.match('^-?([0-9]*[.])?[0-9]+$', str(value2)):
        value2 = float(value2)
    else:
        return None

    return value1, value2


def getDist(origin, destination):
    origin = validNumOrNone(origin)
    destination = validNumOrNone(destination)

    if not origin or not destination:
        return None

    lat1, lon1 = origin  # lat/lon of origin
    lat2, lon2 = destination  # lat/lon of dest

    radius = 6371.0*1000  # meters

    dlat = math.radians(lat2-lat1)  # in radians
    dlon = math.radians(lon2-lon1)

    a = math.sin(dlat/2) * math.sin(dlat/2) + math.cos(math.radians(lat1)) \
        * math.cos(math.radians(lat2)) * math.sin(dlon/2) * math.sin(dlon/2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    d = radius * c

    return d


def getWZId(file_type, name):
    type_values = file_types_dict[file_type]

    begin_str = '{:s}--'.format(type_values['name_prefix'])
    end_str_pattern = '--[0-9]*-of-[0-9]*?\.{:s}'.format(
        type_values['file_type'])
    # end_str_len = '--1-of-[0-9].{:s}'.format(type_values['file_type'])
    alt_end_str = '.{:s}'.format(type_values['file_type'])

    name = name.split('/')[-1]
    if name.startswith(begin_str):
        name = name[len(begin_str):]
    end_match_obj = re.search(end_str_pattern, name)
    if end_match_obj != None:
        name = name[:-len(end_match_obj[0])]
    elif name.endswith(alt_end_str):
        name = name[:-len(alt_end_str)]
    return name


def parseCoordinates(center_str):
    if type(center_str) != str:
        return None

    ref_loc = None
    center_split = center_str.split(',')
    if len(center_split) == 2:
        ref_loc = validNumOrNone(
            (center_split[0].strip(), center_split[1].strip()))
    return ref_loc


def getBlobOrNoneByDistance(file_type, blob, ref_loc, ref_dist):
    begin_loc = (blob.metadata.get('beginning_lat'),
                 blob.metadata.get('beginning_lon'))
    end_loc = (blob.metadata.get('ending_lat'),
               blob.metadata.get('ending_lon'))

    if begin_loc[0] and begin_loc[1] and end_loc[0] and end_loc[1]:
        center_loc = ((float(begin_loc[0])+float(end_loc[0]))/2,
                      (float(begin_loc[1])+float(end_loc[1]))/2)
        blob_dist = getDist(ref_loc, center_loc) / 1000  # Convert meters to km
        if blob_dist and blob_dist <= ref_dist:
            return {'name': getWZId(file_type,
                                    blob.name), 'id': blob.metadata.get('group_id', 'unknown')}
        else:
            pass
    return None


def getFilesListByName(file_type, rsm_name, container_name):
    type_values = file_types_dict[file_type]
    name_beginning = '{0}/{1}--{2}'.format(
        type_values['subdir'], type_values['name_prefix'], rsm_name)

    # For RSM files, multiple files can exist for a single work zone. Thus, these files have --i-of-N at the end of the name
    if file_type == 'rsm-xml' or file_type == 'rsm-uper':
        name_pattern = '{0}--1-of-[0-9]*\.{1}'.format(
            name_beginning, type_values['file_type'])
        # initialize this value, might be updated later
        initial_blob_name = '{0}--1-of-1.{1}'.format(
            name_beginning, type_values['file_type'])
        blob_list = blob_service_client.get_container_client(
            container_name).list_blobs()
        for blob in blob_list:
            if re.match(name_pattern, blob.name):
                initial_blob_name = blob.name

    else:
        initial_blob_name = '{0}.{1}'.format(
            name_beginning, type_values['file_type'])

    blob_client = blob_service_client.get_blob_client(
        container=container_name, blob=initial_blob_name)

    files = []

    try:
        group_id = blob_client.get_blob_properties().metadata.get('group_id', 'unknown')
    except:
        raise HTTPException(
            status_code=404,
            detail=f"Specified {file_type} file not found. Try using the {type_values['list_endpoint']} endpoint to return a list of current files",
        )

    if group_id != 'unknown':
        container_client = blob_service_client.get_container_client(
            container_name)
        blob_list = container_client.list_blobs(
            name_starts_with=name_beginning, include='metadata')
        for blob in blob_list:
            if blob.metadata.get('group_id') == group_id:
                if file_type == 'rsm-uper':
                    files.append({'source_name': blob.name, 'size': blob.size, 'data': str(blob_service_client.get_blob_client(
                        container=container_name, blob=blob.name).download_blob().readall())})
                else:
                    files.append({'source_name': blob.name, 'size': blob.size, 'data': blob_service_client.get_blob_client(
                        container=container_name, blob=blob.name).download_blob().readall().decode('utf-8')})

    return {'num_files': len(files), 'id': group_id, 'files': files}


def getFilesByDistance(file_type, container_name, ref_loc, ref_dist):
    type_values = file_types_dict[file_type]

    container_client = blob_service_client.get_container_client(container_name)
    blob_list = container_client.list_blobs(
        name_starts_with=type_values['subdir'] + '/', include='metadata')

    blob_names = []
    for blob in blob_list:
        if blob.metadata:
            entry = getBlobOrNoneByDistance(
                file_type, blob, ref_loc, ref_dist)
            if entry and entry not in blob_names:
                blob_names.append(entry)
        else:
            pass
    return {'query_parameters': {'distance': f'{ref_dist:.0f} km', 'center': [ref_loc[0], ref_loc[1]]}, 'data': blob_names}


def getFilesByType(file_type, container_name):
    type_values = file_types_dict[file_type]

    container_client = blob_service_client.get_container_client(container_name)
    blob_list = container_client.list_blobs(
        name_starts_with=type_values['subdir'] + '/', include='metadata')

    blob_names = []
    for blob in blob_list:
        if blob.metadata:
            entry = {'name': getWZId(file_type, blob.name),
                     'id': blob.metadata.get('group_id', 'unknown')}
            if entry not in blob_names:
                blob_names.append(entry)

    return {'query_parameters': None, 'data': blob_names}


def getFilesByMetadata(file_type, container_name, query_params):
    print(query_params)
    type_values = file_types_dict[file_type]

    container_client = blob_service_client.get_container_client(container_name)
    blob_list = container_client.list_blobs(
        name_starts_with=type_values['subdir'] + '/', include='metadata')

    blob_names = []
    for blob in blob_list:
        if blob.metadata:
            valid = True

            for param in query_params:
                values = [x.lower()
                          for x in blob.metadata.get(param['name'], '').split(',')]
                if param['value'] and param['value'].lower() not in values:
                    valid = False

            if valid:
                entry = {'name': getWZId(file_type, blob.name),
                         'id': blob.metadata.get('group_id', 'unknown')}
                if entry not in blob_names:
                    blob_names.append(entry)

    formatted_query_params = []
    for param in query_params:
        formatted_query_params.append({param["name"]: param["value"]})

    return {'query_parameters': formatted_query_params, 'data': blob_names}
