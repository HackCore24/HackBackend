from datetime import datetime

from fastapi import Depends, HTTPException
from sqlalchemy import select

from api.variables.model import Variables
from utils.base.service import BaseService
from utils.base.session import AsyncDatabase


class VariablesService(BaseService):
    model = Variables

    async def document(self, document_id):
        return (await self.session.scalars(select(Variables).where(Variables.document_id == document_id))).all()


async def get_variables_service(session=Depends(AsyncDatabase.get_session)):
    return VariablesService(session)


variables_service: VariablesService = Depends(get_variables_service)
