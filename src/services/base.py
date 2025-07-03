import requests
from pathlib import Path
from contextlib import ExitStack

from utils.debug import error_handler


class APIClient:
    """Lightweight API client to handle requests"""

    def __init__(self, base_url: str, timeout: tuple[int, int] = (5, 10)):
        self.base_url = base_url
        self.timeout = timeout
        self.base_headers = {"Content-Type": "application/json"}
        self.file_headers = {"Accept": "application/json"}
        self.session = requests.Session()

    @error_handler()
    def get(
        self,
        endpoint: str,
        headers: dict[str, str] = None,
        params: dict[str, any] = None,
    ) -> any:
        """Handles GET requests"""
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        combined_headers = {**self.base_headers, **(headers or {})}
        try:
            response = self.session.get(
                url, headers=combined_headers, params=params, timeout=self.timeout
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.JSONDecodeError as e:
            return response.status_code
        except requests.RequestException as e:
            raise requests.RequestException(f"GET request to {url} failed: {e}")

    @error_handler()
    def post(
        self, endpoint: str, data: dict[str, any] = None, headers: dict[str, str] = None
    ) -> any:
        """Handles POST requests"""
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        combined_headers = {**self.base_headers, **(headers or {})}
        try:
            response = self.session.post(
                url, json=data, headers=combined_headers, timeout=self.timeout
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.JSONDecodeError as e:
            return response.status_code
        except requests.RequestException as e:
            raise requests.RequestException(f"POST request to {url} failed: {e}")

    @error_handler()
    def post_files(
        self,
        endpoint: str,
        file_path_list: dict[str, Path],
        data: dict[str, any] = None,
        headers: dict[str, str] = None,
    ) -> any:
        """Handles POST requests with a file upload"""
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        combined_headers = {**self.file_headers, **(headers or {})}

        try:
            # Use ExitStack to manage multiple file context managers
            with ExitStack() as stack:
                files = {
                    key: stack.enter_context(open(path, "rb"))
                    for key, path in file_path_list.items()
                }
                response = self.session.post(
                    url,
                    files=files,
                    data=data,
                    headers=combined_headers,
                    timeout=self.timeout,
                )
                response.raise_for_status()
                return response.json()
        except requests.exceptions.JSONDecodeError as e:
            return response.status_code
        except requests.RequestException as e:
            raise requests.RequestException(f"POST file request to {url} failed: {e}")
