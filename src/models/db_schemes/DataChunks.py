from pydantic import BaseModel,Field,validator
from typing import Optional
from bson.objectid import ObjectId

class DataChunks(BaseModel):
    id:Optional[ObjectId]=Field(None,alias="_id")  # id generated by mongodb for each chunk and filed
    chunk_text:str =Field(...,min_length=1) # at least 1 char
    chunk_metadata:dict  # of type dictionary 
    chunk_order:int=Field(...,gr=0) #value must be gr =>greater than 0 
    chunk_project_id:ObjectId
 
    # to avoid error of miss understnding in type of the _id here => _id:Optional[ObjectId]  so allow if there is error in type
    class Config:
        arbitrary_types_allowed = True
    
    @classmethod
    def get_indexes(cls):
        return[
            {
                "key": [("chunk_project_id",1)], # 1 means asc order -1 means desc
                "name":"chunk_project_id_index_1",  #the name of collection it can be any name
                "unique":False # project_id must be unique
                
            }
        ]

class RetrievedDocument(BaseModel):
    text:str
    score:float
      