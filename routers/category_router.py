from enum import Enum
from fastapi import APIRouter, HTTPException, Depends
from sqlmodel import select
from db import SessionDep
from models import *
import bcrypt
from auth import AuthHandler

router = APIRouter(prefix="/v1/category", tags=["Category"])
auth_handler = AuthHandler()

@router.get("/", response_model=list[Category])
def GetCategories(session: SessionDep):
    return session.exec(select(Category)).all()

@router.get("/{id}", response_model=Category)
def GetCategory(session: SessionDep, id: int):
    category = session.exec(select(Category).where(Category.id==id)).first()
    if not category:
        raise HTTPException(404, "Категория не найдена")
    
    return category