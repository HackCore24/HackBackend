import base64
import random

import cloudconvert
import uvicorn
from fastapi import FastAPI, APIRouter
from starlette.middleware.cors import CORSMiddleware

from api.api_router import api_router
from utils.base.config import settings
from utils.middlewares.api_doc_auth_middleware import ApidocBasicAuthMiddleware

app = FastAPI(title="HackBackend API",
              docs_url='/api/docs',
              openapi_url='/api/openapi.json',
              redoc_url='/api/redoc',
              swagger_ui_parameters={
                  'docExpansion': 'none',
                  'persistAuthorization': 'true',
                  'defaultModelRendering': 'model'
              })
app.add_middleware(ApidocBasicAuthMiddleware)

origins = ["http://localhost:3000", "http://localhost:5500", "https://24core.ru"]

app.add_middleware(CORSMiddleware, allow_origins=origins, allow_credentials=True, allow_methods=["*", "OPTIONS"],
                   allow_headers=["*"], max_age=3600)

router = APIRouter()

router.include_router(router=api_router)



@router.get("/ping", tags=["Server"])
async def ping_server():
    return "pong"


app.include_router(router, prefix='/api/v1')

if __name__ == "__main__":
    api_key = "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJhdWQiOiIxIiwianRpIjoiMzgxMWI0OWJjMzcxN2U0MGRjOTEwM2E2MDcxYmZhMzliNjYzZWRkNGYxNGEyNjUwZjQxMGY2OGJkNWY3YmFjYmY2ZWQyMjM0YzcxYWY3NjAiLCJpYXQiOjE3MjMzNzI4OTUuNjA0NzQzLCJuYmYiOjE3MjMzNzI4OTUuNjA0NzQ0LCJleHAiOjQ4NzkwNDY0OTUuNjAxNjY5LCJzdWIiOiI2OTI0MDU1MiIsInNjb3BlcyI6WyJ0YXNrLnJlYWQiLCJ0YXNrLndyaXRlIiwidXNlci5yZWFkIiwidXNlci53cml0ZSIsIndlYmhvb2sucmVhZCIsIndlYmhvb2sud3JpdGUiLCJwcmVzZXQucmVhZCIsInByZXNldC53cml0ZSJdfQ.jhYfBr-kPejUr0PfQX2EQAkemnYeFlH1olzgvupxmduhferpWykDniUGE-dLZmAiwBtkkUjHqZyCEIGqzd5E4Syx-mFVqWkcP9JIAkGZAPp6en7BWrNqm7nU-ptUmS1h7OqXCtD2fRA1VpbTb7JhCH2-b2IIE5dXyyVofFOZUUpj7U1N_Oz9waNZXaxTjKX_jfmti-nCdYJBksCsmHTZ58_J_djXbaqkOfugZqIFBLbxu6VwdjyPE4pPpU9120dSIoDEaIogT3aMB9wfj2syEuu1eGZPDmv1WG6nCi9Uh2_14KagZmygypmenQ7gVEABnkv0s6PhtEGVKhW3QZB9iC7xOuqldlus-wSKvdMUmJDRTeOGtIs0eb5xfONN789F9awduKGQzgQO7ftffVO9YOjEiKucaQydJPI6LPqx5D1idzscrtp7gFhrk7ddAE6JzXmwQsnVODB7CYsD1phzwOasi_A_rKhbJcgeWW0dpiD7KHb6DsKpEFkBmnLuaMSJpPiPgwHlD0beyiH4Z0it62XxCxNPJd7A1WWpAGI4z4g78-9jee6YTsE8paZi4-9N3Xlyz9WVfdrMXBdp50ReY8HWelAd452pdvF4_lGc63FtPP8bQgug5ri39uREAqdG0fvU8xl0F7Xni0m4OB6W9kjwDow99c3E98MN32ldMrc"
    cloudconvert.configure(api_key=api_key, sandbox=False)
    uvicorn.run("app:app", host='0.0.0.0', port=8000, reload=False)
