from enum import Enum
from fastapi import APIRouter, HTTPException, Depends
from sqlmodel import select
from db import SessionDep
from models import *
import bcrypt
from auth import AuthHandler
from math import ceil

router = APIRouter(prefix="/v1/product", tags=["Products"])
auth_handler = AuthHandler()

class Order(str, Enum):
     name = "name"
     price = "price"
     id = "id"

@router.get("/", response_model=PageResponse)
def GetProducts(session: SessionDep, page: int = 1, els_on_page: int = 10, order: Order = "id", category_filter: int = None, min_price: float = None, max_price: float = None):
    cmnd = select(Product)
    
    if min_price:
        cmnd = cmnd.where(Product.price >= min_price)

    if max_price:
        cmnd = cmnd.where(Product.price <= max_price)
    
    if category_filter:
        cmnd = cmnd.where(Product.category_id==category_filter)

    if order in Order.name:
        cmnd = cmnd.order_by(Product.name)
    elif order in Order.price:
        cmnd = cmnd.order_by(Product.price)
    
    products = session.exec(cmnd.offset(els_on_page*(page - 1)).limit(els_on_page)).all()
    total_pages = ceil(len(session.exec(cmnd).all()) / els_on_page)
    
    return {"page": page,
             "elements_on_page": els_on_page,
             "total_pages": total_pages,
             "products": products}

@router.get("/{id}", response_model=ResponseProduct)
def GetProduct(session: SessionDep, id: int):
    product = session.exec(select(Product).where(Product.id==id)).first()

    if not product:
        raise HTTPException(404, "Товар не найден")
    
    return product

@router.post("/", response_model=ResponseProduct)
def AddProduct(session: SessionDep, product: NewProduct, token=Depends(auth_handler.auth_wrapper)):
    if token["rol"] != "Администратор":
        raise HTTPException(403, "Недостаточно прав")
    
    session.expire_on_commit = False

    if session.exec(select(Product).where(Product.name==product.name)).first():
        raise HTTPException(409, "Товар уже существует")

    if not session.exec(select(Category).where(Category.id==product.category_id)).first():
        raise HTTPException(404, "Категория не найдена")
    
    new_product = Product(name=product.name, description=product.description, category_id=product.category_id, price=product.price, quantity=product.quantity)
    
    session.add(new_product)

    session.commit()

    return new_product

@router.patch("/{id}", response_model=ResponseProduct)
def EditProduct(session: SessionDep, id: int, product: EditProduct, token=Depends(auth_handler.auth_wrapper)):
    if token['rol'] == "Пользователь":
        raise HTTPException(403, "Недостаточно прав")
    
    old = session.exec(select(Product).where(Product.id==id)).first()
    if not old:
        raise HTTPException(404, "Товар не найден")
    
    if product.name != "" and not product.name.isspace():
        if session.exec(select(Product).where(Product.name.lower()==product.name.lower())):
            raise HTTPException(409, "Товар с таким именем уже существует")
        
        old.name = product.name
    
    if product.description != "" and not product.description.isspace():
        old.description = product.description

    if product.category_id:
        if not session.exec(select(Category).where(Category.id==product.category_id)):
            raise HTTPException(404, "Категория не найдена")
        
        old.category_id = product.category_id
    
    if product.price:
        if token["rol"] != "Администратор":
            raise HTTPException(403, "Недостаточно прав")
        
        old.price = product.price
    
    if product.quantity:
        old.quantity = product.quantity
    
    session.expire_on_commit = False
    session.add(old)
    session.commit()

    return old

@router.delete("/{id}")
def DeleteProduct(session: SessionDep, id: int, token=Depends(auth_handler.auth_wrapper)):
    if token["rol"] != "Администратор":
        raise HTTPException(403, "Недостаточно прав")
    
    product = session.exec(select(Product).where(Product.id==id)).first()
    if not product:
        raise HTTPException(404, "Продукт не найден")
    
    session.delete(product)
    session.commit()

    return {"msg": "success"}