"""HTTP client wrapper for JSONPlaceholder API tests."""

from typing import Any

import requests


class APIClient:
    """Client for making requests against the JSONPlaceholder API.

    Args:
        base_url: Base URL for the API under test.
    """

    def __init__(self, base_url: str) -> None:
        """Initialize the API client.

        Args:
            base_url: Base URL for the API under test.
        """
        self.base_url = base_url
        self.session = requests.Session()

    def get(self, endpoint: str, **kwargs: Any) -> requests.Response:
        """Send a GET request to the given endpoint.

        Args:
            endpoint: API endpoint path.
            **kwargs: Additional keyword arguments passed to requests.

        Returns:
            HTTP response from the API.
        """
        return self.session.get(f"{self.base_url}{endpoint}", **kwargs)

    def post(
        self,
        endpoint: str,
        json: dict[str, Any],
        **kwargs: Any,
    ) -> requests.Response:
        """Send a POST request to the given endpoint.

        Args:
            endpoint: API endpoint path.
            json: JSON payload for the request body.
            **kwargs: Additional keyword arguments passed to requests.

        Returns:
            HTTP response from the API.
        """
        return self.session.post(f"{self.base_url}{endpoint}", json=json, **kwargs)

    def put(
        self,
        endpoint: str,
        json: dict[str, Any],
        **kwargs: Any,
    ) -> requests.Response:
        """Send a PUT request to the given endpoint.

        Args:
            endpoint: API endpoint path.
            json: JSON payload for the request body.
            **kwargs: Additional keyword arguments passed to requests.

        Returns:
            HTTP response from the API.
        """
        return self.session.put(f"{self.base_url}{endpoint}", json=json, **kwargs)

    def delete(
        self,
        endpoint: str,
        **kwargs: Any,
    ) -> requests.Response:
        """Send a DELETE request to the given endpoint.

        Args:
            endpoint: API endpoint path.
            **kwargs: Additional keyword arguments passed to requests.

        Returns:
            HTTP response from the API.
        """
        return self.session.delete(f"{self.base_url}{endpoint}", **kwargs)
