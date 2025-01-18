from .BaseDataModel import BaseDataModel
from .db_schemes import Project
from .enums.DataBaseEnum import DataBaseEnum

class ProjectModel(BaseDataModel):
    def __init__(self,db_client:object):
        super().__init__(db_client=db_client)
        self.collection  = self.db_client[DataBaseEnum.COLLECTION_PROJECT_NAME.value] 

    # hnadle the async call to create an instance of the class
    @classmethod
    async def create_instance(cls,db_client:object)->object:  
        instance = cls(db_client)  
        await instance.init_collection()
        return instance

    # create function for indexing
    async def init_collection(self):
        all_collections = await self.db_client.list_collection_names()
        if DataBaseEnum.COLLECTION_PROJECT_NAME.value not in all_collections: # check if collection exist or not
            self.collection = self.db_client[DataBaseEnum.COLLECTION_PROJECT_NAME.value] # create one
            indexes = Project.get_indexes()
            # store the values in database
            for index in indexes:
                await self.collection.create_index( 
                    index["key"],
                    name=index["name"],
                    unique=index['unique']
                )

    async def create_project(self,project:Project)->Project:
        result = await self.collection.insert_one(project.dict(by_alias=True,exclude_unset=True))
        project.id = result.inserted_id

        return project
    
    async def get_project_or_create_one(self,project_id:str)->Project:
        record = await self.collection.find_one({"project_id":project_id})
    
        if record is None:
            #create new recored 
            project = Project(project_id=project_id)  
            project = await self.create_project(project=project)  
            return project 
        return Project(**record)
    

    async def get_all_project(self,page:int=1,page_size:int=10)->tuple:
        # count total numer of documnets
        total_documents = await self.collection.count_documents({})

        # calculate total number of pages
        total_pages = total_documents // page_size
        if total_documents % page_size > 0:
            total_pages+=1

        cursor = self.collection.find().skip((page-1)*page_size).limit(page_size)
        projects=[]
        async for doc in cursor:
            projects.append(Project(**doc))  

        return Project,total_pages
        