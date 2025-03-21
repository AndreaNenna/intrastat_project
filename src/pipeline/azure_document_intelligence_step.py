import base64

from pydantic import BaseModel, Field, ConfigDict
from typing import List

from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.ai.documentintelligence.models import AnalyzeDocumentRequest

from src.pipeline.pipeline import PipelineStep, PipelineInput

    
class DocumentIntelligenceMarkdownResult(BaseModel):
    file_name: str
    markdown: str

class GenerativeAIPipelineInput(BaseModel, PipelineInput):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    document_pdf_markdowns: List[DocumentIntelligenceMarkdownResult] = Field(alias="document_pdf_markdowns")

    def to_json(self):
        return self.model_dump_json(by_alias=False)

class AzureDocumentIntelligenceStep(PipelineStep):
    def __init__(self, document_intelligence_client: DocumentIntelligenceClient):
        self.client = document_intelligence_client
        
    def process(self, data: PipelineInput):
        markdown_files_processed = []

        for pdf_file in data.document_pdf_files:
            
            pdf_byte = base64.b64decode(pdf_file.file_base64_string)


            poller = self.client.begin_analyze_document(
                "prebuilt-layout", AnalyzeDocumentRequest(bytes_source=pdf_byte), output_content_format="markdown"
            )

            result = poller.result()

            markdown_files_processed.append(DocumentIntelligenceMarkdownResult(file_name=pdf_file.file_name, markdown=result["content"]))
        
        return GenerativeAIPipelineInput(document_pdf_markdowns=markdown_files_processed)
