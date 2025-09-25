from pydantic import BaseModel, field_validator
from src.forms.enum import FieldTypeEnum


class CreateFieldOption(BaseModel):
    option_text: str


class CreateFormField(BaseModel):
    field_type: FieldTypeEnum
    question_text: str
    is_required: bool
    options: list[CreateFieldOption] = []

    @field_validator('options')
    @classmethod
    def validate_options(cls, v, info):
        field_type = info.data.get('field_type')

        if field_type == FieldTypeEnum.TEXT and v:
            raise ValueError('Text fields cannot have options')
        if field_type in [FieldTypeEnum.RADIO, FieldTypeEnum.CHECKBOX] and not v:
            raise ValueError('Radio and checkbox fields must have options')

        return v


class CreateForm(BaseModel):
    title: str
    description: str | None
    fields: list[CreateFormField]
