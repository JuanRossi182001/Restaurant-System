
from fastapi import FastAPI
from model import order,product,table,waiter
from config.config import engine
from routers import productRouter

app=FastAPI()
app.include_router(productRouter.router)

product.base.metadata.create_all(bind=engine)
order.base.metadata.create_all(bind=engine)
table.base.metadata.create_all(bind=engine)
waiter.base.metadata.create_all(bind=engine)




