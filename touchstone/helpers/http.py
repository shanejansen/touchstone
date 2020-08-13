import json
import urllib.request
from json.decoder import JSONDecodeError
from typing import Optional


def __request(url: str, method: str, body: Optional[str], headers: Optional[dict]) -> str:
    headers = headers or {}
    body = bytes(body, encoding='utf-8') if body else None
    request = urllib.request.Request(url, method=method, data=body, headers=headers)
    return urllib.request.urlopen(request).read().decode('utf-8')


def __decode_json(json_str: str) -> Optional[dict]:
    try:
        return json.loads(json_str)
    except JSONDecodeError:
        print(f'Response JSON: "{json_str}" is not valid.')
        return None


def get(url: str, headers: dict = None) -> str:
    """Makes a GET request to the specified URL."""
    return __request(url, 'GET', None, headers)


def get_json(url: str, headers: dict = None) -> dict:
    """Makes a GET request to the specified URL returning JSON."""
    return __decode_json(get(url, headers))


def post(url: str, body: str = None, headers: dict = None) -> str:
    """Makes a POST request to the specified URL with a body."""
    return __request(url, 'POST', body, headers)


def post_json(url: str, body: dict = None, headers: dict = None) -> dict:
    """Makes a POST request to the specified URL with a JSON body returning JSON."""
    headers = headers or {}
    headers['Content-type'] = 'application/json'
    return __decode_json(post(url, json.dumps(body), headers))


def put(url: str, body: str = None, headers: dict = None) -> str:
    """Makes a PUT request to the specified URL with a body."""
    return __request(url, 'PUT', body, headers)


def put_json(url: str, body: dict = None, headers: dict = None) -> dict:
    """Makes a PUT request to the specified URL with a JSON body returning JSON."""
    headers = headers or {}
    headers['Content-type'] = 'application/json'
    return __decode_json(put(url, json.dumps(body), headers))


def delete(url: str, body: str = None, headers: dict = None) -> str:
    """Makes a DELETE request to the specified URL with a body."""
    return __request(url, 'DELETE', body, headers)


def delete_json(url: str, body: dict = None, headers: dict = None) -> dict:
    """Makes a DELETE request to the specified URL with a JSON body returning JSON."""
    headers = headers or {}
    headers['Content-type'] = 'application/json'
    return __decode_json(delete(url, json.dumps(body), headers))
