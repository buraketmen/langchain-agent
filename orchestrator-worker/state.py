import operator
from typing_extensions import TypedDict
from typing import Annotated
from schemas import Section

# Graph state
class GraphState(TypedDict):
    topic: str # Report topic
    sections: list[Section] # List of report sections
    completed_sections: Annotated[list, operator.add] # All workers write to this key in parallel
    final_report: str # Final report
    
# Worker state
class WorkerState(TypedDict):
    section: Section
    completed_sections: Annotated[list, operator.add]