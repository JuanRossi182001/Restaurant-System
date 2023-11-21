
from datetime import datetime
from typing import Optional,Generic,TypeVar,List
from pydantic import BaseModel, Field
from pydantic.generics import GenericModel
from schemas.productSchema import ProductSchema



T = TypeVar('T')

class OrderSchema(BaseModel):
    order_number: Optional[int]=None
    hour: Optional[datetime] = None
    total: Optional[float]=None
    state: Optional[str]=None
    assigned_table: Optional[int]=None
    assigned_waiter: Optional[int]=None
    products: Optional[List[int]] = None
    

    
    
    class Config:
        orm_mode=True
        
        
        
class RequestOrder(BaseModel):
    parameter: OrderSchema = Field(...)
    

    
class Response(GenericModel, Generic[T]):
    code: str
    status: str
    message: str
    result: Optional[T]
    