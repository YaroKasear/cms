from enum import Enum

from typing import List, Optional

from sqlmodel import Field, Relationship, SQLModel


class ContentType(Enum):
    TEXT = "text"
    COMMENT = "comment"
    IMAGE = "image"
    AUDIO = "audio"
    VIDEO = "video"


class PermissionType(Enum):
    CREATE = "create"
    READ = "read"
    UPDATE = "update"
    DELETE = "delete"
    MODERATE = "moderate"
    ADMIN = "admin"
    OWNER = "owner"


class PermissionRole(Enum):
    GUEST = "guest"
    USER = "user"
    AUTHOR = "author"


class Content(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    type: ContentType
    owner_id: int = Field(foreign_key="user.id")

    owner: "User" = Relationship(back_populates="content")


class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(unique=True)
    email: str = Field(unique=True)

    content: List[Content] = Relationship(back_populates="owner")


class Group(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(unique=True)


class Permission(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    type: PermissionType
    role: PermissionRole


class UserPermission(SQLModel, table=True):
    user_id: Optional[int] = Field(
        default=None, foreign_key="user.id", primary_key=True
    )
    permission_id: Optional[int] = Field(
        default=None, foreign_key="permission.id", primary_key=True
    )


class GroupPermission(SQLModel, table=True):
    group_id: Optional[int] = Field(
        default=None, foreign_key="group.id", primary_key=True
    )
    permission_id: Optional[int] = Field(
        default=None, foreign_key="permission.id", primary_key=True
    )
