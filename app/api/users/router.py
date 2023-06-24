from fastapi import APIRouter, Depends, HTTPException, Form, Request
from sqlalchemy import insert, select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse

from app.api.auth.base import fastapi_users
from app.api.users.shemas import UserCreate
from app.db.database import get_async_session

templates = Jinja2Templates(directory="app/api/templates")

router_register = APIRouter(
    prefix="/register",
    tags=["Regisration"]
)

router_authentic = APIRouter(
    prefix="/authentic",
    tags=["Authentication"]
)


@router_register.get("/", response_class=HTMLResponse)
async def register_user(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})


@router_authentic.get("/", response_class=HTMLResponse)
async def register_user(request: Request):
    return templates.TemplateResponse("authentic.html", {"request": request})


@router_authentic.get("/cabinet", response_class=HTMLResponse)
async def register_user(request: Request):
    return templates.TemplateResponse("base_cabinet.html", {"request": request})

