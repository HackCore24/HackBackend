from datetime import datetime

from fastapi import Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import selectinload, noload

from api.project.model import Projects
from services.telegram import TelegramAPI
from utils.base.service import BaseService
from utils.base.session import AsyncDatabase
from api.project_statuses.model import ProjectStatuses, ProjectStatusReach


class ProjectStatusesService(BaseService):
    model = ProjectStatuses

    async def change_status(self, status_id, project_id, user):
        project = await self.session.get(Projects, project_id)
        if not project:
            raise HTTPException(404, "project not found")
        status = await self.session.get(ProjectStatuses, status_id)
        if not status:
            raise HTTPException(404, "status not found")

        status_reach = ProjectStatusReach(status_id=status_id, project_id=project_id, date_reach=datetime.now())
        self.session.add(status_reach)
        await self.session.commit()

        message = f'''НОВОЕ СОБЫТИЕ ⭐️

Акт #1523 успешно подписан    

Проект "{project.title}" успешно завершен ✅

Проект принял: {user.firstname} {user.lastname}'''
        await TelegramAPI().send_message(user_id=user.telegram_id, message=message, project_id=project_id)
        return status_reach

    async def project(self, project_id):
        statuses = (await self.session.scalars(select(ProjectStatuses).order_by(ProjectStatuses.order))).all()
        reached = (await self.session.scalars(
            select(ProjectStatusReach).where(ProjectStatusReach.project_id == project_id))).all()

        reached_dict = {record.status_id: record.date_reach for record in reached}

        status_with_info = []
        for status in statuses:
            status_info = {
                "id": status.id,
                "title": status.title,
                "order": status.order,
                "is_passed": status.id in reached_dict,
                "date_reach": reached_dict.get(status.id)
            }
            status_with_info.append(status_info)

        return status_with_info


async def get_project_statuses_service(session=Depends(AsyncDatabase.get_session)):
    return ProjectStatusesService(session)


projects_statuses_service: ProjectStatusesService = Depends(get_project_statuses_service)
