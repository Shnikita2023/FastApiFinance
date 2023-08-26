from typing import Any

from ..category.shemas import CategoryCreate, CategoryGet
from ..utils.unitofwork import IUnitOfWork


class CategoryService:

    async def add_category(self, category: CategoryCreate, uow: IUnitOfWork) -> int:
        category_dict = category.dict()
        async with uow:
            category_id = await uow.category.add_one(category_dict)
            await uow.commit()
            return category_id

    async def get_categories(self, uow: IUnitOfWork) -> list[CategoryGet]:
        async with uow:
            all_category = await uow.category.find_all()
            return all_category

    async def get_category(self, id_category: int, uow: IUnitOfWork) -> CategoryGet:
        async with uow:
            one_category = await uow.category.find_one(id_category)
            return one_category

    async def get_category_by_param(self,
                                    param_column: str,
                                    value: Any,
                                    uow: IUnitOfWork) -> CategoryGet:
        async with uow:
            one_category = await uow.category.find_by_param(param_column, value)
            return one_category[0]

    async def delete_category(self, category_id: int, uow: IUnitOfWork) -> int:
        async with uow:
            id_category = await uow.category.delete_one(category_id)
            await uow.commit()
            return id_category
