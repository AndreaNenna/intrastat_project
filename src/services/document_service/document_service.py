from abc import ABC, abstractmethod

class DocumentService(ABC):
    def __init__(self, base_url):
        self.base_url = base_url

    @abstractmethod
    def get_documents(self):
        pass

    @abstractmethod
    def get_document_pdf(self):
        pass
    
    @abstractmethod
    def authenticate(self):
        pass