from sqlalchemy import Integer, String, Boolean, Text, ForeignKey, DateTime
from sqlalchemy.orm import relationship, Mapped, mapped_column
from .database import Base
from datetime import datetime
from typing import Optional

class Email(Base):
    __tablename__ = "emails"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    sender: Mapped[Optional[str]] = mapped_column(index=True)
    recipient: Mapped[Optional[str]] = mapped_column(index=True)
    date: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    subject: Mapped[Optional[str]] = mapped_column()
    body: Mapped[Optional[str]] = mapped_column(Text)
    
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=True)

    # Relationships
    privilege_log: Mapped[Optional["PrivilegeLog"]] = relationship(back_populates="email", uselist=False)
    user: Mapped["User"] = relationship()

class PrivilegeLog(Base):
    __tablename__ = "privilege_logs"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    email_id: Mapped[int] = mapped_column(ForeignKey("emails.id"))
    
    is_privileged: Mapped[bool] = mapped_column(default=False)
    privilege_type: Mapped[Optional[str]] = mapped_column(nullable=True) # e.g. "Attorney-Client", "Work Product"
    log_description: Mapped[Optional[str]] = mapped_column(Text, nullable=True) # The "safe" description
    reasoning: Mapped[Optional[str]] = mapped_column(Text, nullable=True) # AI reasoning
    redacted_text: Mapped[Optional[str]] = mapped_column(Text, nullable=True) # JSON string of text list

    email: Mapped["Email"] = relationship(back_populates="privilege_log")

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    username: Mapped[str] = mapped_column(unique=True, index=True)
    email: Mapped[str] = mapped_column(unique=True, index=True)
    hashed_password: Mapped[str] = mapped_column()
