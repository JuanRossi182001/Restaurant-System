from typing import Optional,Generic,TypeVar
from pydantic import BaseModel, Field
from pydantic.generics import GenericModel

T = TypeVar('T')

class ProductSchema(BaseModel):
    id: Optional[int]=None
    name:Optional[str]=None
    description: Optional[str]=None
    price: Optional[float]=None
    
    class Config:
        orm_mode=True
        
        
        
class RequestProduct(BaseModel):
    parameter: ProductSchema = Field(...)
    
class Response(GenericModel, Generic[T]):
    code: str
    status: str
    message: str
    result: Optional[T]
    