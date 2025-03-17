from enum import Enum


class DocumentTypeFilter(Enum):
    GENERAL = 77
    
    @classmethod
    def get_id(cls, name):
        try:
            return cls[name].value
        except KeyError:
            raise ValueError(f"Invalid name: {name}")
        
class ArchiveFilter(Enum):
    SUPPLIER_INVOICES = 1
    
    @classmethod
    def get_id(cls, name):
        try:
            return cls[name].value
        except KeyError:
            raise ValueError(f"Invalid name: {name}")
        
        
class Filter_IDs(Enum):
    SUPPLIER_CODE_FILTER = 4
    COMPANY_FILTER = 6
    DATA_FILTER = 19
    INVOICE_STATUS_FILTER = 21

    @classmethod
    def get_id(cls, name):
        try:
            return cls[name].value
        except KeyError:
            raise ValueError(f"Invalid name: {name}")