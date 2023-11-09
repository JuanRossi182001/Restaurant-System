from sqlalchemy.orm import Session
from schemas.tableSchema import TableSchema
from model.table import Table


# get all tables 
def get_tables(db: Session):
   return db.query(Table).all()
    
# get table by id 
def get_table_by_id(db: Session, table_id:int):
    return db.query(Table).filter(Table.id == table_id).first()
    
    
# create a new table 
def create_table(db:Session, table: TableSchema):
    _table = Table(number=table.number,capacity=table.capacity,state=table.state)
    db.add(_table)
    db.commit()
    db.refresh(_table)
    return _table.as_dict()


# delete table by id
def delete_table_by_id(db: Session, table_id: int):
    _table = get_table_by_id(db=db,table_id=table_id)
    db.delete(_table)
    db.commit
    return f"Table {table_id} successfully deleted"

# update table 
def update_table(db:Session, number:int,capacity:int,state:str,table_id:int):
    _table = get_table_by_id(db=db,table_id=table_id)
    _table.number = number
    _table.capacity = capacity
    _table.state = state
    db.commit()
    db.refresh(_table)
    return _table.as_dict()
    
    
    
