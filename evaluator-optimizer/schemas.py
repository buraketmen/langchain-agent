from typing import Literal
from pydantic import BaseModel, Field

class Feedback(BaseModel):
    grade: Literal["funny", "not_funny"] = Field(description="Decide if the joke is funny or not.")
    feedback: str = Field(description="If the joke is not funny, provide feedback on how to improve it.")
