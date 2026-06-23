from enum import Enum
from fastapi import APIRouter, HTTPException, Depends
from sqlmodel import select
from db import SessionDep
from models import *
import bcrypt
from auth import AuthHandler
from log import logger

router = APIRouter(prefix="/v1/user", tags=["User"])
auth_handler = AuthHandler()

@router.post('/' ,response_model=ResponseUser)
def Register(user: RegUser, session: SessionDep):
    check = session.exec(select(User).where(User.login==user.login.lower())).first()
    if check:
        raise HTTPException(409, "Пользователь с таким логином существует")
    
    check = session.exec(select(User).where(User.email==user.email.lower())).first()
    if check:
        raise HTTPException(409, "Пользователь с таким email существует")
    
    if user.password != user.confirm_psw:
        raise HTTPException(422, "Пароли не совпадают")
    
    role = session.exec(select(Role).where(Role.name=="Пользователь")).first()
    new_user = User(login=user.login.lower(), password=auth_handler.get_password_hash(user.password), email=user.email.lower(), role=role)

    session.add(new_user)
    session.commit()

    return new_user

@router.patch('/', response_model=ResponseUser)
def Login(user: LoginUser, session: SessionDep):
    check = session.exec(select(User).where(User.login==user.login)).first()
    if not check:
        raise HTTPException(404, "Пользователь с таким логином не найден")

    if not auth_handler.verify_password(user.password, check.password):
        raise HTTPException(403, "Неверный пароль")
    
    token = auth_handler.encode_token(str(check.id), check.role.name)
    refresh_token = auth_handler.encode_refresh_token(str(check.id))

    check.refresh_token = refresh_token
    session.add(check)
    session.commit()

    return {"id": check.id,
            "login": check.login,
            "email": check.email,
            "role": check.role,
            "access_token": token,
            "refresh_token": refresh_token}

@router.post("/refresh", response_model=ResponseUser)
def RefreshToken(session: SessionDep, refresh_token: str):
    session.expire_on_commit = False

    user_info = auth_handler.decode_token(refresh_token)
    user = session.exec(select(User).where(User.id==user_info['sub'])).first()
    if not user:
        raise HTTPException(404, "Пользователь не найден")
    
    if refresh_token != user.refresh_token:
        raise HTTPException(401, "Неверный токен")
    
    access_token = auth_handler.encode_token(str(user.id), user.role.name)
    new_refresh_token = auth_handler.encode_refresh_token(str(user.id))

    user.refresh_token = new_refresh_token
    session.add(user)
    session.commit()

    return {"id": user.id,
            "login": user.login,
            "email": user.email,
            "role": user.role,
            "access_token": access_token,
            "refresh_token": refresh_token}

@router.patch("/{id}", response_model=ResponseUser)
def UpdateUser(session: SessionDep, id: int, update_user: UpdateUser, token=Depends(auth_handler.auth_wrapper)):
    session.expire_on_commit = False
    
    if str(id) != token['sub'] and token['rol'] != "Администратор":
        raise HTTPException(403, "Недостаточно прав")
    
    user = session.exec(select(User).where(User.id==id)).first()

    if not user:
        raise HTTPException(404, "Пользователь не найден")

    if str(id) != token['sub'] and user.role.name == "Администратор":
        raise HTTPException(403, "Отказано в доступе")

    if update_user.role_id:
        if token['rol'] != "Администратор":
            raise HTTPException(403, "Недостаточно прав")
        role = session.exec(select(Role).where(Role.id==update_user.role_id)).first()
        if not role:
            raise HTTPException(404, "Неверная роль")
        
        admin = session.exec(select(User).where(User.id==token["sub"])).first()
        logger.info(f"Admin-user ({admin.id, admin.login}) changed the role of user ({user.id, user.login}) from {user.role.name} to {role.name}")
        user.role = role
    
    if update_user.login != "" and not update_user.login.isspace():
        if session.exec(select(User).where(User.login==update_user.login.lower())).first():
            raise HTTPException(409, "Пользователь с таким логином уже существует!")
        user.login = update_user.login.lower()
    
    if update_user.new_password != "" and not update_user.new_password.isspace():
        if (not auth_handler.verify_password(update_user.old_password, user.password) or token['rol'] != "Администратор") and (user.role.name == "Администратор"):
            raise HTTPException(403, "Неверный пароль")
        
        user.password = auth_handler.get_password_hash(update_user.new_password)
    
    if update_user.email:
        if session.exec(select(User).where(User.email==update_user.email.lower())).first():
            raise HTTPException(400, "Пользователь с таким email уже существует!")
        user.email = update_user.email.lower()
    
    session.add(user)
    session.commit()

    return user

@router.delete("/{id}")
def DeleteUser(session: SessionDep, id: int, token=Depends(auth_handler.auth_wrapper)):
    if str(id) != token['sub'] and token['rol'] != "Администратор":
        raise HTTPException(403, "Недостаточно прав")
    
    user = session.exec(select(User).where(User.id==id)).first()
    if not user:
        raise HTTPException(404, "Пользователь не найден")
    
    if str(id) != token['sub'] and user.role.name == "Администратор":
        raise HTTPException(403, "Отказано в доступе")
    
    logger.info(f"User ({user.id, user.login} has been deleted)")
    session.delete(user)
    session.commit()

    return {"msg": "success"}