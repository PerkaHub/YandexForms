from sqlalchemy.orm import Mapped, mapped_column

from src.database import Base


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(
        primary_key=True, nullable=False, index=True, autoincrement=True,
    )
    username: Mapped[str] = mapped_column(
        nullable=False, index=True, unique=True
    )
    hashed_password: Mapped[str] = mapped_column(
        nullable=False
    )
