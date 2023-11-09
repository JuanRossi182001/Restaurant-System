from fastapi import APIRouter,HTTPException,Depends
from config.config import sessionLocal
from sqlalchemy.orm import Session
from schemas.tableSchema import RequestTable,Response
from service.tableService import create_table,delete_table_by_id,get_table_by_id,get_tables,update_table


router = APIRouter()

def get_db():
    db = sessionLocal()
    try:
        yield db
    finally:
        db.close()
        
# create table end point    
@router.post("/table/create")
async def create( request: RequestTable, db: Session = Depends((get_db))):
    try:
        create_table(db=db,table=request.parameter)
        return Response(code="200", status="OK",message="Table created Successfully", result=None).dict(exclude_none=True)
    except Exception as e:
        raise HTTPException(status_code=500,detail="Fail to create data")
    
    
# get all tables end point 
@router.get("/table")
async def get(db: Session = Depends((get_db))):
    _tables = get_tables(db)
    return Response(code="200", status="OK",message="succes fetch all data",result=_tables).dict(exclude_none=True)

# get table by id end point 
@router.get("/table/{table_id}")
async def get_by_id(table_id: int, db: Session = Depends((get_db))):
    _table = get_table_by_id(db,table_id)
    if not _table:
        raise HTTPException(status_code=404,detail="Fail to get data, table not found")
    return Response(code="200",status="OK",message="Succes get data",result=_table).dict(exclude_none=True)

# update table end point 
@router.patch("/table/update/{table_id}")
async def update(table_id: int,request: RequestTable, db: Session = Depends((get_db))):
    _table = update_table(db,table_id=table_id,number=request.parameter.number,
                          capacity=request.parameter.capacity,state=request.parameter.state)
    return Response(code="200",status="OK",message ="Succes update data", result =_table)


# delete table end point 
@router.delete("/table/delete/{table_id}")
async def delete(table_id: int, db: Session = Depends((get_db))):
    delete_table_by_id(db,table_id)
    return Response(code="200", status="OK", message="Succes delete data", result={})

    


    
        
    