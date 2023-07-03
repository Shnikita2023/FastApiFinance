# from fastapi import APIRouter, Depends, HTTPException
# from sqlalchemy import insert
# from sqlalchemy.ext.asyncio import AsyncSession
#
# from .models import Income
# from .shemas import IncomeCreate
# from app.db.database import get_async_session
#
#
# router_incomes = APIRouter(
#     prefix="/income",
#     tags=["incomes"]
# )
#
# @router_incomes.post("/add", summary='Добавление доходов')
# async def add_incomes(new_expense: IncomeCreate, session: AsyncSession = Depends(get_async_session)):
#     try:
#         stmt = insert(Income).values(**new_expense.dict())
#         await session.execute(stmt)
#         await session.commit()
#
#         return {
#             "status": "succeses",
#             "data": f"expense added",
#             "details": None
#         }
#
#     except Exception:
#         raise HTTPException(status_code=500, detail={
#             "status": "error",
#             "data": None,
#             "details": None
#         })
