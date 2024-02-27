CONNECTION = {
    'CLIENT_ID': '',
    'CLIENT_SECRET': '',
    'TENANT_ID': '',
    'USER_UPN': '',
    'DOWNLOAD_DIRECTORY': '',
    'DOWNLOAD_FILE_NAME': '',
    'DOWNLOAD_FILE_PATH': '',
    'RENAME_DIRECTORY': '',
    'API_VERSION': '',
    'BASE_PATH': '',
    'FOLDER_NAME': '',
    'START_YEAR': '',
    'START_MONTH': '',
    'LOG_FILE_PATH': '',
    'FUNCTION_NAME': '',
}

RENAME = {
    'TIME_RETENTION': '',
    'SERIES_CODE': '',
    'FILES_DIRECTORY': '',
    'RENAME_DIRECTORY': '',
}

PUSH_CONNECTION = {
    'HOSTNAME': '',
    'DOMAIN': '',
    'DESTINATION_DIRECTORY': '',
    'YEAR': '',
    'MONTH': '',
    'DAY': '',
    'WORM': '',
    'SUBFOLDER': '',
    'SOURCE_DIRECTORY': '',
    'SERVICE_ACCOUNT': {        
        'PRD': {
            'username': '',
            'AppID': '',
            'Safe': '',
            'Object': '',
            'passphrase': '',
            'crt': '',
            'key': '',
        },
        'UAT': {
            'username': '',
            'AppID': '',
            'Safe': '',
            'Object': '',
            'passphrase': '',
            'crt': '',
            'key': '',
        }
    }
}


PULL_CONNECTION = {
    'HOSTNAME': '',
    'DOMAIN': '',
    'DESTINATION_DIRECTORY': '',
    'SUBFOLDER': '',
    'SOURCE_DIRECTORY': '',
    'RETRY_LIMIT': '', 
    'SLEEP_DURATION': '',
    'YEAR': '',
    'MONTH': '',
    'DAY': '',
    'SERVICE_ACCOUNT': {
        'PRD': {
            'username': '',
            'AppID': '',
            'Safe': '',
            'Object': '',
            'passphrase': '',
            'crt': '',
            'key': '',
        },
        'UAT': {
            'username': '',
            'AppID': '',
            'Safe': '',
            'Object': '',
            'passphrase': '',
            'crt': '',
            'key': '',
        }
    }
}