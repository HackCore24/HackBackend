from fastapi import Depends, HTTPException
from sqlalchemy import select

from utils.base.service import BaseService
from utils.base.session import AsyncDatabase
from api.project_budget.model import ProjectBudget


class BudgetService(BaseService):
    model = ProjectBudget

    async def project(self, project_id):
        return await self.session.scalar(select(ProjectBudget).where(ProjectBudget.project_id == project_id))


async def get_budget_service(session=Depends(AsyncDatabase.get_session)):
    return BudgetService(session)


budget_service: BudgetService = Depends(get_budget_service)
