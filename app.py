import base64

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
    api = "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJhdWQiOiIxIiwianRpIjoiYzU1ZGY2NGM3MjUwOGE5NGNkYWQ2ZGMwMzJjMmRhZGI4NGZiYmVmNTcyOTY3YTQyMjRjNjRmZDc1NDEwZWNjOWMwYjMyNjhiZDUwY2FlNGQiLCJpYXQiOjE3MjMyNTM1NjMuNjU1Nzg1LCJuYmYiOjE3MjMyNTM1NjMuNjU1Nzg2LCJleHAiOjQ4Nzg5MjcxNjMuNjUyMzY1LCJzdWIiOiI2OTI0MDU1MiIsInNjb3BlcyI6WyJ0YXNrLnJlYWQiLCJ0YXNrLndyaXRlIl19.OKafN0_m99t6pFEyyR11j_aEZfqD4D4v57IqZWvQ9Yh1pj3BjUWFYXn-FU-gbnlc2hgb6h3Z6brHNOdJTIMvnWmihL7bYb0TOiiudBO3NE5_TS11KWNKMxM9w5j17zXWTEj2rh_tXNdu_neSiEnhBfXGXyWEcclVnpzn1C3PAHy6sKb5aEyv3V2fKHdvsfg1nh7siJf-tnqHiU83NpXSJDz7xQ_vO__pK_Dhtfeil7AJvj2MB1knWn0jKNu-fawcwdO6NpS2ayuUGiMIvhagfP6UuHAfdpb5nW8n60WU2uaXolv7octKTZprFKppIfjx7H6uVWsWkgP5hgYeM7mEsONbV6WYgNXVXoD5MPNZ8K0f6w8OKar5bJTE6tjWME2zHqxTgR01gl27Hj7-30gOjg13s-CpOSsclvPp0V93X-nkSRqtx1qdUXb6DdMLnkvaXSDRTjRWbD48yVLQqjRNLVsRMFJ2spMW6kPgdksqTrD5pa4BW2A2cfyOuybVOboYmcQcZwnPYSWERt3o31OAdWf5zQMZo1azGiPKBxVUXW9p0PxwFLHZDuHV9pPtLZTbL-DfW7g5dgd48y5Hm9YBSuu1FpAvdGTBgE3dH0P86EENHPYT5zfAlE2y9yTnj-oW2kQsjzr9xJEBYKQ4_YhPqviE0iOtIEm0skdGt4H_ZxY"
    cloudconvert.configure(api_key=api, sandbox=False)
    uvicorn.run("app:app", host='0.0.0.0', port=8000, reload=False)
