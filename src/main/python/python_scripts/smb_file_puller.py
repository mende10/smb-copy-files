import os
import smbclient
from python_scripts.constants import PULL_CONNECTION
from python_scripts.global_functions import GlobalFunctions

class SMBFilePuller:
    def __init__(self, pull_connection):
        self.hostname = pull_connection['HOSTNAME']
        self.domain = pull_connection['DOMAIN']
        self.username = self.credentials.decrypt_credentials()['username']
        self.password = self.credentials.decrypt_credentials()['password']
        self.source_directory = pull_connection['SOURCE_DIRECTORY']
        self.destination_directory = pull_connection['DESTINATION_DIRECTORY']
        self.organization_username = f"{self.domain}\\{self.username}"
        self.global_functions = GlobalFunctions()

        # Print the pre-configured parameters
        self.log("SMB File Puller Configuration:")
        self.log(f"  Hostname: {self.hostname}")
        self.log(f"  Domain: {self.domain}")
        self.log(f"  Username: {self.username}")
        self.log(f"  Source Directory: {self.source_directory}")
        self.log(f"  Destination Directory: {self.destination_directory}")
        self.log(f"  Organization Username: {self.organization_username}")

    def log(self, message, level="INFO"):
        self.global_functions.print_log(message, level)

    def copy_files(self):
        smbclient.ClientConfig(username=self.username, password=self.password)

        # Define the source SMB share path
        source_share = f'\\\\{self.hostname}\\{self.source_directory}'

        try:
            # List files in the source directory
            files = smbclient.scandir(source_share)
            for entry in files:
                if entry.is_file():
                    source_file_path = os.path.join(source_share, entry.name)
                    destination_file_path = os.path.join(self.destination_directory, entry.name)
                    self.log(f"Attempting to copy {source_file_path} to {destination_file_path}")

                    try:
                        with smbclient.open_file(source_file_path, mode='rb') as source_file:
                            with open(destination_file_path, 'wb') as dest_file:
                                dest_file.write(source_file.read())
                        self.log(f"Copied {entry.name} to {destination_file_path}")
                    except Exception as e:
                        self.log(f"Failed to copy {entry.name}. Error: {e}", level="ERROR")
        except Exception as e:
            self.log(f"Error listing directory: {e}", level="ERROR")
            exit(1)
        finally:
            if 'files' in locals():
                files.close()

        smbclient.reset_connection_cache()

def main():
    smb_puller = SMBFilePuller(PULL_CONNECTION)
    smb_puller.log("Starting SMB file transfer...")
    smb_puller.copy_files()
    smb_puller.log("SMB file transfer completed.")

if __name__ == "__main__":
    main()
