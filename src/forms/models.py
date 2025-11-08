from sqlalchemy import (
    ForeignKey,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database import Base


class Form(Base):
    __tablename__ = "forms"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        nullable=False,
        autoincrement=True,
    )
    title: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(nullable=True)
    owner_id: Mapped[int] = mapped_column(ForeignKey("users.id"))

    owner: Mapped["User"] = relationship(
        "User", back_populates="forms", lazy="joined"
    )
    fields: Mapped[list["FormField"]] = relationship(
        "FormField",
        back_populates="form",
        lazy="selectin",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )
    responses: Mapped[list["FormResponse"]] = relationship(
        "FormResponse", back_populates="form", lazy="selectin"
    )


class FormField(Base):
    __tablename__ = "form_fields"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        nullable=False,
        autoincrement=True,
    )
    form_id: Mapped[int] = mapped_column(ForeignKey("forms.id"))
    field_type: Mapped[str] = mapped_column()
    question_text: Mapped[str] = mapped_column()
    is_required: Mapped[bool] = mapped_column()

    form: Mapped["Form"] = relationship(
        "Form", back_populates="fields", lazy="joined"
    )
    options: Mapped[list["FieldOption"]] = relationship(
        "FieldOption",
        back_populates="field",
        lazy="selectin",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )
    responses: Mapped[list["FormResponse"]] = relationship(
        "FormResponse", back_populates="field", lazy="selectin"
    )


class FieldOption(Base):
    __tablename__ = "field_options"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        nullable=False,
        autoincrement=True,
    )
    field_id: Mapped[int] = mapped_column(ForeignKey("form_fields.id"))
    option_text: Mapped[str] = mapped_column()

    field: Mapped["FormField"] = relationship(
        "FormField", back_populates="options", lazy="joined"
    )
    responses: Mapped[list["FormResponse"]] = relationship(
        "FormResponse",
        back_populates="option",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )


class FormResponse(Base):
    __tablename__ = "form_responses"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        nullable=False,
        autoincrement=True,
    )
    response_id: Mapped[str] = mapped_column(nullable=False)
    form_id: Mapped[int] = mapped_column(ForeignKey("forms.id"))
    field_id: Mapped[int] = mapped_column(ForeignKey("form_fields.id"))
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    answer_text: Mapped[str] = mapped_column(nullable=True)
    answer_option_id: Mapped[int] = mapped_column(
        ForeignKey("field_options.id"), nullable=True
    )

    form: Mapped["Form"] = relationship(
        "Form", back_populates="responses", lazy="joined"
    )
    field: Mapped["FormField"] = relationship(
        "FormField", back_populates="responses", lazy="joined"
    )
    user: Mapped["User"] = relationship(
        "User", back_populates="responses", lazy="joined"
    )
    option: Mapped["FieldOption"] = relationship(
        "FieldOption",
        back_populates="responses",
    )
