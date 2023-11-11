from sqlalchemy.orm import Session
from model.order import Order
from schemas.orderSchema import OrderSchema


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
   return db.query(Order).filter(order_id == Order.id).first()
    
    
# create a new order
def create_order(db: Session,order: OrderSchema):
    _order = Order(order_number=order.order_number,total=order.total,
                   state=order.state,assigned_table=order.assigned_table,assigned_waiter=order.assigned_waiter)
    _order.total=_order.calculate_total()
    db.add(_order)
    db.commit()
    db.refresh(_order)
    return _order.as_dict()

# delete order by id
def delete_order(db: Session,order_id: int):
    _order = get_order_by_id(db=db,order_id=order_id)
    db.delete(_order)
    db.commit()
    return f"Order {order_id} successfully deleted"

# update order
def update_order(db: Session,order_id: int,order_number: int,total: int,state: str,assigned_table: int,assigned_waiter: int):
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
    
    
