from .llm import GroqClient
from .models import Answer, RetrievedChunk

class GroundedAnswerer:
    def __init__(self, llm: GroqClient):
        self.llm = llm
    def answer(self, question: str, evidence: list[RetrievedChunk]) -> Answer:
        return self.llm.answer(question, evidence)
