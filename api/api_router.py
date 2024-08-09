from fastapi import APIRouter

from api.project.router import project_router
from api.project_budget.router import budget_router
from api.project_documentation.router import documentation_router
from api.project_statuses.router import status_router
from api.project_tasks.router import tasks_router
from api.users.auth_router import auth_router
from api.users.users_router import users_router

api_router = APIRouter()

api_router.include_router(auth_router, tags=['Auth'], prefix='/auth')
api_router.include_router(users_router, tags=['Users'], prefix='/users')
api_router.include_router(project_router, tags=['Projects'], prefix='/projects')
api_router.include_router(budget_router, tags=['Project Budget'], prefix='/project_budget')
api_router.include_router(documentation_router, tags=['Project Documentation'], prefix='/project_documentation')
api_router.include_router(status_router, tags=['Project Statuses'], prefix='/project_statuses')
api_router.include_router(tasks_router, tags=['Project Tasks'], prefix='/project_tasks')
