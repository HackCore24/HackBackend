from fastapi import Depends, HTTPException
from sqlalchemy import select

from api.project_documentation.model import ProjectDocumentations
from utils.base.config import settings
from utils.base.service import BaseService
from utils.base.session import AsyncDatabase


class DocumentationService(BaseService):
    model = ProjectDocumentations

    async def project(self, project_id):
        return (await self.session.scalars(select(ProjectDocumentations)
                                          .where(ProjectDocumentations.project_id == project_id))).all()


async def get_documentation_service(session=Depends(AsyncDatabase.get_session)):
    return DocumentationService(session)


documentation_service: DocumentationService = Depends(get_documentation_service)
