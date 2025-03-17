from abc import ABC, abstractmethod
from pydantic import BaseModel, Field
from typing import List

class RequestBody(ABC):
    @abstractmethod
    def to_json(self):
        pass


    
class ArchiflowConnectionInfo(BaseModel):
    language: str = Field(alias="Language")
    date_format: str = Field(alias="DateFormat")
    workflow_domain: str = Field(alias="WorkflowDomain")
    
class ArchiflowDocumentServiceAuthenticationBody(BaseModel, RequestBody):
    str_user: str = Field(alias="strUser")
    str_password: str = Field(alias="strPassword")
    on_connection_info: ArchiflowConnectionInfo = Field(alias="onConnectionInfo")
    
    def to_json(self):
        return self.json(by_alias=True)




class SessionInfo(BaseModel):
    session_id: str = Field(alias="SessionId")
    
class Archive(BaseModel):
    archive_id: str = Field(alias="ArchiveId")
    
class DocumentType(BaseModel):
    document_type_id: str = Field(alias="DocumentTypeId")

class FieldObj(BaseModel):
    field_id: str = Field(alias="FieldId")
    field_value: str = Field(alias="FieldValue")
    
class SearchCriteria(BaseModel):
    archives: List[Archive] = Field(alias="Archives")     
    document_type: DocumentType = Field(alias="DocumentType")
    fields: List[FieldObj] = Field(alias="Fields")

class ParametersIn(BaseModel):
    session_info: SessionInfo = Field(alias="SessionInfo")
    search_criteria: SearchCriteria = Field(alias="SearchCriteria")
    page_number: int = Field(alias="PageNumber")
    page_size: int = Field(alias="PageSize")
    get_indexes: bool = Field(alias="GetIndexes")
    get_invoice: bool = Field(alias="GetInvoice")
    
class ArchiflowDocumentServiceGetDocumentsBody(BaseModel, RequestBody):
    param_in: ParametersIn
    
    def to_json(self):
        return self.json(by_alias=True)




class ArchiflowDocumentServiceGetDocumentPDFBody(BaseModel, RequestBody):
    str_session_id: str = Field(alias="strSessionId")
    o_card_id: str = Field(alias="oCardId")
    card_content_mode: str = Field(alias="cardContentMode")
    n_version: str = Field(alias="nVersion")
    o_water_mark: str = Field(alias="oWaterMark")
    
    def to_json(self):
        return self.json(by_alias=True)