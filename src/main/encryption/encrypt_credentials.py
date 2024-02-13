from cryptography.fernet import Fernet
import json

class CredentialsEncryptor:
    def __init__(self, credentials, filename="encrypted_credentials.bin"):
        self.credentials = credentials
        self.filename = filename
        self.key = Fernet.generate_key()
        self.cipher_suite = Fernet(self.key)

    def encrypt_credentials(self):
        encrypted_credentials = self.cipher_suite.encrypt(json.dumps(self.credentials).encode())
        with open(self.filename, "wb") as file:
            file.write(encrypted_credentials)
        return self.key

    @staticmethod
    def save_key_to_file(key, key_filename="encryption.key"):
        with open(key_filename, "wb") as key_file:
            key_file.write(key)

