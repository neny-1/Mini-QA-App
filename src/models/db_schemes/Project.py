from pydantic import BaseModel,Field,validator
from typing import Optional
from bson.objectid import ObjectId

# validate the project_id
class Project (BaseModel):
    id:Optional[ObjectId]=Field(None,alias="_id")  
    project_id:str = Field(...,min_length=1) 

    
    @validator("project_id")
    def validate_project_id(cls,value):
        if not value.isalnum(): # check if the project_id is alphanumeric or not 
            raise ValueError("Project_id must be alphanumeric")
        return value
    
    # to avoid error of miss understnding in type of the _id here => _id:Optional[ObjectId]  so allow if there is error in type
    class Config:
        arbitrary_types_allowed = True
    
    @classmethod
    def get_indexes(cls):
        return[
            {
                "key": [("project_id",1)], 
                "name":"project_id_index_1",  
                "unique":True 
                
            }
        ]