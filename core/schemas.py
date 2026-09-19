from pydantic import BaseModel

class PersonCreatSchemas(BaseModel):
    name: str


class PersonReasponsSchemas(BaseModel):
    id: int
    name: str


class PersonUpdateSchemas(BaseModel):
    name: str