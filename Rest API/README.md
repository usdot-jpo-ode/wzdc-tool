# WZDC Tool Rest API

This APi is intended to make data collected by the [Work Zone Data Collection Tool](https://github.com/TonyEnglish/Work_Zone_Data_Collection_Toolset) more easily accessible. This APi supports listing/querying and downloading of individual files for RSM {xml}, RSM {upper}, and WZDx {geojson} messages. To acquire an API key, contact [jfrye@neaeraconsulting.com](mailto://jfrye@neaeraconsulting.com). The data accessed by this API is also vailable for download from the WZDC tool website, [https://wzdctool.azurewebsites.net](https://wzdctool.azurewebsites.net). 

## API Endpoints and Documentation
[https://wzdc-published-rest-api.azurewebsites.net](https://wzdc-published-rest-api.azurewebsites.net)

## Example usage (powershell):
### Get Access Token (valid for 30 minutes)
`$response = Invoke-WebRequest 'https://wzdc-published-rest-api.azurewebsites.net/auth/token' -Method "POST" -Body @{"username"="user"; "password"="*api_key*"}; $response.Content`

Example response: `{"access_token":"*access_token_key*","token_type":"Bearer","token_expires":"2021-05-03 19:35:22.509"}`

### Make API Request
`$response = Invoke-WebRequest 'https://wzdc-published-rest-api.azurewebsites.net/wzdx/' -Headers @{"Authentication"="Bearer *access_token_key*"}; $response.Content`

### List files and Query
#### Query RSM {xml} files by center/radius
`https://wzdc-published-rest-api.azurewebsites.net/rsm-xml/?center=40.061336,-105.212715&distance=10`

#### Query RSM {xml} files by county
`https://wzdc-published-rest-api.azurewebsites.net/rsm-xml/?county=Larimer County`

#### Query RSM {xml} files by state
`https://wzdc-published-rest-api.azurewebsites.net/rsm-xml/?state=CO`
`https://wzdc-published-rest-api.azurewebsites.net/rsm-xml/?state=Colorado`

#### Query RSM {xml} files by zipcode
`https://wzdc-published-rest-api.azurewebsites.net/wzdx/?zip_code=80528`

### Download individual filed
#### Download individual WZDx file by name
`https://wzdc-published-rest-api.azurewebsites.net/rsm-xml/main-demo--i-25`


## Deployment
From root directory, after logging into the azure CLI (az login), run the following command:
`az webapp up --name wzdc-published-rest-api`
This will build and deploy the web app.

## Running locally: 

### Install requirements
`pip install -r requirements.txt`

### Configure environment variables
`$env:auth_contact_email = "*contact_email*";
$env:storage_connection_string = "*azure-storage-connnection-string*";
$env:sql_connection_string = "*sql-server-connnection-string*";
$env:stored_procedure_find_key = "exec find_key @key = '{0}'";
$env:stored_procedure_find_token = "exec find_token @token_hash = '{0}'"
$env:stored_procedure_create_token = "exec create_token @token_hash = '{0}', @type = '{1}', @expires = '{2}'"
$env:source_container_name = "*storage-container-name*;"`

### Start local server
`python -m uvicorn main:app --reload`

### Example usage (powershell):
`$response = Invoke-WebRequest 'http://127.0.0.1:8000/rsm-xml/?center=40.061336,-105.212715&distance=10' -Headers @{"Authentication"="Bearer *access_token_key*"}; $response.Content`

