import hashlib
import json
import os
import time
import smbclient
import datetime
from python_scripts.constants import PULL_CONNECTION
from python_scripts.global_functions import GlobalFunctions

class SMBFilePuller:
    def __init__(self, pull_connection):
        current_date = datetime.datetime.now()
        self.global_functions = GlobalFunctions()
        
        if pull_connection['YEAR']:
            self.year = "//" + str(current_date.year)
        else:
            self.year = ""
        
        if pull_connection['MONTH']:
            self.month = "//" + current_date.month
        else:
            self.month = ""

        if pull_connection['DAY']:
            self.day = "//" + str(current_date.day)
        else:
            self.day = ""

        environment = os.getenv('SYSENV', 'UAT')
        self.hostname = pull_connection['HOSTNAME']
        self.domain = pull_connection['DOMAIN']
        self.username = pull_connection['SERVICE_ACCOUNT'][environment]['username']
        self.password = self.global_functions.retrieve_password_from_vault()
        self.source_directory = pull_connection['SOURCE_DIRECTORY']
        self.destination_directory = pull_connection['DESTINATION_DIRECTORY']
        self.organization_username = f"{self.domain}\\{self.username}"
        self.hashes_file = os.path.join(self.destination_directory, 'file_hashes.json')

        # Print the pre-configured parameters
        self.log("SMB File Puller Configuration:")
        self.log(f"Hostname: {self.hostname}")
        self.log(f"Domain: {self.domain}")
        self.log(f"Username: {self.username}")
        self.log(f"Source Directory: {self.source_directory}")
        self.log(f"Destination Directory: {self.destination_directory}")
        self.log(f"Organization Username: {self.organization_username}")

    def log(self, message, level="INFO"):
        self.global_functions.print_log(message, level)

    def copy_files(self, retry_limit=3, sleep_duration=5):

        smbclient.ClientConfig(username=self.username, password=self.password)
        source_share = f'\\\\{self.hostname}\\{self.source_directory}{self.year}{self.month}{self.day}'
        
        # Load the existing hashes
        if os.path.exists(self.hashes_file):
            with open(self.hashes_file, 'r') as f:
                existing_hashes = json.load(f)
        else:
            existing_hashes = {}

        try:
            files = smbclient.scandir(source_share)
            for entry in files:
                if entry.is_file():
                    retries = 0
                    while retries < retry_limit:
                        source_file_path = os.path.join(source_share, entry.name)
                        destination_file_path = os.path.join(self.destination_directory, entry.name)
                        file_hash = self.calculate_file_hash(source_file_path)

                        if entry.name not in existing_hashes or existing_hashes[entry.name] != file_hash:
                            self.log(f"Attempting to copy {source_file_path} to {destination_file_path} (Attempt {retries + 1}/{retry_limit})")
                            try:
                                with smbclient.open_file(source_file_path, mode='rb') as source_file:
                                    with open(destination_file_path, 'wb') as dest_file:
                                        dest_file.write(source_file.read())
                                existing_hashes[entry.name] = file_hash
                                self.log(f"Copied {entry.name} to {destination_file_path}")
                                break  # Exit the retry loop on success
                            except Exception as e:
                                self.log(f"Failed to copy {entry.name}. Error: {e}", level="ERROR")
                                time.sleep(sleep_duration)  # Sleep before the next retry
                                retries += 1
                        else:
                            break  # No need to retry if file doesn't need to be copied
                    else:
                        self.log(f"Reached max retries for {entry.name}. Moving on to next file.", level="WARNING")
        except Exception as e:
            self.log(f"Error listing directory: {e}", level="ERROR")
        finally:
            if 'files' in locals():
                files.close()

        # Update the hashes file
        with open(self.hashes_file, 'w') as f:
            json.dump(existing_hashes, f)

        smbclient.reset_connection_cache()

    def calculate_file_hash(self, file_path):
        hash_md5 = hashlib.md5()
        with smbclient.open_file(file_path, mode='rb') as file:
            for chunk in iter(lambda: file.read(4096), b""):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()

def main():
    smb_puller = SMBFilePuller(PULL_CONNECTION)
    smb_puller.log("Starting SMB file transfer...")
    smb_puller.copy_files(PULL_CONNECTION.RETRY_LIMIT, PULL_CONNECTION.SLEEP_DURATION)
    smb_puller.log("SMB file transfer completed.")

if __name__ == "__main__":
    main()