from datetime import datetime
from sqlalchemy.orm import Session
from model.order import Order
from schemas.orderSchema import OrderSchema
from fastapi import HTTPException
from model.product import Product
from sqlalchemy.orm.exc import NoResultFound





# get all orders
def get_orders(db: Session):
    return db.query(Order).all()


# get open orders
def get_open_orders(db: Session):
    return db.query(Order).filter(Order.state == "open").all()


# get closed orders
def get_closed_orders(db: Session):
    return db.query(Order).filter(Order.state == "closed").all()


# get order by id
def get_order_by_id(db: Session,order_id: int):
    try:
     return db.query(Order).filter(order_id == Order.id).first()
    except:
        raise HTTPException(status_code=404,detail="Error, Order not found")
    

    
# create a new order
def create_order(db: Session,order: OrderSchema,waiter_id:int):
    products_list = []
    for product in order.products:
        p = db.query(Product).filter(Product.id == product).first()
        products_list.append(p)
    _order = Order(order_number=order.order_number,total=order.total,
                    state=order.state,assigned_table=order.assigned_table,assigned_waiter=waiter_id,
                        products = products_list,hour=order.hour)    
    current_time = datetime.utcnow()
    order.hour = current_time
    _order.total=_order.calculate_total()
    db.add(_order)
    db.commit()
    db.refresh(_order)
    return _order.as_dict()


# delete order by id
def delete_order(db: Session,order_id: int):
    try:
        _order = get_order_by_id(db=db,order_id=order_id)
        db.delete(_order)
        db.commit()
    except NoResultFound:
        raise HTTPException(status_code=404,detail="Error, Order not found")
    return f"Order {order_id} successfully deleted"


# update order
def update_order(db: Session,order_id: int,order_number: int,total: int,state: str,assigned_table: int,assigned_waiter: int):
    try:
        _order = get_order_by_id(db=db,order_id=order_id)
        _order.order_number = order_number
        _order.total =  total
        _order.state = state
        _order.assigned_table = assigned_table
        _order.assigned_waiter = assigned_waiter
        _order.total = _order.calculate_total()
        db.commit()
        db.refresh(_order)
        return _order.as_dict()
    except:
        raise HTTPException(status_code=422,detail="Unprocessable Entity")
    
    
