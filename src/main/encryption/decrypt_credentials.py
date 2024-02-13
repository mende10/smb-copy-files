from cryptography.fernet import Fernet
import json
import os
import os
from python_scripts.global_functions import GlobalFunctions

class CredentialsDecryptor:
    def __init__(self, filename="encrypted_credentials.bin"):
        self.global_functions = GlobalFunctions()
        self.filename = os.path.join(os.path.dirname(__file__), filename)
        self.key = self.global_functions.retrieve_key_from_vault()

    def load_key(self):
        with open(self.key_filename, "rb") as key_file:
            return key_file.read()

    def decrypt_credentials(self):
        cipher_suite = Fernet(self.key)
        with open(self.filename, "rb") as file:
            encrypted_credentials = file.read()
        decrypted_credentials = cipher_suite.decrypt(encrypted_credentials)
        return json.loads(decrypted_credentials.decode())
