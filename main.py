from src.pipeline.pipeline import Pipeline
from src.pipeline.document_fetcher import ArchiflowDocumentFetcherStep, ArchiflowFetcherPipelineInput
from src.pipeline.azure_document_intelligence_step import AzureDocumentIntelligenceStep
from src.pipeline.generative_ai_step import GenerativeAIStep
from src.services.document_service.archiflow_document_service import ArchiflowDocumentService
from src.services.document_service.models.archiflow_request_models import ArchiflowDocumentServiceAuthenticationBody, ArchiflowConnectionInfo

from azure.core.credentials import AzureKeyCredential
from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.ai.documentintelligence.models import AnalyzeDocumentRequest

from langchain_openai import AzureChatOpenAI

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
                                                                         oConnectionInfo=connection_info)

filters = {
    "SUPPLIER_CODE": "482582",
    "COMPANY_CODE": "ITC",
    "DATE_FILTER" : "01/01/2025:31/01/2025",
    "INVOCE_STATUS": "BOOKED",
    "ARCHIVE_TYPE": "SUPPLIER_INVOICES",
    "DOCUMENT_TYPE": "GENERAL"
}

pipeline_input = ArchiflowFetcherPipelineInput(credential=authentication_request_body,
                                               filters= filters)

#ARCHIFLOW STEP INITIALIZATION OBJECTS
archiflow_document_service = ArchiflowDocumentService(archiflow_url)
document_fetcher_step = ArchiflowDocumentFetcherStep(document_service=archiflow_document_service)

#DOCUMENT INTELLIGENCE INITIALIZATION OBJECTS
document_intelligence_client = DocumentIntelligenceClient(endpoint= os.getenv("DOCUMENT_INTELLIGENCE_ENDPOINT"),
                                                          credential=AzureKeyCredential(os.getenv("DOCUMENT_INTELLIGENCE_KEY")))
azure_document_intelligence_step = AzureDocumentIntelligenceStep(document_intelligence_client)

#GENERATIVE AI INITIALIZAZION OBJECTS
azure_openai_client = AzureChatOpenAI(azure_endpoint= os.getenv("AZURE_OPENAI_ENDPOINT"),
                                      api_key=os.getenv("AZURE_OPENAI_KEY"),
                                      azure_deployment=os.getenv("AZURE_OPENAI_DEPLOYMENT"),
                                      api_version=os.getenv("API_VERSION"))
generative_ai_step = GenerativeAIStep(azure_openai_client)

process_pipeline = Pipeline()

process_pipeline.add_step(document_fetcher_step)
process_pipeline.add_step(azure_document_intelligence_step)
process_pipeline.add_step(generative_ai_step)


result = process_pipeline.run(pipeline_input)


for element in result:
    print(f"Result for file {element["file_name"]}: \n {element["result"]}")
