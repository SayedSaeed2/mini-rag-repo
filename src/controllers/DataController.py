import os
from .ProjectController import ProjectController
from .BaseController import BaseController
from fastapi import UploadFile
from models import ResponseSignal
import re
from helpers.config import get_settings # Added import

class DataController(BaseController): 
    
    def __init__(self):
        super().__init__()
        self.size_scale = 1024 * 1024  # 1 MB in bytes
        self.app_settings = get_settings() # Added initialization
    
    def validate_uploaded_file(self, file: UploadFile):
        # Validate file extension
        if file.content_type not in self.app_settings.FILE_ALLOWED_TYPES:
            return False, ResponseSignal.FILE_TYPE_NOT_ALLOWED.value
        
        # Validate file size
        if file.size > self.app_settings.FILE_MAX_SIZE_MB * self.size_scale:
            return False, ResponseSignal.FILE_SIZE_EXCEEDED.value

        return True, ResponseSignal.FILE_VALIDATION_SUCCESS.value
    
    def generate_unique_filename(self, original_filename: str, project_id: str):
        random_key = self.generate_random_string()  # Generate a random string of length 12
        project_path = ProjectController().get_project_path(project_id=project_id)  # Get the project path

        cleaned_filename = self.get_cleaned_filename(original_filename)  # Clean the original filename

        new_file_path = os.path.join(project_path, f"{random_key}_{cleaned_filename}")  # Create the new file path
        
        while os.path.exists(new_file_path):  # Check if the file already exists
            random_key = self.generate_random_string()  # Generate a new random string
            new_file_path = os.path.join(project_path, f"{random_key}_{cleaned_filename}")  # Update the file path
        return new_file_path  # Return the unique file path

    def generate_unique_filepath(self, original_filename: str, project_id: str):
            random_key = self.generate_random_string()  # Generate a random string of length 12
            project_path = ProjectController().get_project_path(project_id=project_id)  # Get the project path
    
            cleaned_filename = self.get_cleaned_filename(original_filename)  # Clean the original filename
    
            new_file_path = os.path.join(project_path, f"{random_key}_{cleaned_filename}")  # Create the new file path
            
            while os.path.exists(new_file_path):  # Check if the file already exists
                random_key = self.generate_random_string()  # Generate a new random string
                new_file_path = os.path.join(project_path, f"{random_key}_{cleaned_filename}")  # Update the file path
                
            return new_file_path, random_key + "_" + cleaned_filename  # Return the unique file path
    
    
    def get_cleaned_filename(self, original_filename: str):
        cleaned_filename = re.sub(r'[^\w\.]', '_', original_filename.strip())
        cleaned_filename = cleaned_filename.replace(' ', '_')  # Replace spaces with underscores
        return cleaned_filename