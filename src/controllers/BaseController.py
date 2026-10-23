from helpers.config import get_settings, Settings
import os
import random, string

class BaseController: 
    
    def __init__(self):
        self.settings = get_settings()
        self.base_dir = os.path.dirname(os.path.dirname((__file__)))  # Get the directory of the current file
        self.file_dir = os.path.join(self.base_dir, "assets/files")  # Define the file directory path
        
        
    def generate_random_string(self, length: int=12):
        """Generate a random string of fixed length."""
        return ''.join(random.choices(string.ascii_letters + string.digits, k=length))