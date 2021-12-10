"""
 EEWMap - Modules - SDK
 HN-Python-SDK ver1.0
"""
from typing import Tuple, Union, Any

import requests
from requests import Response


def _response_verify(resp: Response) -> bool:
    """
     Verify if the response's status code is 200 or not.

     :return: True if response code is 200
     :rtype: bool
    """
    if resp.status_code != 200 or resp.text == "":
        return False
    else:
        return True


def generate_list(name: Any) -> list:
    """
    Make sure parameters xmltodict generates is a list.

    :param name: The dict/list that xmltodict gives
    :return: Guaranteed a list
    :rtype: list
    """
    if not name:
        return []
    elif isinstance(name, list):
        return name
    else:
        return [name]


# noinspection PyProtectedMember
def relpath(file: str) -> str:
    """
    Always locate to the correct relative path.

    :param file: The wanted-to-get file location
    :return: An absolute path to the file requested
    """
    from sys import _getframe
    from pathlib import Path
    frame = _getframe(1)
    curr_file = Path(frame.f_code.co_filename)
    return str(curr_file.parent.joinpath(file).resolve())


def make_web_request(url: str,
                     proxies: Union[None, dict] = None,
                     timeout: Union[int, float] = None,
                     to_json: bool = False) -> Tuple[bool, Union[Response, Any]]:
    """
    Makes web requests to API, URL, etc.

    :param url: The URL to get
    :param proxies: The proxy information
    :param timeout: The timeout
    :param to_json: Whether to return it as JSON or not
    :return: Raw response if to_json is False; JSON if to_json is True
    """
    try:
        response = requests.get(url=url, proxies=proxies, timeout=timeout)
        response.encoding = 'utf-8'
        if not _response_verify(response):
            return False, f"Failed response verifying (code={response.status_code})."
        return True, response.json() if to_json else response
    except Exception as e:
        return False, f"Exception occurred: {e}."
