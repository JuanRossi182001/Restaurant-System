from typing import Optional,Generic,TypeVar
from pydantic import BaseModel, Field
from pydantic.generics import GenericModel

T = TypeVar('T')

class WaiterSchema(BaseModel):
    username:Optional[str]=None
    password: Optional[str]=None
    
    class Config:
        orm_mode=True
        
        
        
class RequestWaiter(BaseModel):
    parameter: WaiterSchema = Field(...)
    

    
class Response(GenericModel, Generic[T]):
    code: str
    status: str
    message: str
    result: Optional[T]
    