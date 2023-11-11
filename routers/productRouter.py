from fastapi import APIRouter, Depends,HTTPException
from config.config import sessionLocal
from sqlalchemy.orm import Session
from schemas.productSchema import RequestProduct,Response
from service.productService import create_product,delete_product,get_product_by_id,get_products,update_product


router = APIRouter()

def get_db():
    db = sessionLocal()
    try:
        yield db
    finally:
        db.close()
        

# create product end point    
@router.post("/product/create")
async def create(request: RequestProduct, db: Session = Depends((get_db))):
    try:
        create_product(db=db,product=request.parameter)
        return Response(code="200", status="OK",message="Product created Successfully", result=None).dict(exclude_none=True)
    except Exception as e:
        return Response(code="500", status="Internal Server Error", message=str(e), result=None).dict(exclude_none=True)
    
    
# get all products end point 
@router.get("/product")
async def get(db: Session =Depends(get_db)):
    _Products = get_products(db)
    return Response(code="200", status="OK",message="succes fetch all data",result=_Products).dict(exclude_none=True)


# get product by id end point 
@router.get("/product/{product_id}")
async def get_by_id( product_id:int, db: Session=Depends((get_db))):
    _product = get_product_by_id(db,product_id)
    if not _product:
        raise HTTPException(status_code=404,detail="Fail to get data, product not found")
    return Response(code="200",status="OK",message="Succes get data",result=_product).dict(exclude_none=True)



# update product end point 
@router.patch("/product/update/{product_id}")
async def update_productt(product_id: int ,request: RequestProduct, db: Session = Depends(get_db)):
    _product = update_product(db,product_id=product_id,
                              name=request.parameter.name,description=request.parameter.description,
                              price=request.parameter.price)
    return Response(code="200",status="OK",message ="Succes update data", result =_product)
    


# delete product end point
@router.delete("/product/delete/{product_id}")
async def product_delete(product_id: int, db: Session=Depends((get_db))):
    delete_product(db,product_id=product_id)
    return Response(code="200", status="OK", message="Succes delete data", result={})
    
