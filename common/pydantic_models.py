from pydantic import BaseModel, Field, AliasPath


class URLParams(BaseModel):
    pk: int = Field(validation_alias=AliasPath("pk"))
