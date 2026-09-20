from pydantic import BaseModel

class BasePersonSchemas(BaseModel):
    name: str

class PersonCreatSchemas(BasePersonSchemas):
    pass

class PersonReasponsSchemas(BasePersonSchemas):
    id: int

class PersonUpdateSchemas(BasePersonSchemas):
    pass