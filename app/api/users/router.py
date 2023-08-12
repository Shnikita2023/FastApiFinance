import math
from typing import Any

from fastapi import APIRouter, Depends, Request, Query
from starlette.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

from ..auth.base import current_user
from ..depends.dependencies import UOWDep
from ..transaction.services import TransactionService
from ..users.models import User

templates = Jinja2Templates(directory="app/api/templates")

router_register = APIRouter(
    prefix="/register",
    tags=["Registrations"]
)

router_authentic = APIRouter(
    prefix="/authentic",
    tags=["Authentications"]
)


@router_register.get("/", response_class=HTMLResponse, summary="Шаблон регистрации")
async def register_user(request: Request) -> Any:
    return templates.TemplateResponse("register_user.html", {"request": request})


@router_authentic.get("/", response_class=HTMLResponse, summary="Шаблон аутентификации")
async def get_template_authentic(request: Request) -> Any:
    return templates.TemplateResponse("authentic.html", {"request": request})


@router_authentic.get("/cabinet", response_class=HTMLResponse, summary="Шаблон кабинета авторизованного user")
async def get_template_authentic_user(request: Request, user: User = Depends(current_user)) -> Any:
    return templates.TemplateResponse("cabinet.html", {"request": request})


@router_authentic.get("/cabinet/get_data_user", response_class=HTMLResponse,
                      summary="Шаблон получение данных пользователя")
async def get_data_user(request: Request, user: User = Depends(current_user)) -> Any:
    data_user = {
        "Почта": user.email,
        "Пароль": "*********",
        "Имя": user.first_name,
        "Фамилия": user.last_name,
        "Никнейм": user.username,
        "Дата регистрации": user.registered_at,
    }
    return templates.TemplateResponse("get_data_user.html", {"request": request, "data_user": data_user})


@router_authentic.get("/reset_password", summary="Форма сброса пароля", response_class=HTMLResponse)
async def reset_pass(request: Request, token: str) -> Any:
    return templates.TemplateResponse("reset_password.html", {"request": request, 'token': token})


@router_authentic.get("/send_email", summary="Отправка email", response_class=HTMLResponse)
async def send_email(request: Request) -> Any:
    return templates.TemplateResponse("email_recovery.html", {"request": request})


@router_authentic.get("/cabinet/report", summary="Шаблон отчётов", response_class=HTMLResponse)
async def send_report_transaction(request: Request,
                                  uow: UOWDep,
                                  user: User = Depends(current_user),
                                  page: int = Query(default=1, ge=1),
                                  size: int = Query(default=10)
                                  ) -> Any:
    start = (page - 1) * size
    end = start + size
    list_transaction = await TransactionService().get_transaction_by_param_limit(value=user.id, page=start, size=size,
                                                                                 uow=uow)
    all_transactions = await TransactionService().get_transaction_by_param(value=user.id, uow=uow)
    total_transaction = len(all_transactions)
    total_pages = math.ceil(total_transaction / size)

    return templates.TemplateResponse("reports.html",
                                      {"request": request,
                                       "data_transactions": list_transaction,
                                       "start": start,
                                       "end": end,
                                       "page": page,
                                       "total": total_transaction,
                                       "total_pages": total_pages
                                       })
