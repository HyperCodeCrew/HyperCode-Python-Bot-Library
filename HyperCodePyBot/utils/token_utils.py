import os
import json

class token_utils:
    def load_token_from_string(token_string):
        return token_string.strip()
    
    def load_token_from_file(file_path):
        with open(file_path, 'r') as file:
            return file.read().strip()
    
    def load_token_from_environment(env_var):
        return os.getenv(env_var)
    
    def load_token_from_config(config_file, token_key):
        with open(config_file, 'r') as file:
            config = json.load(file)
            return config.get(token_key)
    
    def load_token_from_secret(secret_name):
        # Add your secret manager logic here
        pass