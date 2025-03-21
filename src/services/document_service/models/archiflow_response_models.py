from abc import ABC, abstractmethod
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

class Response(ABC):
    @abstractmethod
    def to_json(self):
        pass
    
    

class SessionInfo(BaseModel):
    character_set: int = Field(alias="CharacterSet")
    client_type: int = Field(alias="ClientType")
    date_format: str = Field(alias="DateFormat")
    executive_office_code: int = Field(alias="ExecutiveOfficeCode")
    executive_offices: List = Field(alias="ExecutiveOffices")
    language: int = Field(alias="Language")
    login_ticket_user_id: Optional[str] = Field(default=None, alias="LoginTicketUserId")
    login_type: int = Field(alias="LoginType")
    session_id: str = Field(alias="SessionId")
    token_sess: Optional[str] = Field(default=None, alias="TokenSess")
    velocis_database: str = Field(alias="VelocisDatabase")
    velocis_server: str = Field(alias="VelocisServer")
    workflow_id: str = Field(alias="WorkflowId")

class ArchiflowDocumentServiceAuthenticationResponse(BaseModel, Response):
    login_result: int = Field(alias="LoginResult")
    session_info: SessionInfo = Field(alias="oSessionInfo")

    def to_json(self):
        return self.model_dump_json(by_alias=True)
    



class CardExpiration(BaseModel):
    duration: Optional[str] = Field(default=None, alias="Duration")
    expiration_date: Optional[datetime] = Field(default=None, alias="ExpirationDate")
    expiration_method: int = Field(alias="ExpirationMethod")

class OpsFromList(BaseModel):
    archival_collation: bool = Field(alias="ArchivalCollation")
    cancellation: bool = Field(alias="Cancellation")
    digital_sign: bool = Field(alias="DigitalSign")
    graphometric_sign: bool = Field(alias="GraphometricSign")
    pdf_native_sign: bool = Field(alias="PdfNativeSign")
    remote_sign: bool = Field(alias="RemoteSign")
    send_extended_email: bool = Field(alias="SendExtendedEmail")
    send_external_email: bool = Field(alias="SendExternalEmail")
    sharing: bool = Field(alias="Sharing")
    standard_collation: bool = Field(alias="StandardCollation")
    time_stamp: bool = Field(alias="TimeStamp")
    wf_forward: bool = Field(alias="WfForward")
    wf_refuse: bool = Field(alias="WfRefuse")
    wf_take_in_charge: bool = Field(alias="WfTakeInCharge")

class Card(BaseModel):
    additives: Optional[str] = Field(default=None, alias="Additives")
    agid_xml_creation_status: int = Field(alias="AgidXmlCreationStatus")
    archive_id: int = Field(alias="ArchiveId")
    card_expiration: CardExpiration = Field(alias="CardExpiration")
    card_id: str = Field(alias="CardId")
    card_prog: int = Field(alias="CardProg")
    computerized_classification: str = Field(alias="ComputerizedClassification")
    computerized_folder: str = Field(alias="ComputerizedFolder")
    doc_status: int = Field(alias="DocStatus")
    document_extension: str = Field(alias="DocumentExtension")
    document_type_id: int = Field(alias="DocumentTypeId")
    encrypted_card_id: str = Field(alias="EncryptedCardId")
    extern_mail_notification: Optional[str] = Field(default=None, alias="ExternMailNotification")
    extern_mail_notification_xml: Optional[str] = Field(default=None, alias="ExternMailNotificationXML")
    has_additional_data: bool = Field(alias="HasAdditionalData")
    has_attachment: bool = Field(alias="HasAttachment")
    has_computerized_classification: bool = Field(alias="HasComputerizedClassification")
    has_computerized_folder: bool = Field(alias="HasComputerizedFolder")
    has_data: Optional[bool] = Field(default=None, alias="HasData")
    has_document: bool = Field(alias="HasDocument")
    has_folder: bool = Field(alias="HasFolder")
    has_key_versions: bool = Field(alias="HasKeyVersions")
    has_notes: bool = Field(alias="HasNotes")
    has_partial_invalidations: bool = Field(alias="HasPartialInvalidations")
    indexes: Optional[str] = Field(default=None, alias="Indexes")
    invalidate_annotation: Optional[str] = Field(default=None, alias="InvalidateAnnotation")
    invoice: Optional[str] = Field(default=None, alias="Invoice")
    is_cc: bool = Field(alias="IsCC")
    is_curr_user_vis_doc: bool = Field(alias="IsCurrUserVisDoc")
    is_document_locked: bool = Field(alias="IsDocumentLocked")
    is_main_doc_sign_required: bool = Field(alias="IsMainDocSignRequired")
    is_read_only: bool = Field(alias="IsReadOnly")
    is_sealed: bool = Field(alias="IsSealed")
    is_signed: bool = Field(alias="IsSigned")
    is_signed_pdf: bool = Field(alias="IsSignedPdf")
    is_signed_xml: bool = Field(alias="IsSignedXml")
    is_sorted: bool = Field(alias="IsSorted")
    is_stored_protocol: bool = Field(alias="IsStoredProtocol")
    is_valid: bool = Field(alias="IsValid")
    is_vis_only_doc: bool = Field(alias="IsVisOnlyDoc")
    is_wf: bool = Field(alias="IsWf")
    is_wf_read_only: bool = Field(alias="IsWfReadOnly")
    num_pages: int = Field(alias="NumPages")
    ops_from_list: OpsFromList = Field(alias="OpsFromList")
    original_file_name: str = Field(alias="OriginalFileName")
    proc_wf: int = Field(alias="ProcWF")
    progressive: str = Field(alias="Progressive")
    signed_extension: str = Field(alias="SignedExtension")
    status: int = Field(alias="Status")
    stream_id: Optional[str] = Field(default=None, alias="StreamId")
    stream_id_shared: Optional[str] = Field(default=None, alias="StreamIdShared")
    time_stamp_format: int = Field(alias="TimeStampFormat")
    user_id_modifying: int = Field(alias="UserIdModifying")

class RetrieveCardsByParamResult(BaseModel):
    cards: List[Card] = Field(alias="Cards")
    hit_count: int = Field(alias="HitCount")
    invoice_monitor: Optional[str] = Field(default=None, alias="InvoiceMonitor")
    invoice_total_amounts: Optional[str] = Field(default=None, alias="InvoicesTotalAmounts")
    search_result: int = Field(alias="SearchResult")

class ArchiflowDocumentServiceGetDocumentsResponse(BaseModel,Response):
    retrieve_cards_result: RetrieveCardsByParamResult = Field(alias="RetrieveCardsByParamResult")

    def to_json(self):
        return self.model_dump_json(by_alias=True)
    
    
    
class Document(BaseModel):
    card_id: str = Field(alias="CardId")
    content: str = Field(alias="Content")
    content_type: str = Field(alias="ContentType")
    date_modify: str = Field(alias="DateModify")
    display_type: int = Field(alias="DisplayType")
    doc_digest: str = Field(alias="DocDigest")
    document_extension: str = Field(alias="DocumentExtension")
    document_full_extension: str = Field(alias="DocumentFullExtension")
    document_guid: str = Field(alias="DocumentGuid")
    document_title: str = Field(alias="DocumentTitle")
    file_size: int = Field(alias="FileSize")
    is_locked: bool = Field(alias="IsLocked")
    is_read_only: bool = Field(alias="IsReadOnly")
    is_sealed: bool = Field(alias="IsSealed")
    is_signed: bool = Field(alias="IsSigned")
    is_signed_pdf: bool = Field(alias="IsSignedPdf")
    is_signed_xml: bool = Field(alias="IsSignedXml")
    is_time_stamp: bool = Field(alias="IsTimeStamp")
    num_pages: int = Field(alias="NumPages")
    original_file_name: str = Field(alias="OriginalFileName")
    signed_extension: str = Field(alias="SignedExtension")
    time_stamp_format: int = Field(alias="TimeStampFormat")
    version: int = Field(alias="Version")
    warning_extension_off: bool = Field(alias="WarningExtensionOff")

class ArchiflowDocumentServiceGetDocumentPDFResponse(BaseModel, Response):
    get_card_document_result: int = Field(alias="GetCardDocument5Result")
    document: Document = Field(alias="oDocument")

    def to_json(self):
        return self.model_dump_json(by_alias=True)
