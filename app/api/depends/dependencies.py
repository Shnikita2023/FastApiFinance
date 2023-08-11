from typing import Annotated

from fastapi import Depends
from app.api.utils.unitofwork import UnitOfWork, IUnitOfWork

UOWDep = Annotated[UnitOfWork, Depends(UnitOfWork)]
