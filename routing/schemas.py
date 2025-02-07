from typing_extensions import Literal
from pydantic import BaseModel, Field

class RouterSchema(BaseModel):
    step: Literal["poem", "story", "joke"] = Field(None, description="The next step in the routing process.")