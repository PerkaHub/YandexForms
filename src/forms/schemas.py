from pydantic import BaseModel, field_validator

from src.forms.enum import FieldTypeEnum


class CreateOrUpdateFieldOption(BaseModel):
    option_text: str


class CreateOrUpdateFormField(BaseModel):
    field_type: FieldTypeEnum
    question_text: str
    is_required: bool
    options: list[CreateOrUpdateFieldOption] = []

    @field_validator("options")
    @classmethod
    def validate_options(cls, v, info):
        field_type = info.data.get("field_type")

        if field_type == FieldTypeEnum.TEXT and v:
            raise ValueError("Text fields cannot have options")
        if (
            field_type in [FieldTypeEnum.RADIO, FieldTypeEnum.CHECKBOX]
            and not v
        ):
            raise ValueError("Radio and checkbox fields must have options")

        return v


class CreateOrUpdateForm(BaseModel):
    title: str
    description: str | None = None
    fields: list[CreateOrUpdateFormField]


class ResponseFieldOption(BaseModel):
    id: int
    option_text: str

    class Config:
        from_attributes = True


class ResponseFormField(BaseModel):
    id: int
    field_type: str
    question_text: str
    is_required: bool
    options: list[ResponseFieldOption] = []

    class Config:
        from_attributes = True


class ResponseForm(BaseModel):
    id: int
    title: str
    description: str | None
    fields: list[ResponseFormField]

    class Config:
        from_attributes = True


class ResponseFormList(BaseModel):
    forms: list[ResponseForm]


class AnswerData(BaseModel):
    field_id: int
    answer_text: str | None = None
    answer_option_id: int | None = None


class CreateAnswer(BaseModel):
    answers: list[AnswerData]
