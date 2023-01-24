"""Api Client class."""
# Standard Library Imports
from urllib3.util.retry import Retry

# Third Party Imports
import requests
from requests.adapters import HTTPAdapter

# Local App Imports


class ApiClient:
    def __init__(self, base_url: str, headers: dict[str, str] | None = None, max_retries: int = 3):
        self.session = requests.Session()
        self.base_url = base_url
        self.headers = headers
        retry = Retry(total=max_retries, backoff_factor=0.1, status_forcelist=[500, 502, 503, 504])
        adapter = HTTPAdapter(max_retries=retry)
        self.session.mount("http://", adapter)
        self.session.mount("https://", adapter)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.session.close()

    def get(self, endpoint: str) -> dict | None:
        url = f"{self.base_url}{endpoint}"
        response = self.session.get(url, headers=self.headers)
        response.raise_for_status()
        return response.json()

    def post(self, endpoint: str, data: dict | None) -> dict | None:
        url = f"{self.base_url}{endpoint}"
        response = self.session.post(url, headers=self.headers, data=data)
        response.raise_for_status()
        return response.json()

    def put(self, endpoint: str, data: dict | None) -> dict | None:
        url = f"{self.base_url}{endpoint}"
        response = self.session.put(url, headers=self.headers, data=data)
        response.raise_for_status()
        return response.json()

    def delete(self, endpoint: str) -> dict | None:
        url = f"{self.base_url}{endpoint}"
        response = self.session.delete(url, headers=self.headers)
        response.raise_for_status()
        return response.json()

    def close(self):
        self.session.close()
