from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException

from api.project_statuses.schema import StatusUpdate, StatusRead, StatusCreate
from api.project_statuses.service import projects_statuses_service
from utils.base.authentication import get_me

status_router = APIRouter()


@status_router.post('/', name="Create Status", response_model=StatusRead)
async def create_status(status: StatusCreate, statuses=projects_statuses_service, me=Depends(get_me)):
    return await statuses.create(status.__dict__)


@status_router.get('/', name="Get All Boards", response_model=List[StatusRead])
async def get_all_statuses(statuses=projects_statuses_service, me=Depends(get_me)):
    return await statuses.all()


@status_router.patch('/{status_id}', response_model=StatusRead)
async def update_status(status_id: str, status: StatusUpdate, statuses=projects_statuses_service, me=Depends(get_me)):
    return await statuses.update(status_id, status.__dict__)


@status_router.post('/reach/{status_id}/{project_id}', name="Project check status")
async def project_change_status(status_id: str, project_id: str, statuses=projects_statuses_service,
                                me=Depends(get_me)):
    return await statuses.change_status(status_id, project_id, user=me)


@status_router.get('/project/{project_id}', name="get project statuses")
async def project_get_statuses(project_id: str, statuses=projects_statuses_service, me=Depends(get_me)):
    return await statuses.project(project_id)
