from abc import ABC, abstractmethod

class DocumentHandler(ABC):
    def __init__(self, next_handler=None):
        self.next_handler = next_handler

    @abstractmethod
    def handle(self, document):
        pass