from enum import Enum
from fastapi import APIRouter, HTTPException, Depends
from sqlmodel import select
from db import SessionDep
from models import *
import bcrypt
from auth import AuthHandler
from log import logger

router = APIRouter(prefix="/v1/image", tags=["Image"])
auth_handler = AuthHandler()

@router.get("/", response_model=list[Image])
def GetImages(session: SessionDep, product_id: int = None, is_main: bool = None):
    cmnd = select(Image)

    if product_id is not None:
        if not session.exec(select(Product).where(Product.id==product_id)).first():
            raise HTTPException(404, "Товар не найден")
        cmnd = cmnd.where(Image.product_id==product_id)
    
    if is_main is not None:
        cmnd = cmnd.where(Image.is_main==is_main)

    return session.exec(cmnd).all()

@router.get("/{id}", response_model=Image)
def GetImage(session: SessionDep, id: int):
    img = session.exec(select(Image).where(Image.id==id)).first()
    if not img:
        raise HTTPException(404, "Изображение не найдено")

    return img

@router.post("/", response_model=Image)
def AddImage(session: SessionDep, img: NewImage, token=Depends(auth_handler.auth_wrapper)):
    if token["rol"] == "Пользователь":
        raise HTTPException(403, "Недостаточно прав")
    
    user = session.exec(select(User).where(User.id==token["sub"])).first()
    logger.warning(f"User ({user.id}, {user.login}, {user.role.name}) tried to add image for product (id: {img.product_id})")

    if not session.exec(select(Product).where(Product.id==img.product_id)).first():
        logger.error(f"Adding the image caused an error with the code 404 (Product not found)")
        raise HTTPException(404, "Продукт не найден")
    
    if img.is_main:
        old_main_img = session.exec(select(Image).where(Image.product_id==img.product_id, Image.is_main==True)).first()
        if old_main_img:
            old_main_img.is_main = False
            logger.info(f"Image (id: {old_main_img}) is not main anymore")
            session.add(old_main_img)
    
    elif not session.exec(select(Image).where(Image.product_id==img.product_id)).first():
        img.is_main = True
    
    new_img = Image(product_id=img.product_id, image_link=img.image_link, is_main=img.is_main)
    
    session.expire_on_commit = False
    session.add(new_img)
    session.commit()
    logger.info(f"User ({user.id}, {user.login}, {user.role.name}) successfully added image (id: {new_img.id}, link: {new_img.image_link}, product_id: {img.product_id}, is_main: {img.is_main}) for product (id: {img.product_id})")

    return new_img

@router.patch("/{id}", response_model=Image)
def EditImage(session: SessionDep, img: EditImg, id: int, token = Depends(auth_handler.auth_wrapper)):
    if token["rol"] == "Пользователь":
        raise HTTPException(403, "Недостаточно прав")
    
    user = session.exec(select(User).where(User.id==token["sub"])).first()
    logger.warning(f"User ({user.id}, {user.login}, {user.role.name}) tried to change image (id: {id}) information")

    old_img = session.exec(select(Image).where(Image.id==id)).first()
    if not old_img:
        logger.error(f"Changing the image information caused an error with the code 404 (Image not found)")
        raise HTTPException(404, "Изображение не найдено")
    
    if img.image_link:
        old_img.image_link = img.image_link

    if img.is_main is not None:
        if img.is_main:
            old_main_img = session.exec(select(Image).where(Image.product_id==old_img.product_id, Image.is_main==True)).first()
            if old_main_img:
                old_main_img.is_main = False
                session.add(old_main_img)
            
            old_img.is_main = True
            
        elif old_img.is_main:
            new_main_img = session.exec(select(Image).where(Image.id != id, Image.product_id==old_img.product_id)).first()
            if not new_main_img:
                logger.error(f"Changing the image information caused an error with the code 424 (The product has no other images)")
                raise HTTPException(424, "У товара нет других изображений, изменение статуса невозможно")

            old_img.is_main = False
            new_main_img.is_main = True
            session.add(new_main_img)
    
    session.expire_on_commit = False
    session.add(old_img)
    session.commit()

    logger.info(f"User ({user.id}, {user.login}, {user.role.name}) successfully changed image information (id: {old_img.id}, link: {old_img.image_link}, product_id: {old_img.product_id}, is_main: {old_img.is_main}) for product (id: {old_img.product_id})")
    
    return old_img
    
@router.delete("/{id}")
def DeleteImage(session: SessionDep, id: int, token=Depends(auth_handler.auth_wrapper)):
    if token["rol"] == "Пользователь":
        raise HTTPException(403, "Недостаточно прав")
    
    user = session.exec(select(User).where(User.id==token["sub"])).first()
    logger.warning(f"User ({user.id}, {user.login}, {user.role.name}) tried to delete image (id: {id})")

    img = session.exec(select(Image).where(Image.id==id)).first()
    if not img:
        logger.error(f"Deleting the image caused an error with the code 404 (Image not found)")
        raise HTTPException(404, "Изображение не найдено")
    
    if img.is_main:
        new_main_img = session.exec(select(Image).where(Image.id != id, Image.product_id==img.product_id)).first()
        if not new_main_img:
            logger.error(f"Deleting the image caused an error with the code 424 (The product has no other images)")
            raise HTTPException(424, "У товара нет других изображений, удаление невозможно")
        
        new_main_img.is_main = True
    
    session.delete(img)
    session.commit()
    logger.info(f"User ({user.id}, {user.login}, {user.role.name}) successfully deleted the image (id: {id}, link: {img.image_link}, product_id: {img.product_id}, is_main: {img.is_main}) for product (id: {img.product_id})")

    return {"msg": "success"}