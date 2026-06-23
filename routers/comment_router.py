from enum import Enum
from fastapi import APIRouter, HTTPException, Depends
from sqlmodel import select
from db import SessionDep
from models import *
import bcrypt
from auth import AuthHandler
from log import logger

router = APIRouter(prefix="/v1/comments", tags=["Comments"])
auth_handler = AuthHandler()

@router.get("/",response_model=list[Comments])
def GetComments(session: SessionDep, product_id: int=None, user_id=None):
    cmnd = select(Comments)

    if product_id is not None:
        if not session.exec(select(Product).where(Product.id==product_id)).first():
            raise HTTPException(404, "Товар не найден")
        
        cmnd = cmnd.where(Comments.product_id==product_id)
    
    if user_id is not None:
        if not session.exec(select(User).where(User.id==user_id)).first():
            raise HTTPException(404, "Пользователь не найден")
        
        cmnd = cmnd.where(Comments.user_id==user_id)

    return session.exec(cmnd).all()

@router.get("/{id}", response_model=Comments)
def GetComment(session: SessionDep, id: int):
    comment = session.exec(select(Comments).where(Comments.id==id)).first()
    if not comment:
        raise HTTPException(404, "Отзыв не найден")
    return comment

@router.post("/", response_model=Comments)
def AddComment(session: SessionDep, comment: NewComment, token=Depends(auth_handler.auth_wrapper)):
    product = session.exec(select(Product).where(Product.id==comment.product_id)).first()
    if not product:
        raise HTTPException(404, "Товар не найден")
    
    if comment.text.isspace():
        raise HTTPException(422, "Текст отзыва не может состоять из пробелов")
    
    new_comment = Comments(product_id=product.id, user_id=int(token["sub"]), rate=comment.rate, text=comment.text)
    
    session.expire_on_commit = False
    session.add(new_comment)
    session.commit()

    return new_comment

@router.patch("/{id}", response_model=Comments)
def EditComment(session: SessionDep, id: int, data: EditComment, token=Depends(auth_handler.auth_wrapper)):
    comment = session.exec(select(Comments).where(Comments.id==id)).first()
    if not comment:
        raise HTTPException(404, "Отзыв не найден")
    
    if comment.user_id != int(token["sub"]):
        raise HTTPException(403, "Отказано в доступе")
    
    if data.rate is not None:
        comment.rate = data.rate
    
    if data.text is not None:
        comment.text = data.text
    
    session.expire_on_commit = False
    session.add(comment)
    session.commit()

    return comment

@router.delete("/{id}")
def DeleteComment(session: SessionDep, id: int, data: DeleteComment, token=Depends(auth_handler.auth_wrapper)):
    comment = session.exec(select(Comments).where(Comments.id==id)).first()
    if not comment:
        raise HTTPException(404, "Отзыв не найден")
    
    user = session.exec(select(User).where(User.id==token["sub"])).first()

    if comment.user_id != int(token["sub"]) and token["rol"] != "Администратор":
        raise HTTPException(403, "Недостаточно прав")
    
    if comment.user_id != int(token["sub"]) and (data.reason == None or data.reason == "" or data.reason.isspace()):
        raise HTTPException(422, "Для удаления комментария нужно указать причину")
    
    if comment.user_id != int(token["sub"]):
        logger.info(f"Admin-user ({user.id}, {user.login}) deleted the comment (id: {comment.id}) of user ({comment.user_id, comment.user.login}) for a reason: {data.reason}")
    
    session.delete(comment)
    session.commit()

    return {"msg": "success"}