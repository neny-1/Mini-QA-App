from pydantic import BaseModel
from typing import Optional

# define the request schema for the process route
class ProcessRequest(BaseModel):
    file_id:str = None 
    chunk_size:Optional[int]=100  
    overlap_size:Optional[int]=20
    do_reset:Optional[int]=0  # reset the collection or not
