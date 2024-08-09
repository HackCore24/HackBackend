from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, cast, Date, text
from sqlalchemy.exc import IntegrityError, DBAPIError
from fastapi import HTTPException


class BaseService:
    model = None

    def __init__(self, session):
        self.session: AsyncSession = session

    async def all(self, paging=None):
        query = select(self.model).where(self.model.active.is_(True))
        query = query.offset(paging.skip).limit(paging.limit) if paging else query
        result = await self.session.scalars(query)
        if not result:
            return []
        return result.all()
    
    async def all_per_day(self):
        today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        query = select(self.model).where(self.model.created_at >= today).order_by(self.model.created_at)
        result = await self.session.execute(query)
        data = result.scalars().all()
        return data 
    
    async def id(self, model_id: str) -> object:
        model = await self.session.get(self.model, model_id)
        if model is not None:
            return model
        raise HTTPException(status_code=404, detail=f'object not found')
    
    async def create(self, data: dict):
        try:
            model = self.model(**data)
            self.session.add(model)
            await self.session.commit()
            await self.session.refresh(model)
            return model
        except IntegrityError as error:
            raise HTTPException(status_code=400, detail=f'{error}')

    async def delete(self, model_id: str):
        try:
            model = await self.id(model_id)
            if not model:
                raise HTTPException(404, "not found")
            await self.session.delete(model)
            await self.session.commit()
            return 200
        except IntegrityError as error:
            raise HTTPException(403, "There are links to other tables")
        except Exception as error:
            raise HTTPException(500, f"error")

    async def update(self, model_id: str, update_data: dict):
        model = await self.id(model_id)
        for key, value in update_data.items():
            if value is not None:
                attr_value = getattr(model, key)
                attr_value = attr_value.lower() if isinstance(attr_value, str) else attr_value
                validate_value = value.lower() if isinstance(value, str) else value
                if attr_value == validate_value:
                    continue
                else:
                    setattr(model, key, value)
        model.updated_at = datetime.utcnow()
        await self.session.commit()
        return model

    async def filter(self, query):
        result = await self.session.scalars(select(self.model).where(query))
        if not result:
            raise HTTPException(404, 'objects not found')
        return result
