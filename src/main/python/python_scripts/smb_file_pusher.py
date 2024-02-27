import os
import smbclient
from python_scripts.constants import PUSH_CONNECTION
from python_scripts.constants import CONNECTION
from python_scripts.global_functions import GlobalFunctions

class SMBFilePusher:
    def __init__(self):
        environment = os.getenv('SYSENV', 'UAT')
        self.global_functions = GlobalFunctions()
        self.push_connection = PUSH_CONNECTION
        self.connection = CONNECTION
        self.hostname = self.push_connection['HOSTNAME']
        self.domain = self.push_connection['DOMAIN']
        self.username = self.push_connection['SERVICE_ACCOUNT'][environment]['username']
        self.password = self.global_functions.retrieve_password_from_vault()
        
        self.source_directory = self.push_connection['SOURCE_DIRECTORY']
        self.organization_username = f"{self.domain}\\{self.username}"
        
        self.year = self.global_functions.call_function_by_name(self.global_functions, self.connection['FUNCTION_NAME'])        

        self.subfolder = self.push_connection['SUBFOLDER']
        self.destination_directory = self.push_connection['DESTINATION_DIRECTORY']
        env_str = "_UAT" if environment == "UAT" and self.push_connection['WORM'] else ""
        self.destination_directory = self.destination_directory.format(env_str)

    def log(self, message, level="INFO"):
        self.global_functions.print_log(message, level)

    def copy_files(self):
        
        smbclient.ClientConfig(username=self.username, password=self.password)

        for file_name in os.listdir(self.source_directory):
            # Skip the filelist.txt file
            if file_name == 'filelist.txt':
                continue

            source_file_path = os.path.join(self.source_directory, file_name)
            destination_file_path = f'\\\\{self.hostname}\\{self.destination_directory}\\{file_name}'

            # Print the pre-configured parameters
            self.log("SMB File Pusher Configuration:")
            self.log(f"Hostname: {self.hostname}")
            self.log(f"Domain: {self.domain}")
            self.log(f"Username: {self.username}")
            self.log(f"Destination Directory: {destination_file_path}")
            self.log(f"Source Directory: {self.source_directory}")
            self.log(f"Organization Username: {self.organization_username}")
            self.log(f"Attempting to copy {source_file_path} to {destination_file_path}")

            if os.path.isfile(source_file_path):
                try:
                    with open(source_file_path, 'rb') as source_file:
                        with smbclient.open_file(destination_file_path, mode='wb') as dest_file:
                            dest_file.write(source_file.read())
                    self.log(f"Copied {file_name} to {destination_file_path}")
                except Exception as e:
                    self.log(f"Failed to copy {file_name}. Error: {e}", level="ERROR")
                    exit(1)

        smbclient.reset_connection_cache()

def main():
    smb_pusher = SMBFilePusher()
    smb_pusher.log("Starting SMB file transfer...")
    smb_pusher.copy_files()
    smb_pusher.log("SMB file transfer completed.")

if __name__ == "__main__":
    main()