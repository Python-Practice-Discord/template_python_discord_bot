import uuid

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import declarative_base


Base = declarative_base()


class User(Base):
    __tablename__ = "user"
    id: uuid.UUID = Column(UUID(as_uuid=True), primary_key=True, unique=True, default=uuid.uuid4)
    discord_id = Column(String, unique=True, nullable=False)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)


class PrivacyTermsOfService(Base):
    __tablename__ = "privacy_terms_of_service"
    version = Column(String, primary_key=True, unique=True)
    content = Column(String, nullable=False)
    hash = Column(String, nullable=False)
    # created_at = Column(DateTime, nullable=False)


class UserPrivacyTOS(Base):
    __tablename__ = "user_privacy_tos"
    user_id: uuid.UUID = Column(UUID(as_uuid=True), ForeignKey("user.id"), primary_key=True)
    tos_version = Column(String, ForeignKey("privacy_terms_of_service.version"), primary_key=True)


class BotVersion(Base):
    __tablename__ = "bot_version"
    version = Column(String, unique=True, primary_key=True, nullable=False)
    notification_sent = Column(Boolean, nullable=False)


class BotMessage(Base):
    __tablename__ = "bot_message"
    name = Column(String, unique=True, primary_key=True, nullable=False)
    message_id = Column(String, nullable=False, unique=True)
