from datetime import datetime
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database import Base


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(
        primary_key=True, nullable=False, autoincrement=True,
    )
    username: Mapped[str] = mapped_column(
        nullable=False, index=True, unique=True
    )
    hashed_password: Mapped[str] = mapped_column(
        nullable=False
    )

    refresh_tokens: Mapped[list["RefreshToken"]] = relationship(
        "RefreshToken",
        back_populates="user",
        lazy='selectin'
    )


class RefreshToken(Base):
    __tablename__ = "refresh_tokens"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"))
    token_hash: Mapped[str] = mapped_column()
    expires_at: Mapped[datetime] = mapped_column()
    created_at: Mapped[datetime] = mapped_column(default=datetime.now())

    user: Mapped["User"] = relationship(
        "User",
        back_populates="refresh_tokens",
        lazy='joined'
    )
