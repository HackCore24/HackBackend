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
    uvicorn.run("app:app", host='0.0.0.0', port=8000, reload=False)
