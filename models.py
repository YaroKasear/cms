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
    filepath: str = Field(unique=True)
    owner_id: int = Field(foreign_key="user.id")

    owner: "User" = Relationship(back_populates="content")
    tags: List["Tag"] = Relationship(back_populates="contents", link_model="ContentTag")


class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(unique=True)
    email: str = Field(unique=True)

    content: List[Content] = Relationship(back_populates="owner")
    groups: List["Group"] = Relationship(back_populates="users", link_model="UserGroup")
    permissions: List["Permission"] = Relationship(
        back_populates="users", link_model="UserPermission"
    )


class Group(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(unique=True)

    users: List[User] = Relationship(back_populates="groups", link_model="UserGroup")


class Permission(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    type: PermissionType
    role: PermissionRole

    users: List[User] = Relationship(
        back_populates="permissions", link_model="UserPermission"
    )
    groups: List[Group] = Relationship(
        back_populates="permissions", link_model="GroupPermission"
    )


class Tag(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(unique=True)

    contants: List[Content] = Relationship(
        back_populates="tags", link_model="ContentTag"
    )


class UserGroup(SQLModel, table=True):
    user_id: Optional[int] = Field(default=None, foreign_key="user.id")
    group_id: Optional[int] = Field(default=None, foreign_key="group.id")


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


class ContentTag(SQLModel, table=True):
    content_id: Optional[int] = Field(
        default=None, foreign_key="content.id", primary_key=True
    )
    tag_id: Optional[int] = Field(default=None, foreign_key="tag.id", primary_key=True)
