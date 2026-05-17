"""Pydantic models for JSONPlaceholder API response validation."""

from pydantic import BaseModel, ConfigDict, Field


class Post(BaseModel):
    """Represent a JSONPlaceholder post response.

    Attributes:
        id: Unique post identifier.
        title: Post title.
        body: Post body content.
        user_id: Identifier for the user who owns the post.
    """

    model_config = ConfigDict(populate_by_name=True)

    id: int
    title: str
    body: str
    user_id: int = Field(alias="userId")


class PostCreate(BaseModel):
    """Represent a JSONPlaceholder post creation payload.

    Attributes:
        title: Post title.
        body: Post body content.
        user_id: Identifier for the user who owns the post.
    """

    model_config = ConfigDict(populate_by_name=True)

    title: str
    body: str
    user_id: int = Field(alias="userId")


class User(BaseModel):
    """Represent a JSONPlaceholder user response."""

    model_config = ConfigDict(populate_by_name=True)

    id: int
    name: str
    username: str
    email: str


class Comment(BaseModel):
    """Represent a JSONPlaceholder comment response."""

    model_config = ConfigDict(populate_by_name=True)

    id: int
    post_id: int = Field(alias="postId")
    name: str
    email: str
    body: str
