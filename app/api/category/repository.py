from ..category.models import Category
from ..repositories.base_repository import SQLAlchemyRepository


class CategoryRepository(SQLAlchemyRepository):
    model = Category
