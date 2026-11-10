from pydantic import BaseModel


# Pydantic model for GAIA responses
class GaiaOutput(BaseModel):
    is_solvable: bool
    unsolvable_reason: str = ""
    final_answer: str = ""
