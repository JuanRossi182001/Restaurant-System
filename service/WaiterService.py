from datetime import timedelta,datetime
from sqlalchemy.orm import Session
from schemas.waiterSchema import WaiterSchema
from model.waiter import Waiter
from fastapi import Depends, HTTPException
from sqlalchemy.orm.exc import NoResultFound
from passlib.context import CryptContext
from jose import jwt,JWTError
from fastapi.security import OAuth2PasswordBearer
from typing import Annotated

SECRET_KEY = '4a4e0a14fb014a0abbbd4fb72c8dfd72'
ALGORITH = 'HS256'
bycrypt_context = CryptContext(schemes=['bcrypt'], deprecated ='auto')
oauth_bearer = OAuth2PasswordBearer(tokenUrl='/token')



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
    _Waiter = Waiter(username = waiter.username,password=bycrypt_context.hash(waiter.password))
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



# authenticate waiter
def authenticate_user(waiterr: WaiterSchema,db: Session):
    _waiter = db.query(Waiter).filter(Waiter.username == waiterr.username).first()
    if not _waiter:
        return False
    if not bycrypt_context.verify(waiterr.password, _waiter.password):
        return False
    return _waiter

# create token 
def create_token(username: str, waiter_id: int, expires_delta: timedelta):
    encode = {'sub': username,'id': waiter_id}
    expires = datetime.utcnow() + expires_delta
    encode.update({'exp':expires})
    return jwt.encode(encode,SECRET_KEY,algorithm=ALGORITH)

# get current waiter
async def get_current_waiter(token: Annotated[str,Depends(oauth_bearer)]):
    try:
        payload = jwt.decode(token,SECRET_KEY)
        username: str = payload.get('sub')
        waiter_id: int = payload.get('id')
        if username is None or waiter_id is None:
            raise HTTPException(status_code=401,
                                detail="Could not validate Waiter")
        return{'username': username, 'id': waiter_id}
    except JWTError:
        raise HTTPException(status_code=401,detail="Could not validate Waiter")


def authenticate_user_2(username: str, password: str,db: Session):
    _waiter = db.query(Waiter).filter(Waiter.username == username).first()
    if not _waiter:
        return False
    if not bycrypt_context.verify(password, _waiter.password):
        return False
    return _waiter

