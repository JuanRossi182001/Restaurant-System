from sqlalchemy.orm import Session
from schemas.waiterSchema import WaiterSchema
from model.waiter import Waiter
from fastapi import HTTPException
from sqlalchemy.orm.exc import NoResultFound

# get all waiters
def get_waiters(db: Session):
  return db.query(Waiter).all()
    
    
# get waiter by id 
def get_waiter_by_id(waiter_id: int, db: Session):
    try:
        return db.query(Waiter).filter(waiter_id == Waiter.id).first()
    except:
        raise HTTPException(status_code=404,detail="Error, Waiter not found")

# create a new waiter 
def create_waiter(db: Session,waiter: WaiterSchema):
    _Waiter = Waiter(username = waiter.username,password=waiter.password)
    db.add(_Waiter)
    db.commit()
    db.refresh(_Waiter)
    return _Waiter.as_dict()


# delete by id
def delete_waiter_by_id(waiter_id: int,db: Session):
    try:
        _waiter = get_waiter_by_id(waiter_id=waiter_id,db=db)
        db.delete(_waiter)
        db.commit()
        return f"waiter {waiter_id} successfully deleted"
    except NoResultFound:
        raise HTTPException(status_code=404,detail="Error, Waiter not found")

# update waiter
def update_waiter(db: Session, waiter_id: int, username: str, password: str):
    try:
        _waiter = get_waiter_by_id(waiter_id=waiter_id,db=db)
        _waiter.username = username
        _waiter.password = password
        db.commit()
        db.refresh(_waiter)
        return _waiter.as_dict()
    except:
        raise HTTPException(status_code=422,detail="Unprocessable Entity")  


