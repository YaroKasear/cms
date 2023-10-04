from enum import Enum

from typing import List, Optional

from sqlmodel import Field, Relationship, SQLModel


class ContentType(Enum):
    TEXT = 0
    COMMENT = 1
    MESSAGE = 2
    IMAGE = 3
    AUDIO = 4
    VIDEO = 5


class PermissionType(Enum):
    CREATE = 0
    READ = 1
    UPDATE = 2
    DELETE = 3


class PermissionCategory(Enum):
    USER = 0
    GROUP = 1
    OTHER = 2


class UserGroup(SQLModel, table=True):
    user_id: Optional[int] = Field(
        default=None, foreign_key="user.id", primary_key=True
    )
    group_id: Optional[int] = Field(
        default=None, foreign_key="group.id", primary_key=True
    )


class ContentTag(SQLModel, table=True):
    content_id: Optional[int] = Field(
        default=None, foreign_key="content.id", primary_key=True
    )
    tag_id: Optional[int] = Field(default=None, foreign_key="tag.id", primary_key=True)


class UserPermission(SQLModel, table=True):
    user_id: Optional[int] = Field(
        default=None, primary_key=True, foreign_key="user.id"
    )
    permission_id: Optional[int] = Field(
        default=None, primary_key=True, foreign_key="permission.id"
    )


class GroupPermission(SQLModel, table=True):
    group_id: Optional[int] = Field(
        default=None, primary_key=True, foreign_key="group.id"
    )
    permission_id: Optional[int] = Field(
        default=None, primary_key=True, foreign_key="permission.id"
    )


class ContentPermission(SQLModel, table=True):
    content_id: Optional[int] = Field(
        default=None, primary_key=True, foreign_key="content.id"
    )
    permission_id: Optional[int] = Field(
        default=None, primary_key=True, foreign_key="permission.id"
    )


class Permission(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    type: PermissionType
    category: PermissionCategory

    user: "User" = Relationship(back_populates="permissions", link_model=UserPermission)
    group: "Group" = Relationship(
        back_populates="permissions", link_model=GroupPermission
    )
    content: "Content" = Relationship(
        back_populates="permissions", link_model=ContentPermission
    )


class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(unique=True)
    email: str = Field(unique=True)
    password_hash: str
    password_salt: str

    content: List["Content"] = Relationship(back_populates="owner")
    groups: List["Group"] = Relationship(back_populates="users", link_model=UserGroup)

    permissions: List[Permission] = Relationship(
        back_populates="user", link_model=UserPermission
    )


class Group(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(unique=True)

    users: List[User] = Relationship(back_populates="groups", link_model=UserGroup)

    permissions: List[Permission] = Relationship(
        back_populates="group", link_model=GroupPermission
    )


class Content(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    type: ContentType
    filepath: str = Field(unique=True)
    owner_id: int = Field(foreign_key="user.id")

    owner: User = Relationship(back_populates="content")
    tags: List["Tag"] = Relationship(back_populates="contents", link_model=ContentTag)

    permissions: List[Permission] = Relationship(
        back_populates="content", link_model=ContentPermission
    )


class Tag(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(unique=True)

    contents: List[Content] = Relationship(back_populates="tags", link_model=ContentTag)
