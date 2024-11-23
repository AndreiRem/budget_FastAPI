from app.db.session import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends


def get_service_factory(repository_class, service_class):
    def get_service(db: AsyncSession = Depends(get_db)):
        repository = repository_class(db)
        return service_class(repository)
    return get_service
