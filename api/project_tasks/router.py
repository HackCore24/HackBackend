from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException
from api.project_tasks.schema import TasksCreate, TasksUpdate, TasksRead
from api.project_tasks.service import tasks_service
from utils.base.authentication import get_me

tasks_router = APIRouter()


@tasks_router.post('/', name="Create Tasks", response_model=TasksRead)
async def create_task(task: TasksCreate, tasks=tasks_service, me=Depends(get_me)):
    return await tasks.create(task.__dict__)


@tasks_router.get('/', name="Get All Taskss", response_model=List[TasksRead])
async def get_all_tasks(tasks=tasks_service, me=Depends(get_me)):
    return await tasks.all()


@tasks_router.get('/project/{project_id}', name="Get Tasks By project Id", response_model=List[TasksRead])
async def get_task_by_project_id(project_id: str, tasks=tasks_service, me=Depends(get_me)):
    return await tasks.project(project_id)


@tasks_router.get('/{task_id}', name="Get Tasks By Id", response_model=TasksRead)
async def get_task_by_id(task_id: str, tasks=tasks_service, me=Depends(get_me)):
    return await tasks.id(task_id)


@tasks_router.patch('/{task_id}', response_model=TasksRead)
async def update_task(task_id: str, task: TasksUpdate, tasks=tasks_service, me=Depends(get_me)):
    return await tasks.update(task_id, task.__dict__)
