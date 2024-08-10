from typing import List, Optional
from urllib.parse import quote

from aiohttp.web_fileresponse import FileResponse
from fastapi import APIRouter, Depends, HTTPException, File, UploadFile
from starlette.responses import StreamingResponse

from api.services.service import services_service
from api.services.schema import ServiceRead, ServiceCreate, ServiceUpdate, ChapterCreate, ChapterRead, ChapterUpdate
from utils.base.authentication import get_me

service_router = APIRouter()


@service_router.post('/chapter/', name="Create chapter", response_model=ChapterRead)
async def create_service(chapter: ChapterCreate, services=services_service, me=Depends(get_me)):
    return await services.create(chapter.__dict__)


@service_router.get('/chapter/', name="Get All chapters", response_model=List[ChapterRead])
async def get_all_services(services=services_service, me=Depends(get_me)):
    return await services.all()


@service_router.get('/chapter/{chapter_id}', name="Get chapter By id", response_model=ChapterRead)
async def get_service_by_id(chapter_id: str, services=services_service, me=Depends(get_me)):
    return await services.id(chapter_id)


@service_router.patch('/chapter/{chapter_id}', response_model=ChapterRead)
async def update_service(chapter_id: str, chapter: ChapterUpdate, services=services_service, me=Depends(get_me)):
    return await services.update(chapter_id, chapter.__dict__)


@service_router.post('/service/', name="Create chapter", response_model=ServiceRead)
async def create_service(service: ChapterCreate, services=services_service, me=Depends(get_me)):
    return await services.create_service(service.__dict__)


@service_router.get('/service/', name="Get All chapters", response_model=List[ServiceRead])
async def get_all_services(services=services_service, me=Depends(get_me)):
    return await services.all_services()


@service_router.get('/service/chpater/{chapter_id}', name="Get chapter By id", response_model=ServiceRead)
async def get_service_by_id(chapter_id: str, services=services_service, me=Depends(get_me)):
    return await services.chapter(chapter_id)


@service_router.get('/service/{service_id}', name="Get chapter By id", response_model=ServiceRead)
async def get_service_by_id(service_id: str, services=services_service, me=Depends(get_me)):
    return await services.service_id(service_id)


@service_router.patch('/service/{service_id}', response_model=ServiceRead)
async def update_service(service_id: str, service: ServiceCreate, services=services_service, me=Depends(get_me)):
    return await services.update_service(service_id, service.__dict__)
