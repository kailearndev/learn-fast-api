from datetime import datetime
from pydantic import BaseModel
from uuid import UUID


from core.shema import PagingResponse
class TagsCreateDTO(BaseModel):
    name: str
    


class TagsUpdateDTO(BaseModel):
    name : str | None = None

class TagsResponse(BaseModel):
    id: UUID
    name: str
    created_at: datetime
    updated_at: datetime | None = None
  

TagsPagingResponse = PagingResponse[TagsResponse]
