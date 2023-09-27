from pydantic import (
    BaseModel,
    Field,
    AliasPath,
    EmailStr,
    StrictStr,
    StrictInt,
    SecretStr,
    model_validator,
)
from datetime import date
from re import match
from .constants import NAME_PATTERN, PASSWORD_PATTERN, DOCTOR_PATTERN
from typing import Union, Optional
from rest_framework import exceptions


class URLParams(BaseModel):
    pk: int = Field(validation_alias=AliasPath("pk"))


class CreateUserRequest(BaseModel):
    model_config = dict(extra="forbid")

    email: EmailStr = Field(validation_alias=AliasPath("email"))
    other_names: StrictStr = Field(
        validation_alias=AliasPath("other_names"), max_length=50, min_length=2
    )
    surname: StrictStr = Field(
        validation_alias=AliasPath("surname"), max_length=30, min_length=2
    )
    password: SecretStr = Field(
        validation_alias=AliasPath("password"), min_length=10, max_length=30
    )
    password2: SecretStr = Field(
        validation_alias=AliasPath("password2"), min_length=10, max_length=30
    )
    date_of_birth: date = Field(
        validation_alias=AliasPath("date_of_birth"), le=date.today()
    )

    @model_validator(mode="after")
    def validate_input(cls, values):
        if not all(
            (
                match(NAME_PATTERN, values.other_names),
                match(NAME_PATTERN, values.surname),
            )
        ):
            raise exceptions.APIException(detail={"message": "Names should contain only letters and '-' !", "status": 422})
        if values.password._secret_value != values.password2._secret_value:
            raise exceptions.APIException(detail={"message": "Password mismacth!", "status": 422})
        if not match(PASSWORD_PATTERN, values.password._secret_value):
            raise exceptions.APIException(detail={"message": "Password is not valid!", "status": 422})
        return values


class LoginRequest(BaseModel):
    model_config = dict(extra="forbid")
    email: EmailStr = Field(validation_alias=AliasPath("email"))
    password: SecretStr = Field(
        validation_alias=AliasPath("password")
    )

    @model_validator(mode="after")
    def validate_input(cls, values):
        return values

class CreateRecordRequest(BaseModel):
    model_config = dict(extra="forbid")
    doctor: StrictStr = Field(validation_alias=AliasPath("doctor"))
    diagnosis: str = Field(validation_alias=AliasPath("diagnosis"), max_length=500)
    treatment: str = Field(validation_alias=AliasPath("treatment"), max_length=500)
    date_of_treatment: date = Field(
        validation_alias=AliasPath("date_of_treatment"), gt=date.today()
    )
    patient: StrictInt = Field(validation_alias=AliasPath("patient"))

    @model_validator(mode="after")
    def validate_input(cls, values):
        if not match(DOCTOR_PATTERN, values.doctor):
            raise exceptions.APIException(detail={"message": "Doctor's name is not valid", "status": 422})
        return values
    
class UpdateRecordRequest(BaseModel):
    model_config = dict(extra="forbid")
    doctor: Optional[StrictStr] = Field(validation_alias=AliasPath("doctor"))
    diagnosis: Optional[str] = Field(validation_alias=AliasPath("diagnosis"), max_length=500)
    treatment: Optional[str] = Field(validation_alias=AliasPath("treatment"), max_length=500)
    date_of_treatment: Optional[date] = Field(
        validation_alias=AliasPath("date_of_treatment"), gt=date.today()
    )

    @model_validator(mode="after")
    def validate_input(cls, values):
        if not match(DOCTOR_PATTERN, values.doctor):
            raise exceptions.APIException(detail={"message": "Doctor's name is not valid", "status": 422})
        return values


class APIResponseModel(BaseModel):
    model_config = dict(extra="forbid")
    data: dict[str, Union[str, list, dict]] = Field(validation_alias=AliasPath("data"))

    @model_validator(mode="after")
    def prepare_output(cls, values):
        return {"response": {"data": values.data}}
    
class APIErrorModel(BaseModel):
    model_config = dict(extra="forbid")
    error: dict[str, Union[str, list, dict]] = Field(validation_alias=AliasPath("error"))

    @model_validator(mode="after")
    def prepare_output(cls, values):
        return {"error": {"message": values.error}}