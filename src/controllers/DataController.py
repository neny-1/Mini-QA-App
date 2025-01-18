from .BaseController import BaseController
from .ProjectController import ProjectController
from fastapi import UploadFile
from models import ResponseSignal
import os
import re
class DataController(BaseController):

    def __init__(self) -> None:

        super().__init__()

        self.size_scale = 104875  # 1MB = 104875 bytes

    # validate the uploaded file
    def validate_uploaded_file(self, file: UploadFile)->tuple:
        
        if file.content_type not in self.app_settings.FILE_ALLOWED_TYPE:
            return False,ResponseSignal.FILE_TYPE_NOT_SUPPORTED
        
        if file.size > self.app_settings.FILE_MAX_SIZE*self.size_scale:
            return False,ResponseSignal.FILE_SIZE_NOT_ALLWOEDT
        return True ,ResponseSignal.FILL_Success_upload
    
    # generate random string with file name 
    def generate_unique_filename(self,orig_file_name:str,project_id:str) -> tuple:
        randome_key: str = self.generate_random_string()
        project_dir: str = ProjectController().get_project_path(project_id=project_id)

        cleaned_file_name: str= self.get_clean_file_name(orig_file_name=orig_file_name)

        new_file_path: str=os.path.join(
            project_dir,
            randome_key+"_"+cleaned_file_name
        )

        # check if file is exist to create new file name
        while os.path.exists(new_file_path):
            randome_key = self.generate_random_string()
            new_file_path=os.path.join(
            project_dir,
            randome_key+"_"+cleaned_file_name
        )

        return new_file_path,randome_key+"_"+cleaned_file_name
    
    # remove any special characters, except underscores using regular expression
    def get_clean_file_name(self, orig_file_name: str) -> str:

        # remove any special characters, except underscores using regular expression
        cleaned_file_name: str = re.sub(r'[^\w.]', '', orig_file_name.strip())

        # replace spaces with underscore
        cleaned_file_name = cleaned_file_name.replace(" ", "_")

        return cleaned_file_name
