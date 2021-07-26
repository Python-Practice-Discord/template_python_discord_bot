import uuid

from sqlalchemy import Column, DateTime, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import declarative_base


Base = declarative_base()


class User(Base):
    __tablename__ = "user"
    id = Column(UUID(as_uuid=True), primary_key=True, unique=True, default=uuid.uuid4)
    discord_id = Column(String, unique=True, nullable=False)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)


class PrivacyTermsOfService(Base):
    __tablename__ = "privacy_terms_of_service"
    version = Column(String, primary_key=True, unique=True)
    content = Column(String, nullable=False)


class UserTOS(Base):
    __tablename__ = "user_privacy_tos"
    user_id = Column(UUID(as_uuid=True), ForeignKey("user.id"), primary_key=True)
    tos_version = Column(String, ForeignKey("privacy_terms_of_service.version"), primary_key=True)
