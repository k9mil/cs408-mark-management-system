from pydantic import BaseModel


class SampleSchema(BaseModel):
    id: int
    username: str

    class Config:
        orm_mode = True