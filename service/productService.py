from sqlalchemy.orm import Session
from model.product import Product
from schemas.productSchema import ProductSchema
from fastapi import HTTPException
from sqlalchemy.orm.exc import NoResultFound

# get all products
def get_products(db:Session):
    return db.query(Product).all()
    


# get product by id 
def get_product_by_id(db: Session, product_id: int):
    try:
        return db.query(Product).filter(Product.id == product_id).first()
    except: raise HTTPException(status_code=404,detail="Error, Product not found")
        

# create a new product
def create_product(db: Session,product: ProductSchema):
    _product = Product(name=product.name,description=product.description,price=product.price) 
    db.add(_product)
    db.commit()
    db.refresh(_product)
    return _product.as_dict()


# delete product by id 
def delete_product(db: Session, product_id: int):
    try:
        _product = get_product_by_id(db=db,product_id=product_id)
        db.delete(_product)
        db.commit()
    except NoResultFound:
        raise HTTPException(status_code=404,detail="Error, Product not found")
    return f"Product {product_id} successfully deleted"

# update product
def update_product(db:Session,product_id: int,name: str, description: str,price:float):
    try:
        _product = get_product_by_id(db=db,product_id=product_id)
        _product.name = name
        _product.description = description
        _product.price =price
        db.commit()
        db.refresh(_product)
        return _product.as_dict()
    except:
        raise HTTPException(status_code=422,detail="Unprocessable Entity")



    