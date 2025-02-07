from typing import Type
from state import GraphState, WorkerState
from langchain_core.messages import HumanMessage, SystemMessage
from schemas import Sections
from langchain_core.language_models import BaseChatModel

class Nodes:
    def __init__(self, llm: BaseChatModel):
        self.llm: BaseChatModel = llm
        self.planner = llm.with_structured_output(Sections)

    def orchestrator(self, state: GraphState) -> dict:
        """Orchestrator that generates a plan for the report."""
        report_sections: Type[Sections] = self.planner.invoke(
            [
                SystemMessage(content="Generate a plan for the report."),
                HumanMessage(content=f"Here is the report topic: {state['topic']}"),
            ]
        )
        return {"sections": report_sections.sections}

    def synthesizer(self, state: GraphState) -> dict:
        """Synthesizer full report from sections."""
        completed_sections = state["completed_sections"]
        final_report = "\n\n---\n\n".join(completed_sections)
        return {"final_report": final_report}

    def llm_call(self, state: WorkerState) -> dict:
        """Worker writes a section of the report."""
        section = self.llm.invoke(
            [
                SystemMessage(content="Write a report section following the provided name and description. Include no preamble for each section. Use markdown formatting."),
                HumanMessage(content=f"Here is the section name: {state['section'].name} and description: {state['section'].description}"),
            ]
        )
        # All the workes write to the same key in parallel
        return {"completed_sections": [section.content]} # Should be array to use operator.add