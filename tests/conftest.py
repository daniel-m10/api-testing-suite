"""Shared pytest fixtures for API tests."""

import pytest

from api_testing_suite.client import APIClient


@pytest.fixture(scope="session")
def base_url() -> str:
    """Provide the base URL for JSONPlaceholder API."""
    return "https://jsonplaceholder.typicode.com"


@pytest.fixture(scope="session")
def api_client(base_url: str) -> APIClient:
    """Provide a shared API client for the entire test session.

    Args:
        base_url: Base URL for JSONPlaceholder API.
    """
    return APIClient(base_url=base_url)
