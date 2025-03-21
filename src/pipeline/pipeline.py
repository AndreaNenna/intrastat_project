from abc import ABC, abstractmethod
from typing import List

class PipelineStep(ABC):
    """Classe base astratta per ogni step della pipeline"""
    @abstractmethod
    def process(self, data):
        pass

class PipelineInput(ABC):
    @abstractmethod
    def to_json(self):
        pass

class Pipeline:
    def __init__(self):
        self.steps: List[PipelineStep] = []

    def add_step(self, step: PipelineStep):
        self.steps.append(step)

    def run(self, data):
        for step in self.steps:
            data = step.process(data)
        return data