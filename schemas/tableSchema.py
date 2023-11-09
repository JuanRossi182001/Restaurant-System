from typing import Optional,Generic,TypeVar
from pydantic import BaseModel, Field
from pydantic.generics import GenericModel

T = TypeVar('T')

class TableSchema(BaseModel):
    number:Optional[int]=None
    capacity: Optional[int]=None
    state: Optional[str]=None
    
    class Config:
        orm_mode=True
        
        
        
class RequestTable(BaseModel):
    parameter: TableSchema = Field(...)
    

    
class Response(GenericModel, Generic[T]):
    code: str
    status: str
    message: str
    result: Optional[T]
    
    