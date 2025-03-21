from datetime import datetime
from typing import Optional

from pydantic import BaseModel, validator


class Paginated(BaseModel):
    total_count: int
    page: int


class Created(BaseModel):
    created: Optional[datetime]

    @validator('created', pre=True, always=True)
    def set_created(cls, v):  # noqa: N805
        return v or datetime.now()
