from typing import List
from pydantic import BaseModel, Field, ConfigDict

from src.services.document_service.archiflow_document_service import DocumentService
from src.services.document_service.models.archiflow_request_models import RequestBody,ArchiflowDocumentServiceGetDocumentPDFBody, ArchiflowDocumentServiceGetDocumentsBody, Archive, DocumentType, FieldObj, SearchCriteria, SessionInfo, ParametersIn
from src.services.document_service.models.archiflow_response_models import ArchiflowDocumentServiceGetDocumentsResponse
from src.services.document_service.models.filter_model import DocumentTypeFilter, ArchiveFilter, Filter_IDs

from src.pipeline.pipeline import PipelineStep, PipelineInput

class ArchiflowFetcherPipelineInput(BaseModel, PipelineInput):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    credential: RequestBody = Field(alias="credential")
    filters: dict = Field(alias="filters")

    def to_json(self):
        return self.model_dump_json(by_alias=False)
    
class DocumentPDF(BaseModel):
    file_name: str = Field(alias="file_name")
    file_base64_string: str = Field(alias="file_base64_string")

class DocumentIntelligencePipelineInput(BaseModel, PipelineInput):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    document_pdf_files: List[DocumentPDF] = Field(alias="document_pdf_files")

    def to_json(self):
        return self.model_dump_json(by_alias=False)

class ArchiflowDocumentFetcherStep(PipelineStep):
    def __init__(self, document_service: DocumentService):
        self.document_service = document_service
        
    def process(self, data: PipelineInput):

        session_id = self.document_service.authenticate(data.credential).session_info.session_id
        get_document_list_request_object = self._build_get_document_list_request_object(data.filters, session_id)

        document_list = self.document_service.get_documents(get_document_list_request_object)
        document_files = self._retrieve_pdf_files(document_list, session_id)


        return DocumentIntelligencePipelineInput(document_pdf_files=document_files)
    
    
    def _build_get_document_list_request_object(self, filters: dict, session_id:str) -> ArchiflowDocumentServiceGetDocumentsBody:
        
        archive_object = self._get_archive_type_object(filters)
        document_type_object = self._get_document_type_object(filters)
        filter_field_list = self._get_filter_fields_list(filters)

        search_criteria = SearchCriteria(Archives=archive_object,
                                 DocumentType=document_type_object,
                                 Fields=filter_field_list)


        session_info = SessionInfo(SessionId=session_id)

        parametersIn = ParametersIn(SessionInfo=session_info,
                                    SearchCriteria=search_criteria,
                                    PageNumber=1,
                                    PageSize=10,
                                    GetIndexes=False,
                                    GetInvoice=False)


        archiflow_get_documents_request_body = ArchiflowDocumentServiceGetDocumentsBody(paramIn=parametersIn)

        return archiflow_get_documents_request_body


    
    def _get_archive_type_object(self,filters: dict) -> Archive:
        archive_type = filters["ARCHIVE_TYPE"]
        archive_type_id = ArchiveFilter[archive_type].value
        archive_object = [Archive(ArchiveId=archive_type_id)]

        return archive_object
    
    def _get_document_type_object(self, filters: dict) -> DocumentType:
        document_type = filters["DOCUMENT_TYPE"]
        document_type_id = DocumentTypeFilter[document_type].value
        document_type_object = DocumentType(DocumentTypeId=document_type_id)

        return document_type_object
    
    def _get_filter_fields_list(self, filters: dict) -> List[FieldObj]:

        filter_field_list = []
        for key, value in Filter_IDs.__members__.items():

            filter_value = filters[key]
            filter_key_id = value
            filter_field_obj = FieldObj(FieldId=filter_key_id, FieldValue=filter_value)

            filter_field_list.append(filter_field_obj)

        return filter_field_list
    

    def _retrieve_pdf_files(self, document_list: ArchiflowDocumentServiceGetDocumentsResponse, session_id: str):

        pdf_ids = [card.card_id for card in document_list.retrieve_cards_result.cards]

        base_64_string_pdf_list = []
        for pdf_id in pdf_ids:
            request_pdf_body = ArchiflowDocumentServiceGetDocumentPDFBody(strSessionId=session_id,
                                                                          oCardId=pdf_id,
                                                                          CardContentMode="4",
                                                                          nVersion="0",
                                                                          oWaterMark="")

            pdf_file_base_64 = self.document_service.get_document_pdf(request_pdf_body)

            base_64_string_pdf_list.append(DocumentPDF(file_name=pdf_file_base_64.document.original_file_name,
                                                       file_base64_string=pdf_file_base_64.document.content))
            #print(f"Base64 string: {pdf_file_base_64.document.content}")

        return base_64_string_pdf_list            