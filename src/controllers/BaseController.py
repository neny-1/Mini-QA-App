from helper.config import get_settings,Settings
import os
import random
import string

class BaseController:
    def __init__(self) -> None:  
        self.app_settings: Settings = get_settings()

        self.base_dir: str = os.path.dirname(os.path.dirname(__file__)) 
        self.files_dir: str = os.path.join(
            self.base_dir,
            "assets/files"
        )
        
        self.database_dir: str = os.path.join(
            self.base_dir,
            "assets/database"
        )

    def generate_random_string(self, length: int=12) -> str:
        return ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))
    
    def get_database_path(self,database_name:str) -> str:
        database_path: str=os.path.join(self.database_dir,database_name)

        if not os.path.exists(database_path):
            os.makedirs(database_path)
            
        return database_path