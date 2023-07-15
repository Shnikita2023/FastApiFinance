# import asyncio
#
# from fastapi import Depends, HTTPException
# from sqlalchemy import insert
# from sqlalchemy.ext.asyncio import AsyncSession
#
# from app.api.balance.models import Balance
# from app.db.database import get_async_session
#
#
# async def create_balance_user(user_id: int, session: AsyncSession):
#     try:
#         session = get_async_session()
#         balance = {"users_id": user_id, "total_balance": 0}
#         stmt = insert(Balance).values(**balance)
#         await session.execute(stmt)
#         await session.commit()
#
#     except Exception:
#         raise HTTPException(status_code=500, detail={
#             "status": "error",
#             "data": None,
#             "details": None
#         })
#
# if __name__ == '__main__':
#     asyncio.run(create_balance_user(13))