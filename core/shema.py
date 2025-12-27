
from pydantic import BaseModel
from typing import Generic, Optional, TypeVar, List



T = TypeVar("T")

class PagingResponse(BaseModel, Generic[T]):
    total: int
    page: int
    limit: int
    data: List[T]
    
class ErrorDetail(BaseModel):
    message: str
    code: str

# 2. Định nghĩa ErrorResponse chính
class ErrorResponse(BaseModel):
    message: str
    code: str
    # Thay vì 'str', ta dùng class 'ErrorDetail' vừa tạo ở trên
    data: Optional[ErrorDetail] = None