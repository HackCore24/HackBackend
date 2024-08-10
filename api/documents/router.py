from typing import List, Optional
from urllib.parse import quote

from aiohttp.web_fileresponse import FileResponse
from fastapi import APIRouter, Depends, HTTPException, File, UploadFile
from starlette.responses import StreamingResponse

from api.documents.service import documents_service
from api.documents.schema import DocumentsRead, DocumentsCreate, DocumentsUpdate, InputVariables
from utils.base.authentication import get_me

document_router = APIRouter()


@document_router.post('/', name="Create Document", response_model=DocumentsRead)
async def create_document(document: DocumentsCreate, documents=documents_service, me=Depends(get_me)):
    return await documents.create(document.__dict__)


@document_router.post('/upload', name="Create Document by upload", response_model=DocumentsRead)
async def create_document(document: UploadFile = File(...), documents=documents_service, me=Depends(get_me)):
    return await documents.create_upload(document)


@document_router.post('/download', name="Download Document", response_model=DocumentsRead)
async def create_document(document_id: str, documents=documents_service, me=Depends(get_me)):
    document = await documents.id(document_id)
    document_link = await documents.convert_html_to_docx(html=document.html, filename=document.title)
    file_data = await documents.download_file(document_link)
    filename_utf8 = quote(f"{document.title}.docx")
    content_disposition = f'attachment; filename*=UTF-8\'\'{filename_utf8}'
    return StreamingResponse(file_data,
                             media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                             headers={"Content-Disposition": content_disposition})


@document_router.post('/generate', name="Download generate Document", response_model=DocumentsRead)
async def create_document(document_id: str, variables: List[InputVariables], documents=documents_service,
                          me=Depends(get_me)):
    document, html = await documents.generate(document_id, variables)
    document_link = await documents.convert_html_to_docx(html=html, filename=document.title)
    file_data = await documents.download_file(document_link)
    filename_utf8 = quote(f"{document.title}.docx")
    content_disposition = f'attachment; filename*=UTF-8\'\'{filename_utf8}'
    return StreamingResponse(file_data,
                             media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                             headers={"Content-Disposition": content_disposition})


@document_router.post('/relate', name="relation document and project")
async def releate_document(document_id: str, project_id: str, documents=documents_service, me=Depends(get_me)):
    return await documents.create_relation(document_id, project_id)


@document_router.get('/relate/{project_id}', name="get related documents by project_id")
async def releate_document(project_id: str, documents=documents_service, me=Depends(get_me)):
    return await documents.get_related_documents(project_id)


@document_router.get('/', name="Get All Documents", response_model=List[DocumentsRead])
async def get_all_documents(documents=documents_service, me=Depends(get_me)):
    return await documents.all()


@document_router.get('/{document_id}', name="Get Document By Id", response_model=DocumentsRead)
async def get_document_by_id(document_id: str, documents=documents_service, me=Depends(get_me)):
    return await documents.id(document_id)


@document_router.patch('/{document_id}', response_model=DocumentsRead)
async def update_document(document_id: str, document: DocumentsUpdate, documents=documents_service,
                          me=Depends(get_me)):
    return await documents.update(document_id, document.__dict__)
