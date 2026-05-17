"""Tests for the JSONPlaceholder users endpoint."""

import pytest

from api_testing_suite.client import APIClient
from api_testing_suite.models import User


@pytest.mark.smoke
def test_get_users_list_returns_200(
    api_client: APIClient,
) -> None:
    """Verify that retrieving users returns HTTP 200.

    Args:
        api_client: Shared API client fixture from conftest.py.
    """
    # Arrange
    endpoint = "/users"

    # Act
    response = api_client.get(endpoint)

    # Assert
    assert response.status_code == 200


@pytest.mark.smoke
def test_get_users_list_with_default_query_returns_non_empty_list(
    api_client: APIClient,
) -> None:
    """Verify that retrieving users with default query returns non-empty data.

    Args:
        api_client: Shared API client fixture from conftest.py.
    """
    # Arrange
    endpoint = "/users"

    # Act
    response = api_client.get(endpoint)
    users = response.json()

    # Assert
    assert users


@pytest.mark.smoke
@pytest.mark.parametrize("user_id", [1, 5, 10], ids=["1", "5", "10"])
def test_get_user_with_valid_id_returns_200(
    api_client: APIClient,
    user_id: int,
) -> None:
    """Verify that retrieving a valid user ID returns HTTP 200.

    Args:
        api_client: Shared API client fixture from conftest.py.
        user_id: Valid user ID to retrieve.
    """
    # Arrange
    endpoint = f"/users/{user_id}"

    # Act
    response = api_client.get(endpoint)

    # Assert
    assert response.status_code == 200


@pytest.mark.smoke
def test_get_user_with_valid_id_validates_schema(
    api_client: APIClient,
) -> None:
    """Verify that retrieving a valid user ID matches the User schema.

    Args:
        api_client: Shared API client fixture from conftest.py.
    """
    # Arrange
    endpoint = "/users/1"

    # Act
    response = api_client.get(endpoint)

    # Assert
    assert User(**response.json())


@pytest.mark.regression
def test_get_user_with_invalid_id_returns_404(
    api_client: APIClient,
) -> None:
    """Verify that retrieving an invalid user ID returns HTTP 404.

    Args:
        api_client: Shared API client fixture from conftest.py.
    """
    # Arrange
    endpoint = "/users/99999"

    # Act
    response = api_client.get(endpoint)

    # Assert
    assert response.status_code == 404
