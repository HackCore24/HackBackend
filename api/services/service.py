import base64
from io import BytesIO
import aiohttp
import cloudconvert
from fastapi import Depends, HTTPException, UploadFile
from jinja2 import Template
from sqlalchemy import select
from api.documents.model import Documents, DocumentsProjects
from api.services.model import Chapters
from utils.base.service import BaseService
from utils.base.session import AsyncDatabase


class ServicesService(BaseService):
    model = Chapters



async def get_service_service(session=Depends(AsyncDatabase.get_session)):
    return ServicesService(session)


services_service: ServicesService = Depends(get_service_service)
