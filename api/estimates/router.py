from typing import List, Optional
from fastapi import APIRouter, Depends
from api.estimates.service import services_service
from api.estimates.schema import ServiceRead, ServiceCreate, ServiceUpdate, ChapterCreate, ChapterRead, ChapterUpdate
from utils.base.authentication import get_me

estimates_router = APIRouter()


@estimates_router.post('/chapter/', name="Create chapter", response_model=ChapterRead)
async def create_service(chapter: ChapterCreate, services=services_service, me=Depends(get_me)):
    return await services.create(chapter.__dict__)


@estimates_router.get('/chapter/', name="Get All chapters", response_model=List[ChapterRead])
async def get_all_services(services=services_service, me=Depends(get_me)):
    return await services.all()


@estimates_router.get('/chapter/{chapter_id}', name="Get chapter By id", response_model=ChapterRead)
async def get_service_by_id(chapter_id: str, services=services_service, me=Depends(get_me)):
    return await services.id(chapter_id)


@estimates_router.patch('/chapter/{chapter_id}', name="Update chapter", response_model=ChapterRead)
async def update_service(chapter_id: str, chapter: ChapterUpdate, services=services_service, me=Depends(get_me)):
    return await services.update(chapter_id, chapter.__dict__)


@estimates_router.post('/service/', name="Create service", response_model=ServiceRead)
async def create_service(service: ServiceCreate, services=services_service, me=Depends(get_me)):
    return await services.create_service(service.__dict__)


@estimates_router.get('/service/', name="Get All services", response_model=List[ServiceRead])
async def get_all_services(services=services_service, me=Depends(get_me)):
    return await services.all_services()


@estimates_router.get('/service/chapter/{chapter_id}', name="Get services By chapter id",
                      response_model=List[ServiceRead])
async def get_service_by_id(chapter_id: str, services=services_service, me=Depends(get_me)):
    return await services.chapter(chapter_id)


@estimates_router.get('/service/{service_id}', name="Get service By id", response_model=ServiceRead)
async def get_service_by_id(service_id: str, services=services_service, me=Depends(get_me)):
    return await services.service_id(service_id)


@estimates_router.patch('/service/{service_id}', name="update service", response_model=ServiceRead)
async def update_service(service_id: str, service: ServiceUpdate, services=services_service, me=Depends(get_me)):
    return await services.update_service(service_id, service.__dict__)


@estimates_router.post('/estimates/generate', name="Generate estimate")
async def generate_estimate(project_id: str, services=services_service, me=Depends(get_me)):
    return await services.generate_estimate(project_id)
