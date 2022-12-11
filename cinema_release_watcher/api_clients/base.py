from typing import Any, Callable, Union, Optional

import requests


class BaseJsonRestClient:
    def __init__(self, config_: dict[str, Union[str, int]]):
        self._config = config_

    def _request(self, method: Callable[..., requests.Response], path: str, **kwargs) -> requests.Response:

        return method(f'{self._config["base_url"]}/{path}', **kwargs)

    def _get(self, path: str, query_parameters: Optional[dict[str, Any]] = None) -> requests.Response:
        return self._request(requests.get, path, params=query_parameters)

    def _put(self, path: str, data: dict[Any, Any], query_parameters: Optional[dict[str, Any]] = None) \
            -> requests.Response:
        return self._request(requests.put, path, data=data, params=query_parameters)

    def _post(self, path: str, data: dict[Any, Any], query_parameters: Optional[dict[str, Any]] = None) \
            -> requests.Response:
        return self._request(requests.post, path, data=data, params=query_parameters)

    def _delete(self, path: str, query_parameters: Optional[dict[str, Any]] = None):
        self._request(requests.get, path, params=query_parameters)
