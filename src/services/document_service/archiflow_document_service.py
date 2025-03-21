from src.services.document_service.document_service import DocumentService
import requests
from src.services.document_service.models.archiflow_request_models import ArchiflowDocumentServiceAuthenticationBody, ArchiflowDocumentServiceGetDocumentsBody, ArchiflowDocumentServiceGetDocumentPDFBody
from src.services.document_service.models.archiflow_response_models import ArchiflowDocumentServiceGetDocumentsResponse, ArchiflowDocumentServiceGetDocumentPDFResponse, ArchiflowDocumentServiceAuthenticationResponse
import json

class ArchiflowDocumentService(DocumentService):
    def __init__(self, base_url):
        super().__init__(base_url)

    def get_documents(self, get_documents_body: ArchiflowDocumentServiceGetDocumentsBody):
        url = f"{self.base_url}/Card.svc/json/RetrieveCardsByParam"
        try:
            response = requests.post(url, json=json.loads(get_documents_body.model_dump_json(by_alias=True)))
        except Exception as e:
            print(f"Error: {e.message}")            
        return ArchiflowDocumentServiceGetDocumentsResponse.model_validate(response.json())

    def get_document_pdf(self, get_document_pdf_body: ArchiflowDocumentServiceGetDocumentPDFBody):
        url = f"{self.base_url}/Card.svc/json/GetCardDocument5"
        try:
            response = requests.post(url, json=json.loads(get_document_pdf_body.model_dump_json(by_alias=True)))
        except Exception as e:
            print(f"Error: {e.message}")            
        return ArchiflowDocumentServiceGetDocumentPDFResponse.model_validate(response.json())

    def authenticate(self, auth_body: ArchiflowDocumentServiceAuthenticationBody):
        url = f"{self.base_url}/Login.svc/json/Login"
        try:
            response = requests.post(url, json=json.loads(auth_body.model_dump_json(by_alias=True)))
        except Exception as e:
            print(f"Error: {e.message}")
        return ArchiflowDocumentServiceAuthenticationResponse.model_validate(response.json())