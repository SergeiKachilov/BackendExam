from enum import Enum
from fastapi import APIRouter, HTTPException, Depends
from sqlmodel import select
from db import SessionDep
from models import *
import bcrypt
from auth import AuthHandler
from log import logger

router = APIRouter(prefix="/v1/specs", tags=["Specs"])
auth_handler = AuthHandler()

@router.get("/", response_model=list[Spec])
def GetSpecs(session: SessionDep):
    return session.exec(select(Spec)).all()

@router.get("/{id}", response_model=Spec)
def GetSpec(session: SessionDep, id: int):
    spec = session.exec(select(Spec).where(Spec.id==id)).first()
    if not spec:
        raise HTTPException(404, "Характеристика не найдена")
    return spec

@router.patch("/{spec_id}/{product_id}", response_model=ProductSpecs)
def EditProductSpec(session: SessionDep, spec_id: int, product_id: int, data: EditSpecs, token=Depends(auth_handler.auth_wrapper)):
    if token["rol"] == "Пользователь":
        raise HTTPException(403, "Недостаточно прав")
    
    user = session.exec(select(User).where(User.id==token["sub"])).first()
    logger.warning(f"User ({user.id}, {user.login}, {user.role.name}) tried to change the specification (id: {spec_id}) of product (id: {product_id}) with value: {data.value}")
    
    product_spec = session.exec(select(ProductSpecs).where(ProductSpecs.product_id==product_id, ProductSpecs.spec_id==spec_id)).first()
    if not product_spec:
        logger.error(f"Changing the specification caused an error with the code 404 (Not found)")
        raise HTTPException(404, "Характеристика у товара не найдена")
    
    if data.value.isspace():
        logger.error(f"Changing the specification caused an error with the code 422 (Value is white-spaced)")
        raise HTTPException(422, "Значение не может состоять из одних пробелов")
    
    logger.info(f"User ({user.id}, {user.login}, {user.role.name}) changed the specification (id: {spec_id}) of product (id: {product_id}) from value: {product_spec.value} to: {data.value}")
    product_spec.value = data.value

    session.expire_on_commit = False
    session.add(product_spec)
    session.commit()

    return product_spec

@router.post("/{spec_id}/{product_id}", response_model=ProductSpecs)
def AddProductSpec(session: SessionDep, spec_id: int, product_id: int, data: EditSpecs, token=Depends(auth_handler.auth_wrapper)):
    if token["rol"] == "Пользователь":
        raise HTTPException(403, "Недостаточно прав")
    
    user = session.exec(select(User).where(User.id==token["sub"])).first()
    logger.warning(f"User ({user.id}, {user.login}, {user.role.name}) tried to add the specification (id: {spec_id}) of product (id: {product_id}) with value: {data.value}")
    
    product = session.exec(select(Product).where(Product.id==product_id)).first()
    spec = session.exec(select(Spec).where(Spec.id==spec_id)).first()

    if not product:
        logger.error(f"Adding the specification caused an error with the code 404 (Product not found)")
        raise HTTPException(404, "Товар не найден")
    
    if not spec:
        logger.error(f"Adding the specification caused an error with the code 404 (Specification not found)")
        raise HTTPException(404, "Характеристика не найдена")

    product_spec = session.exec(select(ProductSpecs).where(ProductSpecs.product_id==product_id, ProductSpecs.spec_id==spec_id)).first()
    if product_spec:
        logger.error(f"Adding the specification caused an error with the code 409 (Specification of product already exist)")
        raise HTTPException(409, "Характеристика у товара уже существует")
    
    if data.value.isspace():
        logger.error(f"Adding the specification caused an error with the code 422 (Value is white-spaced)")
        raise HTTPException(422, "Значение не может состоять из одних пробелов")
    
    logger.info(f"User ({user.id}, {user.login}, {user.role.name}) added the specification (id: {spec_id}) of product (id: {product_id}) with value: {data.value}")
    new_product_spec = ProductSpecs(product_id=product_id, spec_id=spec_id, value=data.value)

    session.expire_on_commit = False
    session.add(new_product_spec)
    session.commit()

    return new_product_spec

@router.delete("/{spec_id}/{product_id}")
def DeleteProductSpec(session: SessionDep, spec_id: int, product_id: int, token=Depends(auth_handler.auth_wrapper)):
    if token["rol"] == "Пользователь":
        raise HTTPException(403, "Недостаточно прав")
    
    user = session.exec(select(User).where(User.id==token["sub"])).first()
    logger.warning(f"User ({user.id}, {user.login}, {user.role.name}) tried to delete the specification (id: {spec_id}) of product (id: {product_id})")

    product_spec = session.exec(select(ProductSpecs).where(ProductSpecs.product_id==product_id, ProductSpecs.spec_id==spec_id)).first()
    if not product_spec:
        logger.error(f"Deleting the specification caused an error with the code 404 (Not found)")
        raise HTTPException(404, "Характеристика у товара не найдена")
    
    logger.info(f"User ({user.id}, {user.login}, {user.role.name}) deleted the specification (id: {spec_id}) of product (id: {product_id}) with value: {product_spec.value}")
    session.delete(product_spec)
    session.commit()

    return {"msg": "success"}