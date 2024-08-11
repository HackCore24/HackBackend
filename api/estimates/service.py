import base64
from datetime import datetime
from io import BytesIO
import aiohttp
import cloudconvert
from fastapi import Depends, HTTPException, UploadFile
from jinja2 import Template
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from api.documents.model import Documents, DocumentsProjects
from api.estimates.model import Chapters, Service
from api.project.model import Projects
from utils.base.service import BaseService
from utils.base.session import AsyncDatabase


class ServicesService(BaseService):
    model = Chapters

    async def create_service(self, service_data):
        try:
            service = self.model(**service_data)
            self.session.add(service)
            await self.session.commit()
            await self.session.refresh(service)
            return service
        except IntegrityError as error:
            raise HTTPException(status_code=400, detail=f'{error}')

    async def all_services(self):
        return (await self.session.scalars(select(Service))).all()

    async def service_id(self, service_id):
        return await self.session.scalar(select(Service).where(Service.id == service_id))

    async def update_service(self, service_id, service_data):
        model = await self.service_id(service_id)
        for key, value in service_data.items():
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

    async def chapter(self, chapter_id):
        query = select(Service).where(Service.chapter_id == chapter_id)
        return (await self.session.scalars(query)).all()

    async def generate_estimate(self, project_id):
        project = await self.session.get(Projects, project_id)
        if not project:
            raise HTTPException(404, "project not found")



async def get_service_service(session=Depends(AsyncDatabase.get_session)):
    return ServicesService(session)


services_service: ServicesService = Depends(get_service_service)
