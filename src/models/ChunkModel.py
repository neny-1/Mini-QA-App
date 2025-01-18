from .BaseDataModel import BaseDataModel
from .db_schemes import DataChunks
from .enums.DataBaseEnum import DataBaseEnum
from bson.objectid import ObjectId   
from pymongo import InsertOne 


class ChunkModel(BaseDataModel):

    def __init__(self, db_client:object):
        super().__init__(db_client)
        self.collection=self.db_client[DataBaseEnum.COLLECTION_CHUNK_NAME.value]

    # hnadle the async call to create an instance of the class
    @classmethod
    async def create_instance(cls,db_client:object):  
        instance = cls(db_client)  
        await instance.init_collection()
        return instance

    # create function for indexing 
    async def init_collection(self):
        all_collections = await self.db_client.list_collection_names()
        if DataBaseEnum.COLLECTION_CHUNK_NAME.value not in all_collections:  
            self.collection = self.db_client[DataBaseEnum.COLLECTION_CHUNK_NAME.value] 
            indexes = DataChunks.get_indexes()
            
            # loop over the indexes and create them in the database
            for index in indexes:
                await self.collection.create_index(  
                    index["key"],
                    name=index["name"],
                    unique=index['unique']
                )

    async def create_chunk(self,chunk:DataChunks)->DataChunks:
        result = await self.collection.insert_one(chunk.dict(by_alias=True,exclude_unset=True))
        chunk._id =result.inserted_id
        return chunk

    async def get_chunk(self,chunk_id:str)->DataChunks:
        result = await self.collection.find_one({"_id",ObjectId(chunk_id)}) 
        if result is None:
            return "there is no _id for this chunk"
        return DataChunks(**result)         
    
    # insert many chunks in the database
    async def insert_many_chunks(self,chunks:list,batch_size=100)->int:

        for i in range(0,len(chunks),batch_size):
            batch =chunks[i:i+batch_size] 

            operations=[
                InsertOne(chunk.dict(by_alias=True,exclude_unset=True))
                for chunk in batch      
            ]

        await self.collection.bulk_write(operations) 

        return len(chunks)
    
    async def delete_chunks_by_project_id(self,project_id:ObjectId)->str:
        result = await self.collection.delete_many({
            "chunk_project_id": project_id
        })
        
        if result.deleted_count >0:
            return {f"deleted {result.deleted_count}"}
        return "there is no deleted cunk"
    
    async def get_project_chunks(self,project_id:ObjectId,page_num:int=1,page_size:int=50)->list:
        records = await self.collection.find({
            "chunk_project_id": project_id
        }).skip((page_num-1)*page_size).limit(page_size).to_list(length=None)
        
        # return the records as a list of DataChunks
        return [
            DataChunks(**chunk) 
            for chunk in records
            ]

    
