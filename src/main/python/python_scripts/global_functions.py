
import datetime
import logging
import os
import json
import ssl
import urllib3
from python_scripts.constants import PUSH_CONNECTION

class GlobalFunctions:
    
    def print_log(self, message, level="INFO"):
        # Set up the logging format to include the timestamp
        # Note: It's best to call this once at the start of your script or program
        logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', 
                            datefmt='%Y-%m-%d %H:%M:%S', 
                            level=logging.INFO)

        # Get the appropriate logging function based on the level
        log_func = getattr(logging, level.lower())

        # Log the message
        log_func(message)
    
    def read_last_processed_date(self, log_file_path):
        try:
            with open(log_file_path, 'r') as file:
                last_date = file.readline().strip()
                return datetime.datetime.strptime(last_date, "%Y-%m").date() if last_date else None
        except FileNotFoundError:
            return None
    
    def write_last_processed_date(self, log_file_path, date):
        os.makedirs(os.path.dirname(log_file_path), exist_ok=True)

        with open(log_file_path, 'w') as file:
            file.write(date.strftime("%Y-%m"))

    def get_previous_month_year(self):
        today = datetime.date.today()
        first_of_current_month = datetime.date(today.year, today.month, 1)
        last_month = first_of_current_month - datetime.timedelta(days=1)
        return f'\\{last_month.year}\\'
    
    def get_cyberark_credentials(self, ssl_context, Object=None):
        # Determine the environment from the SYSENV variable, defaulting to UAT
        SYSENV = os.getenv('SYSENV', 'UAT')
        
        AppID = PUSH_CONNECTION['SERVICE_ACCOUNT'][SYSENV]['AppID']        
        Safe = PUSH_CONNECTION['SERVICE_ACCOUNT'][SYSENV]['Safe'] 

        web_service_url = f"https://ccp.corp.pjc.com/AIMWebService/api/Accounts?AppID={AppID}&Safe={Safe}&Object={Object}"
        http = urllib3.PoolManager(ssl_context=ssl_context)  
        response = http.request('GET', web_service_url)
        if response.status == 200:
            return json.loads(response.data.decode('utf-8'))['Content']
        else:
            raise Exception(f"Failed to retrieve credentials: HTTP {response.status}")
    
    def retrieve_password_from_vault(self):
        # Determine the environment from the SYSENV variable, defaulting to UAT
        SYSENV = os.getenv('SYSENV', 'UAT')

        # SSL context setup
        ssl_context = ssl.create_default_context()
        # Configuration crt and key files
        ssl_context.load_verify_locations(cafile=PUSH_CONNECTION['SERVICE_ACCOUNT'][SYSENV]['crt'])
        ssl_context.load_cert_chain(certfile=PUSH_CONNECTION['SERVICE_ACCOUNT'][SYSENV]['crt'],
                                        keyfile=PUSH_CONNECTION['SERVICE_ACCOUNT'][SYSENV]['key'],
                                        password=PUSH_CONNECTION['SERVICE_ACCOUNT'][SYSENV]['passphrase'])
        ssl_context.check_hostname = False
        ssl_context.verify_mode = ssl.CERT_NONE
            
        return self.get_cyberark_credentials(ssl_context, Object=PUSH_CONNECTION['SERVICE_ACCOUNT'][SYSENV]['Object'] )       

    
    def call_function_by_name(self, class_instance, function_name):
        if not function_name:
            return "\\"
        # Get the method from the class instance
        method = getattr(class_instance, function_name, None)
        
        # Check if the method exists and is callable
        if callable(method):
            return method()
        else:
            return "Function not found"
