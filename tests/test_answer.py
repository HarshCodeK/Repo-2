from financial_assistant.answer import GroundedAnswerer
from financial_assistant.models import RetrievedChunk, SourceType, Answer

class FakeLLM:
    def answer(self, question, evidence):
        return Answer(supported=True, answer=f"Evidence: {evidence[0].text}", sources=evidence)

def test_grounded_answerer_passes_evidence():
    evidence=[RetrievedChunk(source="p.pdf", source_type=SourceType.pdf, text="Meal allowance is 500 INR.", page=2, distance=.1)]
    result=GroundedAnswerer(FakeLLM()).answer("What is the meal allowance?", evidence)
    assert result.supported is True
    assert "500 INR" in result.answer
