from sqlalchemy.orm import Session
from schemas.waiterSchema import WaiterSchema
from model.waiter import Waiter

# get all waiters
def get_waiters(db: Session):
  return db.query(Waiter).all()
    
    
# get waiter by id 
def get_waiter_by_id(waiter_id: int, db: Session):
    return db.query(Waiter).filter(waiter_id == Waiter.id).first()

# create a new waiter 
def create_waiter(waiter: WaiterSchema,db: Session):
    _Waiter = Waiter(username = waiter.username,password=waiter.password)
    db.add(_Waiter)
    db.commit
    db.refresh(_Waiter)
    return _Waiter.as_dict()


# delete by id
def delete_waiter_by_id(waiter_id: int,db: Session):
    _waiter = get_waiter_by_id(waiter_id=waiter_id,db=db)
    db.delete(_waiter)
    db.commit()
    return f"waiter {waiter_id} successfully deleted"

# update waiter
def update_waiter(db: Session, waiter_id: int, username: str, password: str):
    _waiter = get_waiter_by_id(waiter_id=waiter_id,db=db)
    _waiter.username = username
    _waiter.password = password
    db.commit()
    db.refresh(_waiter)
    return _waiter.as_dict()      


