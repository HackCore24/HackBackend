from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException
from api.variables.schema import VariablesUpdate, VariablesRead, VariablesCreate
from api.variables.service import variables_service
from utils.base.authentication import get_me

variable_router = APIRouter()


@variable_router.post('/', name="Create Variable", response_model=VariablesRead)
async def create_variable(variable: VariablesCreate, variables=variables_service, me=Depends(get_me)):
    return await variables.create(variable.__dict__)


@variable_router.get('/', name="Get All Variables", response_model=List[VariablesRead])
async def get_all_variables(variables=variables_service, me=Depends(get_me)):
    return await variables.all()


@variable_router.get('/{variable_id}', name="Get Variable By Id", response_model=VariablesRead)
async def get_variable_by_id(variable_id: str, variables=variables_service, me=Depends(get_me)):
    return await variables.id(variable_id)


@variable_router.get('/document/{document_id}', name="Get Variable By Id", response_model=VariablesRead)
async def get_variable_by_id(document_id: str, variables=variables_service, me=Depends(get_me)):
    return await variables.document(document_id)


@variable_router.patch('/{variable_id}', response_model=VariablesRead)
async def update_variable(variable_id: str, variable: VariablesUpdate, variables=variables_service, me=Depends(get_me)):
    return await variables.update(variable_id, variable.__dict__)
