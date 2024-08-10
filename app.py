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

origins = ["http://localhost:3000", "http://localhost:5500"]

app.add_middleware(CORSMiddleware, allow_origins=origins, allow_credentials=True, allow_methods=["*", "OPTIONS"],
                   allow_headers=["*"], max_age=3600)

router = APIRouter()

router.include_router(router=api_router)


@router.get("/ping", tags=["Server"])
async def ping_server():
    return "pong"


app.include_router(router, prefix='/api/v1')

if __name__ == "__main__":
    api_key = "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJhdWQiOiIxIiwianRpIjoiZDk4YzM0NmFhNmNkZGNkZjVhYjZhZTRjNDc0ZmM4MzM5YjBhODQwMDdiZTBlYTdmMzlmZDkyMmY4YWU3YzJmODk0OTE5NTE0NWZhMjNhNWUiLCJpYXQiOjE3MjMyODY0NTIuNzE4MTU2LCJuYmYiOjE3MjMyODY0NTIuNzE4MTU3LCJleHAiOjQ4Nzg5NjAwNTIuNzEzNjEzLCJzdWIiOiIzMzE3MDE5NCIsInNjb3BlcyI6WyJ0YXNrLndyaXRlIiwidGFzay5yZWFkIiwid2ViaG9vay5yZWFkIiwid2ViaG9vay53cml0ZSIsInVzZXIucmVhZCJdfQ.Km8Aq8SnElpQ__po62ES0urPzRoEckhZ9Lnw2Aouqm7pN72YK6tjhmBv1bNbC-OXT9f05xI8_3B-NI8UdTZwoshduiWD472svugg68Htm1cTM1l8lQphYGMSgG39AAL9cbtfb6d73S173eMnqW4g34l2EF3Z21lu6-Ej9_THml4JjccYnzixhEP1iSFYZKBiDjcEvgWKviR9hi1krmCOPCHbNCNUsaasP_yJw0JthOm1lxLhhbCPuebvztaAsX2mTmOfMnF3_T09vGHcDOPNfJwhp5i3l5I5A_mgKXDU5g260geZdKoH2WaOfaMyq1y39VLk6I92tq8-iNuYrqi7ffvW2SJj8gHRoDMFImZkrOemqe-O0lSi5Nd5E1V3troewxUvSYXv4FTgskrziip5EBAoOB7V4d-OJxTYvN-ecfB_DaZFOy4idQXdqUIfF2adWGVMo3TV87KWaK0-ChDyQKo24G8TPMDZIzz_HBjmHM6wONyls1sCAy5hbMECSFyfMoz1l8pp8ndy-goVMMJvbHlrtyS8FiNB8DtHnhZEvh5Bsj8c7i8dlCJ7TeCBHDyBC8KYZdEASdpjKhSFpwhzleL1BzgafgYFeuDehqTFLp8Cdkq9Hi7DFoumEqtiMYtm6u2Ye2zMw6hipMgLfzOkbzUvbxidvvuGFUOVY_o_nRI"
    cloudconvert.configure(api_key=api_key, sandbox=False)
    uvicorn.run("app:app", host='0.0.0.0', port=8000, reload=False)
