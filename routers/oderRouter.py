from tkinter import SE
from fastapi import APIRouter, Depends,HTTPException
from config.config import sessionLocal
from sqlalchemy.orm import Session
from schemas.orderSchema import RequestOrder,Response
from service.orderService import get_order_by_id,get_orders,create_order,delete_order,update_order


router = APIRouter()

def get_db():
    db = sessionLocal()
    try:
        yield db
    finally:
        db.close()
        
        
# create order end point
@router.post("/order/create")
async def create(request: RequestOrder, db: Session = Depends((get_db))):
    try:
        create_order(db=db,order=request.parameter)
        return Response(code="200", status="OK",message="Order created Successfully", result=None).dict(exclude_none=True)
    except Exception as e:
        return Response(code="500", status="Internal Server Error", message=str(e), result=None).dict(exclude_none=True)
    
    
# get all orders end point  
@router.get("/order")
async def get(db: Session = Depends((get_db))):
    _orders = get_orders(db=db)
    return Response(code="200", status="OK",message="succes fetch all data",result=_orders).dict(exclude_none=True)



# get order by id end point
@router.get("/order/{order_id}")
async def get_by_id(order_id: int, db: Session = Depends((get_db))):
    _order = get_order_by_id(db=db,order_id=order_id)
    if not _order:
        raise HTTPException(status_code=404,detail="Fail to get data, order not found")
    return Response(code="200",status="OK",message="Succes get data",result=_order).dict(exclude_none=True)



# update order end point
@router.patch("/order/update/{order_id}")
async def update(order_id: int, request: RequestOrder, db: Session = Depends((get_db))):
    _order = update_order(db=db,order_id=order_id,order_number=request.parameter.order_number,total=request.parameter.total,
                          state=request.parameter.state,assigned_table=request.parameter.assigned_table,assigned_waiter=request.parameter.assigned_waiter)
    return Response(code="200",status="OK",message ="Succes update data", result =_order)


# delete order end point    
@router.delete("/order/delete/{order_id}")
async def delete(order_id: int, db: Session = Depends((get_db))):
    delete_order(db=db,order_id=order_id)
    return Response(code="200", status="OK", message="Succes delete data", result={})
        