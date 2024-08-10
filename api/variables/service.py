from datetime import datetime
from fastapi import Depends, HTTPException
from sqlalchemy import select
from api.variables.model import Variables
from api.variables.schema import VariablesCreate
from utils.base.service import BaseService
from utils.base.session import AsyncDatabase
from slugify import slugify

class VariablesService(BaseService):
    model = Variables

    async def document(self, document_id):
        return (await self.session.scalars(select(Variables).where(Variables.document_id == document_id))).all()

    async def create_variable(self, variable_data: VariablesCreate):
        if variable_data.key is None:
            variable_data.key = slugify(variable_data.title)
        var = Variables(**variable_data.__dict__)
        self.session.add(var)
        await self.session.commit()
        return var


async def get_variables_service(session=Depends(AsyncDatabase.get_session)):
    return VariablesService(session)


variables_service: VariablesService = Depends(get_variables_service)
