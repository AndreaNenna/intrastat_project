from src.services.document_service.document_service import DocumentService
import requests
from src.services.document_service.models.archiflow_request_models import ArchiflowDocumentServiceAuthenticationBody, ArchiflowDocumentServiceGetDocumentsBody, ArchiflowDocumentServiceGetDocumentPDFBody
from src.services.document_service.models.archiflow_response_models import ArchiflowDocumentServiceGetDocumentsResponse, ArchiflowDocumentServiceGetDocumentPDFResponse, ArchiflowDocumentServiceAuthenticationResponse


class ArchiflowDocumentService(DocumentService):
    def __init__(self, base_url):
        super().__init__(base_url)

    def get_documents(self, get_documents_body: ArchiflowDocumentServiceGetDocumentsBody):
        url = f"{self.base_url}/Card.svc/json/RetrieveCardsByParam"
        response = requests.post(url, json=get_documents_body.json())
        return ArchiflowDocumentServiceGetDocumentsResponse(response.json())

    def get_document_pdf(self, get_document_pdf_body: ArchiflowDocumentServiceGetDocumentPDFBody):
        url = f"{self.base_url}/Card.svc/json/GetCardDocument5"
        response = requests.post(url, json=get_document_pdf_body.json())
        return ArchiflowDocumentServiceGetDocumentPDFResponse(response.json())

    def authenticate(self, auth_body: ArchiflowDocumentServiceAuthenticationBody):
        url = f"{self.base_url}/Login.svc/json/Login"
        response = requests.post(url, json=auth_body.json())
        return ArchiflowDocumentServiceAuthenticationResponse(response.json())