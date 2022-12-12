from typing import Any, Callable, Union, Optional

import requests

from cinema_release_watcher import config


class BaseJsonRestClient:
    def __init__(self, config_: dict[str, Union[str, int]]):
        self._config = config_

    def _request(
            self,
            method: Callable[..., requests.Response],
            path: str,
            status_code: Optional[int] = None,
            **kwargs
    ) -> requests.Response:
        tries_count = 0

        while True:
            response = method(f'{self._config["base_url"]}/{path}', **kwargs)
            if tries_count < config.get('http_client.max_retries') \
                    or (not status_code or response.status_code == status_code):
                break

            tries_count += 1

        return response

    def _get(
            self,
            path: str,
            query_parameters: Optional[dict[str, Any]] = None,
            status_code: Optional[int] = None
    ) -> requests.Response:
        return self._request(requests.get, path, params=query_parameters, status_code=status_code)

    def _put(
            self,
            path: str,
            data: dict[Any, Any],
            query_parameters: Optional[dict[str, Any]] = None,
            status_code: Optional[int] = None
    ) -> requests.Response:
        return self._request(requests.put, path, data=data, params=query_parameters, status_code=status_code)

    def _post(
            self,
            path: str,
            data: dict[Any, Any],
            query_parameters: Optional[dict[str, Any]] = None,
            status_code: Optional[int] = None
    ) -> requests.Response:
        return self._request(requests.post, path, data=data, params=query_parameters, status_code=status_code)

    def _delete(
            self,
            path: str,
            query_parameters: Optional[dict[str, Any]] = None,
            status_code: Optional[int] = None
    ) -> requests.Response:
        return self._request(requests.get, path, params=query_parameters, status_code=status_code)
