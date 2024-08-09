from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException
from api.project_budget.schema import BudgetCreate, BudgetBase, BudgetRead, BudgetUpdate
from api.project_budget.service import budget_service
from utils.base.authentication import get_me

budget_router = APIRouter()


# Budget endpoints
@budget_router.post('/', name="Create Budget", response_model=BudgetRead)
async def create_budget(budget: BudgetCreate, budgets=budget_service, me=Depends(get_me)):
    return await budgets.create(budget.__dict__)


@budget_router.get('/', name="Get All Budgets", response_model=List[BudgetRead])
async def get_all_budgets(budgets=budget_service, me=Depends(get_me)):
    return await budgets.all()


@budget_router.get('/{budget_id}', name="Get Budget By Id", response_model=BudgetRead)
async def get_budget_by_id(budget_id: str, budgets=budget_service, me=Depends(get_me)):
    return await budgets.id(budget_id)


@budget_router.get('/project/{project_id}', name="Get Budget By project Id", response_model=BudgetRead)
async def get_budget_by_id(project_id: str, budgets=budget_service, me=Depends(get_me)):
    return await budgets.project(project_id)

@budget_router.patch('/{budget_id}', response_model=BudgetRead)
async def update_budget(budget_id: str, budget: BudgetUpdate, budgets=budget_service, me=Depends(get_me)):
    return await budgets.update(budget_id, budget.__dict__)
