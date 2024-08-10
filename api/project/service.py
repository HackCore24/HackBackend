from datetime import datetime

from fastapi import Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import selectinload, noload

from api.project.schema import ProjectUpdate, ProjectRead, ProjectCreate
from api.users.model import Users
from utils.base.config import settings
from utils.base.service import BaseService
from utils.base.session import AsyncDatabase
from api.project.model import Projects, RelatedProject


class ProjectService(BaseService):
    model = Projects

    async def create_project(self, project_data: ProjectCreate):
        project = Projects(**project_data.__dict__)
        self.session.add(project)
        await self.session.commit()
        return project

    async def all_projects(self):
        query = select(Projects)
        projects = (await self.session.scalars(query)).all()
        if not projects:
            raise HTTPException(404, "not found")
        return projects

    async def project_by_id(self, project_id):
        query = select(Projects).where(Projects.id == project_id)
        project = await self.session.scalar(query)
        if not project:
            raise HTTPException(404, "not found")
        return project

    async def update_project(self, project_id, project_data):
        project = await self.session.get(Projects, project_id)
        for key, value in project_data.items():
            if value is not None:
                attr_value = getattr(project, key)
                attr_value = attr_value.lower() if isinstance(attr_value, str) else attr_value
                validate_value = value.lower() if isinstance(value, str) else value
                if attr_value == validate_value:
                    continue
                else:
                    setattr(project, key, value)
        project.updated_at = datetime.utcnow()
        await self.session.commit()
        return project

    async def create_relation(self, project_id, relate_project_id):
        project = await self.session.get(Projects, project_id)
        if not project:
            raise HTTPException(404, "project not found")
        relate_project = await self.session.get(Projects, relate_project_id)
        if not relate_project:
            raise HTTPException(404, "relate project not found")
        relate = RelatedProject(project_id=project_id, related_project_id=relate_project_id)
        self.session.add(relate)
        await self.session.commit()
        return relate

    async def get_related_projects(self, project_id):
        related_projects = await self.session.scalars(
            select(Projects)
            .join(RelatedProject, Projects.id == RelatedProject.related_project_id)
            .where(RelatedProject.project_id == project_id)
        )

        return related_projects.all()

    async def all_my_projects(self, user):
        query = select(Projects).where(Projects.creator_id == user.id)
        return (await self.session.scalars(query)).all()


async def get_project_service(session=Depends(AsyncDatabase.get_session)):
    return ProjectService(session)


projects_service: ProjectService = Depends(get_project_service)
