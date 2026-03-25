from fastapi import Depends,FastAPI
from fastapi.middleware.cors import CORSMiddleware
from models import product
from database import sessionLocal, engine
import database_models
from sqlalchemy.orm import session
app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3001"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

database_models.Base.metadata.create_all(bind=engine)
@app.get("/")
def greet():
    return "welcome to my fastapi"

products = [
    product(id=1, name="Phone", description="A smartphone", price=699.99, quantity=50),
    product(id=2, name="Laptop", description="A powerful laptop", price=999.99, quantity=30),
    product(id=3, name="Pen", description="A blue ink pen", price=1.99, quantity=100),
    product(id=4, name="Table", description="A wooden table", price=199.99, quantity=20),
]

def get_db():
    db=sessionLocal()
    try:
        yield db
    finally:
        db.close()
    

def init_db():
    db= sessionLocal()
    
    count=db.query(database_models.product).count
   
    if count==0:
       for product in products:
        db.add(database_models.product(**product.model_dump()))
       db.commit()    
init_db()    
        
        
@app.get("/products")
def get_all_products(db:session =Depends(get_db)):
    products=db.query(database_models.product).all()
    return products

@app.get("/products/{id}")
def get_product_by_id(id:int,db:session =Depends(get_db)):
    product=db.query(database_models.product).filter(database_models.product.id==id).first()
    if product:
        return product
    return "product not found"

@app.post("/products/{id}")
def add_product(product: product,db:session =Depends(get_db)):
    db.add(database_models.product(**product.model_dump()))
    db.commit()
    return product
@app.put("/products/{id}")
def update_product(id:int,product:product,db:session =Depends(get_db)):
    product=db.query(database_models.product).filter(database_models.product.id==id).first()
    if product:
        product.name = product.name
        product.description=product.description
        product.price=product.price
        product.quantity=product.quantity
        db.commit()
        return "product updated"
    else:
        return 'No product'    

@app.delete("/products/{id}")
def delete_product(id:int,db:session =Depends(get_db)):
    product=db.query(database_models.product).filter(database_models.product.id==id).first()
    if product:
        db.delete(product)
        db.commit()   
    else:  
     return "product not found"
    