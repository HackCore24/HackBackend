from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException
from api.project_documentation.schema import DocumentationRead, DocumentationCreate, DocumentationUpdate
from api.project_documentation.service import documentation_service
from utils.base.authentication import get_me

documentation_router = APIRouter()


# documentation endpoints
@documentation_router.post('/', name="Create documentation", response_model=DocumentationRead)
async def create_documentation(documentation: DocumentationCreate, documentations=documentation_service,
                               me=Depends(get_me)):
    return await documentations.create(documentation.__dict__)


@documentation_router.get('/', name="Get All documentations", response_model=List[DocumentationRead])
async def get_all_documentations(documentations=documentation_service, me=Depends(get_me)):
    return await documentations.all()


@documentation_router.get('/project/{project_id}', name="Get Budget By project Id", response_model=List[DocumentationRead])
async def get_budget_by_id(project_id: str, documentations=documentation_service, me=Depends(get_me)):
    return await documentations.project(project_id)


@documentation_router.get('/{documentation_id}', name="Get documentation By Id", response_model=DocumentationRead)
async def get_documentation_by_id(documentation_id: str, documentations=documentation_service, me=Depends(get_me)):
    return await documentations.id(documentation_id)


@documentation_router.patch('/{documentation_id}', response_model=DocumentationRead)
async def update_documentation(documentation_id: str, documentation: DocumentationUpdate,
                               documentations=documentation_service, me=Depends(get_me)):
    return await documentations.update(documentation_id, documentation.__dict__)
