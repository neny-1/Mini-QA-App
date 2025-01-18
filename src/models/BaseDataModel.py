from helper.config import get_settings,Settings

# generic class for all data models
class BaseDataModel:
    def __init__(self,db_client:object):
        self.db_client = db_client
        self.app_settings = get_settings()