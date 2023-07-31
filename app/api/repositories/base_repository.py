from abc import ABC, abstractmethod
from typing import Any

from sqlalchemy import insert, select, delete, update
from sqlalchemy.exc import InvalidRequestError

from app.db.database import async_session_maker


class AbstractRepository(ABC):
    @abstractmethod
    async def add_one(self, data):
        raise NotImplementedError

    @abstractmethod
    async def find_all(self):
        raise NotImplementedError

    @abstractmethod
    async def find_one(self, data_id):
        raise NotImplementedError

    @abstractmethod
    async def delete_one(self, id_data):
        raise NotImplementedError

    @abstractmethod
    async def update_one(self, id_data, new_data):
        raise NotImplementedError

    @abstractmethod
    async def find_by_param(self, param_column, value):
        raise NotImplementedError

    @abstractmethod
    async def find_by_param_limit(self, param_column, value, index, count):
        raise NotImplementedError


class SQLAlchemyRepository(AbstractRepository):
    model = None

    async def add_one(self, data: dict) -> int:
        try:
            async with async_session_maker() as session:
                stmt = insert(self.model).values(**data).returning(self.model.id)
                res = await session.execute(stmt)
                await session.commit()
                return res.scalar_one()

        except ConnectionError:
            raise Exception("Ошибка подключения к базе данных")

        except InvalidRequestError:
            raise Exception("Некорректный запрос, проверьте формат данных")

        except Exception as ex:
            raise f"Ошибка {ex}"

    async def find_all(self) -> list[model]:
        try:
            async with async_session_maker() as session:
                stmt = select(self.model)
                res = await session.execute(stmt)
                res = [row[0].to_read_model() for row in res.all()]
                return res

        except ConnectionError:
            raise Exception("Ошибка подключения к базе данных")

        except InvalidRequestError:
            raise Exception("Некорректный запрос, проверьте формат данных")

        except Exception as ex:
            raise f"Ошибка {ex}"

    async def find_one(self, data_id: int) -> model:
        try:
            async with async_session_maker() as session:
                stmt = select(self.model).where(self.model.id == data_id)
                res = await session.execute(stmt)
                res = [row[0].to_read_model() for row in res.all()]
                return res[0]

        except ConnectionError:
            raise Exception("Ошибка подключения к базе данных")

        except InvalidRequestError:
            raise Exception("Некорректный запрос, проверьте формат данных")

        except Exception as ex:
            raise f"Ошибка {ex}"

    async def find_by_param(self, param_column: str, value: Any) -> list[model]:
        try:
            async with async_session_maker() as session:
                stmt = select(self.model).where(getattr(self.model, param_column) == value)
                res = await session.execute(stmt)
                res = [row[0].to_read_model() for row in res.all()]
                return res

        except ConnectionError:
            raise Exception("Ошибка подключения к базе данных")

        except InvalidRequestError:
            raise Exception("Некорректный запрос, проверьте формат данных")

        except Exception as ex:
            raise f"Ошибка {ex}"

    async def find_by_param_limit(self,
                                  param_column: str,
                                  value: Any,
                                  index: int,
                                  count: int) -> list[model]:
        try:
            async with async_session_maker() as session:
                stmt = (select(self.model).where(getattr(self.model, param_column) == value).
                        offset(index).limit(count))
                res = await session.execute(stmt)
                res = [row[0].to_read_model() for row in res.all()]
                return res

        except ConnectionError:
            raise Exception("Ошибка подключения к базе данных")

        except InvalidRequestError:
            raise Exception("Некорректный запрос, проверьте формат данных")

        except Exception as ex:
            raise f"Ошибка {ex}"

    async def delete_one(self, id_data: int) -> int:
        try:
            async with async_session_maker() as session:
                find_id = await session.get(self.model, id_data)
                if find_id:
                    stmt = delete(self.model).where(self.model.id == id_data).returning(self.model.id)
                    res = await session.execute(stmt)
                    await session.commit()
                    return res.scalar_one()

                raise InvalidRequestError("Данный id не существует")

        except ConnectionError:
            raise Exception("Ошибка подключения к базе данных")

        except InvalidRequestError:
            raise Exception("Некорректный запрос, проверьте формат данных")

        except Exception as ex:
            raise f"Ошибка {ex}"

    async def update_one(self, id_data: int, new_data: Any) -> dict:
        try:
            async with async_session_maker() as session:
                stmt = update(self.model).where(self.model.id == id_data).values(new_data)
                res = await session.execute(stmt)
                await session.commit()
                return new_data

        except ConnectionError:
            raise Exception("Ошибка подключения к базе данных")

        except InvalidRequestError:
            raise Exception("Некорректный запрос, проверьте формат данных")

        except Exception as ex:
            raise f"Ошибка {ex}"
