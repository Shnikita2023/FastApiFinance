# from fastapi import FastAPI
# from pydantic import BaseModel
# import asyncpg
# from app.config import DB_NAME, DB_PORT, DB_HOST, DB_PASS, DB_USER
#
# app = FastAPI()
#
#
# class Item(BaseModel):
#     id: int
#     comment: str
#
#
# async def connect_to_db():
#     conn = await asyncpg.connect(
#         host=DB_HOST,
#         port=DB_PORT,
#         user=DB_USER,
#         password=DB_PASS,
#         database=DB_NAME
#     )
#     return conn
#
#
# @app.get("/items/")
# async def get_items(page: int = 0, size: int = 10):
#     conn = await connect_to_db()
#
#     offset = page * size
#     query = f"SELECT * FROM transactions OFFSET {offset} LIMIT {size};"
#
#     items = []
#     async with conn.transaction():
#         async for record in conn.cursor(query):
#             items.append(record[0])
#
#     await conn.close()
#     return items
import uvicorn
from fastapi import FastAPI, Depends
from sqlalchemy import insert
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.balance.models import Balance
from app.api.category.models import Category
from app.api.category.shemas import CategoryCreate
from app.db.database import get_async_session

app = FastAPI()


@app.post("/category_balance/")
async def create_category_and_balance(category: CategoryCreate,
                                      db: AsyncSession = Depends(get_async_session)):
    try:
        # Начинаем транзакцию
        async with db.begin():
            stmt = insert(Category).values(**dict(category))
            await db.execute(stmt)
            balance = {
                "total_balance": "13",
                "users_id": 64
            }
            stmt = insert(Balance).values(**dict(balance))
            await db.execute(stmt)
        await db.commit()
        return {"message": "Category created successfully"}
    except Exception as ex:
        # В случае ошибки откатываем транзакцию
        await db.rollback()
        print(ex)
        return {"message": f"Error occurred while category {ex}"}


if __name__ == "__main__":
    uvicorn.run(app)
