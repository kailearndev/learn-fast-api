from pydantic import BaseModel

class SumRequest(BaseModel):
    a: float
    b: float
class SumResponse(BaseModel):
    result: float