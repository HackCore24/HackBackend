import base64
from io import BytesIO
import aiohttp
import cloudconvert
from fastapi import Depends, HTTPException, UploadFile
from jinja2 import Template
from sqlalchemy import select
from api.documents.model import Documents, DocumentsProjects
from utils.base.service import BaseService
from utils.base.session import AsyncDatabase
from api.project.model import Projects


class DocumentsService(BaseService):
    model = Documents

    async def fetch_file(self, url: str):
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    file_content = await response.read()
                    return file_content
                else:
                    raise Exception(f"Failed to fetch the file, status code: {response.status}")

    async def create_upload(self, document: UploadFile):
        filename = document.filename.split('.')[0]
        file = await document.read()
        base64_encoded_file = base64.b64encode(file).decode('utf-8')
        job = cloudconvert.Job.create(payload={
            "tasks": {
                "import": {
                    "operation": "import/base64",
                    "file": f"{base64_encoded_file}",
                    "filename": document.filename
                },
                "convert": {
                    "operation": "convert",
                    "input_format": "docx",
                    "output_format": "html",
                    "engine": "office",
                    "input": [
                        "import"
                    ],
                    "engine_version": "2.1"
                },
                "export": {
                    "operation": "export/url",
                    "input": [
                        "convert"
                    ],
                    "inline": False,
                    "archive_multiple_files": False
                }
            }
        })
        job_id = job['tasks'][-1]['id']
        convert_result = cloudconvert.Task.wait(job_id)
        convert_result_link = convert_result['result']['files'][0]['url']
        html_file_bytes = await self.fetch_file(convert_result_link)
        html_file = html_file_bytes.decode('utf-8')
        doc = Documents(html=html_file, filename=f"{filename}.html", title=filename)
        self.session.add(doc)
        await self.session.commit()
        return doc

    async def convert_html_to_docx(self, html, filename):
        byte_doc = html.encode('utf-8')
        base64_bytes = base64.b64encode(byte_doc)
        base64_string = base64_bytes.decode('utf-8')

        job = cloudconvert.Job.create(payload={
            "tasks": {
                "import": {
                    "operation": "import/base64",
                    "file": f"{base64_string}",
                    "filename": f"{filename}.html"
                },
                "convert": {
                    "operation": "convert",
                    "input_format": "html",
                    "output_format": "docx",
                    "engine": "office",
                    "input": [
                        "import"
                    ],
                    "embed_images": False,
                    "engine_version": "2.1"
                },
                "export": {
                    "operation": "export/url",
                    "input": [
                        "convert"
                    ],
                    "inline": False,
                    "archive_multiple_files": False
                }
            }
        })
        job_id = job['tasks'][-1]['id']
        convert_result = cloudconvert.Task.wait(job_id)
        convert_result_link = convert_result['result']['files'][0]['url']
        return convert_result_link

    async def download_file(self, url: str) -> BytesIO:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status != 200:
                    raise HTTPException(404, "File not found")
                file_data = await response.read()
                return BytesIO(file_data)

    async def create_relation(self, document_id, project_id):
        doc = await self.session.get(Documents, document_id)
        if not doc:
            raise HTTPException(404, "not found")
        project = await self.session.get(Projects, project_id)
        if not project:
            raise HTTPException(404, "not found")

        relation = DocumentsProjects(document_id=document_id, project_id=project_id)
        self.session.add(relation)
        await self.session.commit()
        return relation

    async def get_related_documents(self, project_id):
        related_docs = await self.session.scalars(
            select(Documents)
            .join(DocumentsProjects, Projects.id == DocumentsProjects.project_id)
            .where(DocumentsProjects.project_id == project_id)
        )

        return related_docs.all()

    async def generate(self, document_id, variables):
        document = await self.session.get(Documents, document_id)
        format_variables = {}
        for var in variables:
            format_variables[var.key] = var.input
        template = Template(document.html)
        html = template.render(format_variables)
        return document, html


async def get_documents_service(session=Depends(AsyncDatabase.get_session)):
    return DocumentsService(session)


documents_service: DocumentsService = Depends(get_documents_service)
