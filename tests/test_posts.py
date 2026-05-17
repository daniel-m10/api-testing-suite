"""Tests for the JSONPlaceholder posts endpoint."""

import pytest

from api_testing_suite.client import APIClient
from api_testing_suite.models import Post, PostCreate


@pytest.mark.smoke
@pytest.mark.parametrize("post_id", [1, 50, 100], ids=["1", "50", "100"])
def test_get_post_with_valid_id_returns_200(
    api_client: APIClient,
    post_id: int,
) -> None:
    """Verify that retrieving a valid post ID returns HTTP 200.

    Args:
        api_client: Shared API client fixture from conftest.py.
        post_id: Valid post ID to retrieve.
    """
    # Arrange
    endpoint = f"/posts/{post_id}"

    # Act
    response = api_client.get(endpoint)

    # Assert
    assert response.status_code == 200


@pytest.mark.smoke
def test_get_posts_list_returns_200(
    api_client: APIClient,
) -> None:
    """Verify that retrieving posts returns HTTP 200.

    Args:
        api_client: Shared API client fixture from conftest.py.
    """
    # Arrange
    endpoint = "/posts"

    # Act
    response = api_client.get(endpoint)

    # Assert
    assert response.status_code == 200


@pytest.mark.smoke
def test_get_posts_list_with_default_query_returns_non_empty_list(
    api_client: APIClient,
) -> None:
    """Verify that retrieving posts with default query returns non-empty data.

    Args:
        api_client: Shared API client fixture from conftest.py.
    """
    # Arrange
    endpoint = "/posts"

    # Act
    response = api_client.get(endpoint)
    posts = response.json()

    # Assert
    assert posts


@pytest.mark.smoke
def test_get_post_with_valid_id_validates_schema(
    api_client: APIClient,
) -> None:
    """Verify that retrieving a valid post ID matches the Post schema.

    Args:
        api_client: Shared API client fixture from conftest.py.
    """
    # Arrange
    endpoint = "/posts/1"

    # Act
    response = api_client.get(endpoint)

    # Assert
    assert Post(**response.json())


@pytest.mark.regression
def test_get_post_with_invalid_id_returns_404(
    api_client: APIClient,
) -> None:
    """Verify that retrieving an invalid post ID returns HTTP 404.

    Args:
        api_client: Shared API client fixture from conftest.py.
    """
    # Arrange
    endpoint = "/posts/99999"

    # Act
    response = api_client.get(endpoint)

    # Assert
    assert response.status_code == 404


@pytest.mark.regression
def test_create_post_with_valid_payload_returns_201(
    api_client: APIClient,
) -> None:
    """Verify that creating a post with valid data returns HTTP 201.

    Args:
        api_client: Shared API client fixture from conftest.py.
    """
    # Arrange
    payload = PostCreate(title="Test post", body="Content", user_id=1)

    # Act
    response = api_client.post("/posts", json=payload.model_dump(by_alias=True))

    # Assert
    assert response.status_code == 201


@pytest.mark.regression
def test_update_post_with_valid_payload_returns_200(
    api_client: APIClient,
) -> None:
    """Verify that updating a post with valid data returns HTTP 200.

    Args:
        api_client: Shared API client fixture from conftest.py.
    """
    # Arrange
    payload = Post(id=1, title="Updated post", body="Updated content", user_id=1)

    # Act
    response = api_client.put("/posts/1", json=payload.model_dump(by_alias=True))

    # Assert
    assert response.status_code == 200


@pytest.mark.regression
def test_delete_post_with_valid_id_returns_200(
    api_client: APIClient,
) -> None:
    """Verify that deleting a valid post ID returns HTTP 200.

    Args:
        api_client: Shared API client fixture from conftest.py.
    """
    # Arrange
    endpoint = "/posts/1"

    # Act
    response = api_client.delete(endpoint)

    # Assert
    assert response.status_code == 200
