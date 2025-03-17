from src.services.document_service.archiflow_document_service import ArchiflowDocumentService
from src.services.document_service.models.archiflow_request_models import ArchiflowDocumentServiceAuthenticationBody, ArchiflowConnectionInfo
from src.handlers.handler import DocumentHandler


class DocumentFetcher(DocumentHandler):
    def __init__(self, base_url):
        self.document_service = ArchiflowDocumentService(base_url)
        super().__init__()
        
    def handle(self, document):
        pass
    
    
    def obtain_session_id(self,credentials: dict, connection_info: ArchiflowConnectionInfo):
        authentication_request_body = ArchiflowDocumentServiceAuthenticationBody(strUser=credentials["USER"],
                                                                                 strPassword=credentials["PASSWORD"],
                                                                                 onConnectionInfo=connection_info)
        try:
            auth_response = self.document_service.authenticate(authentication_request_body)
            return auth_response.session_info.session_id
        except Exception as e:
            print(f"Error while authenticating: {e}")
            return None