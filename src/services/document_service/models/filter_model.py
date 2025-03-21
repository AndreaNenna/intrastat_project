from enum import Enum

class BaseEnumFilter(Enum):
    @classmethod
    def get_id(cls, name):
        try:
            return cls[name].value
        except KeyError:
            raise ValueError(f"Invalid name: {name}")  
          
class DocumentTypeFilter(BaseEnumFilter):
    GENERAL = 77

class ArchiveFilter(BaseEnumFilter):
    SUPPLIER_INVOICES = 0

class Filter_IDs(BaseEnumFilter):
    SUPPLIER_CODE = "4"
    COMPANY_CODE = "6"
    DATE_FILTER = "19"
    INVOCE_STATUS = "21"
