

from fastapi import APIRouter
from modules.calculator.schema import SumRequest, SumResponse
from modules.calculator.service import sum_two_numbers

router = APIRouter()

@router.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "Calculator module is healthy"}

@router.post("/sum", response_model=SumResponse)
def sum_handler(payload: SumRequest):
    return {
        "result": sum_two_numbers(payload.a, payload.b)
    }

@router.get("/info")
def module_info() -> dict[str, str]:
    return {"module": "Calculator", "version": "1.0.0"}
# --- IGNORE ---