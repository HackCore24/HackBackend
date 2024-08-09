from datetime import datetime

from fastapi import Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import selectinload, noload

from api.project.schema import ProjectUpdate, ProjectRead, ProjectCreate
from api.project_tasks.model import ProjectTasks
from api.users.model import Users
from utils.base.config import settings
from utils.base.service import BaseService
from utils.base.session import AsyncDatabase
from api.project.model import Projects, RelatedProject


class ProjectTasksService(BaseService):
    model = ProjectTasks

    async def project(self, project_id):
        query = select(ProjectTasks).where(ProjectTasks.project_id == project_id).order_by(ProjectTasks.deadline.desc())
        return (await self.session.scalars(query)).all()


async def get_tasks_service(session=Depends(AsyncDatabase.get_session)):
    return ProjectTasksService(session)


tasks_service: ProjectTasksService = Depends(get_tasks_service)
