from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException
from api.project.schema import ProjectCreate, ProjectUpdate, ProjectRead
from api.project.service import projects_service
from utils.base.authentication import get_me

project_router = APIRouter()


# Project endpoints
@project_router.post('/', name="Create Project", response_model=ProjectRead)
async def create_project(project: ProjectCreate, projects=projects_service, me=Depends(get_me)):
    return await projects.create_project(project)

@project_router.post('/relate', name="releate project")
async def releate_project(project_id: str, relate_project_id: str,projects=projects_service, me=Depends(get_me)):
    return await projects.create_relation(project_id, relate_project_id)

@project_router.get('/relate', name="get releate project")
async def releate_project(project_id: str,projects=projects_service, me=Depends(get_me)):
    return await projects.get_related_projects(project_id)

@project_router.get('/', name="Get All Projects", response_model=List[ProjectRead])
async def get_all_projects(projects=projects_service, me=Depends(get_me)):
    return await projects.all_projects()


@project_router.get('/{project_id}', name="Get Project By Id", response_model=ProjectRead)
async def get_project_by_id(project_id: str, projects=projects_service, me=Depends(get_me)):
    return await projects.project_by_id(project_id)


@project_router.patch('/{project_id}', response_model=ProjectRead)
async def update_project(project_id: str, project: ProjectUpdate, projects=projects_service, me=Depends(get_me)):
    return await projects.update_project(project_id, project.__dict__)
