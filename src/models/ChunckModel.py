from .BaseDataModel import BaseDataModel
from .db_schemas import DataChunk
from .enums.DataBaseEnum import DataBaseEnum
from bson.objectid import ObjectId
from pymongo import InsertOne

class ChunckModel(BaseDataModel):
    
    def __init__(self, db_client: object):
            super().__init__(db_client=db_client)
            self.colletion = self.db_client[DataBaseEnum.COLLECTIN_CHUNK_NAME.value]
            

    async def create_chunck(self, chunck: DataChunk):
        result = await self.colletion.insert_one(chunck.dict(by_alias=True, exclude_unset=True))
        chunck._id = result.inserted_id
        return chunck
    
    async def get_chunck(self, chunck_id: str):
        result = await self.colletion.find_one({
            "_id": ObjectId(chunck_id)
        })
        
        if result is None: 
            return None 
        
        return DataChunk(**result)
    
    async def inset_many_chuncks(self, chuncks: list, batch_size: int=100):
        
        for i in range(0, len(chuncks), batch_size):
            batch = chuncks[i:i+batch_size]
            
            operations =[
                InsertOne(chunck.dict(by_alias=True, exclude_unset=True))
                for chunck in batch 
            ]
            
            await self.colletion.bulk_write(operations)
        
        return len(chuncks)
    
    
    async def delete_chuncks_by_project_id(self, project_id: ObjectId):
        result = await self.colletion.delete_many({
            "chunk_project_id": project_id
        })
        
        return result.deleted_count