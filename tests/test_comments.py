"""Tests for the JSONPlaceholder comments endpoint."""

import pytest

from api_testing_suite.client import APIClient
from api_testing_suite.models import Comment


@pytest.mark.regression
def test_get_comments_list_returns_200(
    api_client: APIClient,
) -> None:
    """Verify that retrieving comments returns HTTP 200.

    Args:
        api_client: Shared API client fixture from conftest.py.
    """
    # Arrange
    endpoint = "/comments"

    # Act
    response = api_client.get(endpoint)

    # Assert
    assert response.status_code == 200


@pytest.mark.regression
def test_get_comments_list_with_default_query_returns_non_empty_list(
    api_client: APIClient,
) -> None:
    """Verify that retrieving comments with default query returns non-empty data.

    Args:
        api_client: Shared API client fixture from conftest.py.
    """
    # Arrange
    endpoint = "/comments"

    # Act
    response = api_client.get(endpoint)
    comments = response.json()

    # Assert
    assert comments


@pytest.mark.regression
def test_get_comments_filtered_by_post_id_returns_200(
    api_client: APIClient,
) -> None:
    """Verify that filtering comments by post ID returns HTTP 200.

    Args:
        api_client: Shared API client fixture from conftest.py.
    """
    # Arrange
    post_id = 1
    endpoint = "/comments"

    # Act
    response = api_client.get(endpoint, params={"postId": post_id})

    # Assert
    assert response.status_code == 200


@pytest.mark.regression
def test_get_comments_filtered_by_post_id_returns_only_matching_post_ids(
    api_client: APIClient,
) -> None:
    """Verify that filtered comments contain only the requested post ID.

    Args:
        api_client: Shared API client fixture from conftest.py.
    """
    # Arrange
    post_id = 1
    endpoint = "/comments"

    # Act
    response = api_client.get(endpoint, params={"postId": post_id})
    returned_post_ids = {comment["postId"] for comment in response.json()}

    # Assert
    assert returned_post_ids == {post_id}


@pytest.mark.regression
@pytest.mark.parametrize("comment_id", [1, 5, 10], ids=["1", "5", "10"])
def test_get_comment_with_valid_id_returns_200(
    api_client: APIClient,
    comment_id: int,
) -> None:
    """Verify that retrieving a valid comment ID returns HTTP 200.

    Args:
        api_client: Shared API client fixture from conftest.py.
        comment_id: Valid comment ID to retrieve.
    """
    # Arrange
    endpoint = f"/comments/{comment_id}"

    # Act
    response = api_client.get(endpoint)

    # Assert
    assert response.status_code == 200


@pytest.mark.regression
def test_get_comment_with_valid_id_validates_schema(
    api_client: APIClient,
) -> None:
    """Verify that retrieving a valid comment ID matches the Comment schema.

    Args:
        api_client: Shared API client fixture from conftest.py.
    """
    # Arrange
    endpoint = "/comments/1"

    # Act
    response = api_client.get(endpoint)

    # Assert
    assert Comment(**response.json())
