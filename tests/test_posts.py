"""Tests for the JSONPlaceholder posts endpoint."""

import pytest

from api_testing_suite.client import APIClient


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
