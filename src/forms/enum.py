from enum import Enum


class FieldTypeEnum(str, Enum):
    TEXT = "text"
    RADIO = "radio"
    CHECKBOX = "checkbox"
