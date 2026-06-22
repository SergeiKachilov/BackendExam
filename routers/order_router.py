from enum import Enum
from fastapi import APIRouter, HTTPException, Depends
from sqlmodel import select
from db import SessionDep
from models import *
import bcrypt
from auth import AuthHandler

router = APIRouter(prefix="/v1/order", tags=["Order"])
auth_handler = AuthHandler()

class OrderStatus(str, Enum):
    created = "Создан"
    in_proccess = "Обрабатывается"
    sent = "Отправлен"
    delivered = "Доставлен"
    cancelled = "Отменен"

@router.get("/", response_model=list[FullOrderResponse])
def GetOrders(session: SessionDep, is_available: bool = None, status: OrderStatus = None, token=Depends(auth_handler.auth_wrapper), user_id: int=None):
    if token["sub"] != str(user_id) and token["rol"] == "Пользователь":
        raise HTTPException(403, "Недостаточно прав")
    
    cmnd = select(Order)

    if is_available is not None:
        cmnd = cmnd.where(Order.is_available==is_available)
    
    if status in OrderStatus:
        stat = session.exec(select(Status).where(Status.name==status)).first()
        cmnd = cmnd.where(Order.status==stat)
    
    if user_id is not None:
        cmnd = cmnd.where(Order.user_id==user_id)
    
    orders = session.exec(cmnd).all()

    result = []
    for order in orders:
        full_price = 0
        for product in order.product_links:
            full_price += product.product.price * product.count
        
        result.append({
            "order": order,
            "full_price": full_price
        })

    return result

@router.get("/{id}", response_model=FullOrderResponse)
def GetOrder(session: SessionDep, id: int, token=Depends(auth_handler.auth_wrapper)):
    order = session.exec(select(Order).where(Order.id==id)).first()
    if not order:
        raise HTTPException(404, "Заказ не найден")
    
    if str(order.user_id) != token["sub"] and token["rol"] == "Пользователь":
        raise HTTPException(403, "Недостаточно прав")
    
    full_price = 0

    for product in order.product_links:
        full_price += product.product.price * product.count
    
    return {
        "order": order,
        "full_price": full_price
    }

@router.post("/", response_model=FullOrderResponse)
def AddProductToCart(session: SessionDep, product_id: int, token=Depends(auth_handler.auth_wrapper)):
    product = session.exec(select(Product).where(Product.id==product_id)).first()
    if not product:
        raise HTTPException(404, "Товар не найден")
    
    order = session.exec(select(Order).where(Order.user_id==token["sub"], Order.is_available==True)).first()
    if not order:
        order = Order(user_id=token["sub"], is_available=True)
        session.add(order)
    
    cart_el = session.exec(select(Cart).where(Cart.product_id==product_id, Cart.order_id==order.id)).first()
    if cart_el:
        cart_el.count += 1
        session.add(cart_el)
    else:
        order.product_links.append(Cart(order_id=order.id, product_id=product_id, count=1))
        session.add(order)
    
    session.expire_on_commit = False
    session.commit()

    full_price = 0

    for product in order.product_links:
        full_price += product.product.price * product.count
    
    return {
        "order": order,
        "full_price": full_price
    }

@router.patch("/{id}", response_model=FullOrderResponse)
def EditOrder(session: SessionDep, id: int, data: OrderData, token=Depends(auth_handler.auth_wrapper)):
    order = session.exec(select(Order).where(Order.id==id)).first()
    if not order:
        raise HTTPException(404, "Заказ не найден")

    if (not order.is_available or str(order.user_id) != token["sub"]) and token["rol"] == "Пользователь":
        raise HTTPException(403, "Недостаточно прав")
    
    if data.is_available == False and order.is_available:
        if data.address == "" or data.address.isspace():
            raise HTTPException(422, "Для создания заказа необходим адрес")
        if len(order.product_links) == 0:
            raise HTTPException(422, "Создание заказа невозможно с пустой корзиной")
        
        order.is_available = False
        order.address = data.address
        order.status = session.exec(select(Status).where(Status.name=="Создан")).first()
        order.date = datetime.now()
    
    if data.status_id is not None:
        status = session.exec(select(Status).where(Status.id==data.status_id)).first()
        if not status:
            raise HTTPException(404, "Статус не найден")
        
        if token["rol"] == "Пользователь":
            raise HTTPException(403, "Недостаточно прав")
        
        order.status = status

    if data.address != "" and not data.address.isspace():
        order.address = data.address
    
    if data.date is not None:
        order.date = data.date
    
    if data.new_products_id:
        products = session.exec(select(Product).where(Product.id.in_(data.new_products_id))).all()
        if len(products) == 0:
            raise HTTPException(404, "Товары не найдены")
        
        for product in products:
            cart = session.exec(select(Cart).where(Cart.order_id==order.id, Cart.product_id==product.id)).first()
            if not cart:
                cart = Cart(order_id=order.id, product_id=product.id, count=1)
                order.product_links.append(cart)
            else:
                cart.count += 1
    
    if data.delete_products_id:
        cart = session.exec(select(Cart).where(Cart.product_id.in_(data.delete_products_id), Cart.order_id==order.id)).all()
        if not cart:
            raise HTTPException(404, "Товары в корзине заказа не найдены")
        
        for el in cart:
            session.delete(el)
    
    session.expire_on_commit = False
    session.add(order)
    session.commit()

    full_price = 0

    for product in order.product_links:
        full_price += product.product.price * product.count
    
    return {
        "order": order,
        "full_price": full_price
    }

@router.patch("/", response_model=FullOrderResponse)
def ChangeAmount(session: SessionDep, id: int, data: AmountChange, token=Depends(auth_handler.auth_wrapper)):
    order = session.exec(select(Order).where(Order.id==id)).first()
    if not order:
        raise HTTPException(404, "Заказ не найден")

    if (not order.is_available or str(order.user_id) != token["sub"]) and token["rol"] == "Пользователь":
        raise HTTPException(403, "Недостаточно прав")
    
    cart = session.exec(select(Cart).where(Cart.order_id==id, Cart.product_id==data.product_id)).first()
    if not cart:
        raise HTTPException(404, "Товар в корзине заказа не найден")
    
    if data.amount == 0:
        session.delete(cart)
    else:
        cart.count = data.amount
        session.add(cart)
    
    session.commit()
    
    full_price = 0

    for product in order.product_links:
        full_price += product.product.price * product.count
    
    return {
        "order": order,
        "full_price": full_price
    }

@router.delete("/{id}")
def DeleteOrder(session: SessionDep, id: int, token=Depends(auth_handler.auth_wrapper)):
    if token["rol"] != "Администратор":
        raise HTTPException(403, "Недостаточно прав")
    
    order = session.exec(select(Order).where(Order.id==id)).first()
    session.delete(order)
    session.commit()

    return {"msg": "success"}