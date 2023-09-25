from enum import Enum

from typing import List, Optional

from sqlmodel import Field, Relationship, SQLModel


class ContentType(Enum):
    TEXT = 0
    COMMENT = 1
    IMAGE = 2
    AUDIO = 3
    VIDEO = 4


class PermissionType(Enum):
    CREATE = 0
    READ = 1
    UPDATE = 2
    DELETE = 3
    MODERATE = 4
    ADMIN = 5
    OWNER = 6


class PermissionRole(Enum):
    GUEST = 0
    USER = 1
    AUTHOR = 2


class UserGroup(SQLModel, table=True):
    user_id: Optional[int] = Field(
        default=None, foreign_key="user.id", primary_key=True
    )
    group_id: Optional[int] = Field(
        default=None, foreign_key="group.id", primary_key=True
    )


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


class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(unique=True)
    email: str = Field(unique=True)

    content: List["Content"] = Relationship(back_populates="owner")
    groups: List["Group"] = Relationship(back_populates="users", link_model=UserGroup)
    permissions: List["Permission"] = Relationship(
        back_populates="users", link_model=UserPermission
    )


class Content(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    type: ContentType
    filepath: str = Field(unique=True)
    owner_id: int = Field(foreign_key="user.id")

    owner: User = Relationship(back_populates="content")
    tags: List["Tag"] = Relationship(back_populates="contents", link_model=ContentTag)


class Group(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(unique=True)

    users: List[User] = Relationship(back_populates="groups", link_model=UserGroup)
    permissions: List["Permission"] = Relationship(
        back_populates="groups", link_model=GroupPermission
    )


class Permission(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    type: PermissionType
    role: PermissionRole

    users: List[User] = Relationship(
        back_populates="permissions", link_model=UserPermission
    )
    groups: List[Group] = Relationship(
        back_populates="permissions", link_model=GroupPermission
    )


class Tag(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(unique=True)

    contents: List[Content] = Relationship(back_populates="tags", link_model=ContentTag)
