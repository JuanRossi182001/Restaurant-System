from datetime import timedelta
from fastapi import APIRouter,HTTPException,Depends
from config.config import sessionLocal
from sqlalchemy.orm import Session
from schemas.waiterSchema import RequestWaiter,Response
from service.WaiterService import authenticate_user_2, get_waiter_by_id,get_waiters,create_waiter,update_waiter,delete_waiter_by_id,authenticate_user,create_token
from model.token import Token
from typing import Annotated
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm 


router = APIRouter()

def get_db():
    db = sessionLocal()
    try:
        yield db
    finally:
        db.close()
        
        
        
# create waiter end point
@router.post("/waiter/create")
async def create(request: RequestWaiter, db: Session = Depends((get_db))):
    try:
        create_waiter(waiter=request.parameter,db=db)
        return Response(code="200", status="OK",message="Waiter created Successfully", result=None).dict(exclude_none=True)
    except Exception as e:
         raise HTTPException(status_code=500,detail="Fail to create data")
     
     
# get all waiters end point
@router.get("/waiter")
async def get(db: Session = Depends((get_db))):
   _waiters = get_waiters(db=db)
   return Response(code="200", status="OK",message="succes fetch all data",result=_waiters).dict(exclude_none=True)


# get waiter by id end point
@router.get("/waiter/{waiter_id}")
async def get_by_id(waiter_id: int, db: Session = Depends((get_db))):
    _waiter = get_waiter_by_id(db=db,waiter_id=waiter_id)
    if not _waiter:
        raise HTTPException(status_code=404,detail="Fail to get data, table not found")
    return Response(code="200",status="OK",message="Succes get data",result=_waiter).dict(exclude_none = True)


# update waiter end point
@router.patch("/waiter/update/{waiter_id}")
async def waiter_update(waiter_id: int, request: RequestWaiter, db: Session = Depends((get_db))):
    _waiter = update_waiter(db=db,waiter_id=waiter_id,username=request.parameter.username,
                            password=request.parameter.password)
    return Response(code="200",status="OK",message ="Succes update data", result =_waiter).dict(exclude_none = True)

# delete waiter end point 
@router.delete("/waiter/delete/{waiter_id}")
async def delete (waiter_id: int, db: Session = Depends((get_db))):
    delete_waiter_by_id(waiter_id=waiter_id,db=db)
    return Response(code="200", status="OK", message="Succes delete data", result={}).dict(exclude_none = True)
    
    
    
# authenticate waiter
@router.post ("/waiter/auth")
async def auth (request: RequestWaiter, db: Session = Depends((get_db))):
    try:
        _waiter = authenticate_user(waiterr=request.parameter,db=db)
        if not _waiter:
            raise HTTPException(status_code=401,detail="fail to athenticate")
        return Response(code="200", status="OK", message="successfully authenticated", result=_waiter).dict(exclude_none = True)
    except:
        raise HTTPException(status_code=500,detail="fatal error")
        
        
        
@router.post("/token",response_model=Token)
async def login_for_token(form_data:  Annotated[OAuth2PasswordRequestForm,Depends()],db: Session = Depends((get_db))):
    waiter = authenticate_user_2(form_data.username,form_data.password,db=db)
    if not waiter:
        raise HTTPException(status_code=401,detail="Could not validate Waiter")
    
    token = create_token(waiter.username,waiter.id,timedelta(minutes=10))
    
    return {'access_token': token, 'token_type': 'bearer'}
    
    