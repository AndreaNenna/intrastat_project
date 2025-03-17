from src.services.document_service.archiflow_document_service import ArchiflowDocumentService

from src.services.document_service.models.archiflow_request_models import ArchiflowDocumentServiceAuthenticationBody, ArchiflowDocumentServiceGetDocumentsBody, ArchiflowConnectionInfo, ParametersIn, SessionInfo, Archive, DocumentType, FieldObj, SearchCriteria
from src.services.document_service.models.filter_model import Filter_IDs, DocumentTypeFilter, ArchiveFilter
from dotenv import load_dotenv
import os


load_dotenv()
archiflow_url = os.getenv("ARCHIFLOW_URL")
archiflow_user = os.getenv("ARCHIFLOW_USER")
archiflow_password = os.getenv("ARCHIFLOW_PASSWORD")


connection_info = ArchiflowConnectionInfo(Language="0",
                                          DateFormat="dd/mm/yyyy",
                                          WorkflowDomain="SIAV")

authentication_request_body = ArchiflowDocumentServiceAuthenticationBody(strUser=archiflow_user,
                                                                         strPassword=archiflow_password,
                                                                         onConnectionInfo=connection_info)


archiflow_service = ArchiflowDocumentService(archiflow_url)
session_id = archiflow_service.authenticate(authentication_request_body).session_info.session_id


# Build archives

archive = [Archive(archive_id=ArchiveFilter.SUPPLIER_INVOICES.value)]

# Build document_type
document_type = DocumentType(document_type_id=DocumentTypeFilter.GENERAL.value)


#Build Fields
supplier_code = FieldObj(field_id=Filter_IDs.SUPPLIER_CODE_FILTER.value, field_value="482582")
company_code = FieldObj(field_id=Filter_IDs.COMPANY_FILTER.value, field_value="ITC")
data_filter = FieldObj(field_id=Filter_IDs.DATA_FILTER.value, field_value="01/01/2025:31/01/2025")
invoice_status_filter = FieldObj(FieldId=Filter_IDs.INVOICE_STATUS_FILTER.value, field_value="BOOKED")

filter_fields = [supplier_code, company_code, data_filter, invoice_status_filter]


#Build Search criteria
search_criteria = SearchCriteria(archives=archive,
                                 document_type=document_type,
                                 fields=filter_fields)


session_info = SessionInfo(session_id=session_id)

parametersIn = ParametersIn(session_info=session_info,
                            search_criteria=search_criteria,
                            page_number=1,
                            page_size=10,
                            get_indexes=False,
                            get_invoice=False)


archiflow_get_documents_request_body = ArchiflowDocumentServiceGetDocumentsBody(param_in=parametersIn)

result = archiflow_service.get_documents(archiflow_get_documents_request_body)

pdf_ids = [card.card_id for card in result.retrieve_cards_result.cards]


for pdf_id in pdf_ids:
    print(f"File retrieved: {pdf_id}")