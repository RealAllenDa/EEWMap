"""
 EEWMap - Modules - SDK
 HN-Python-SDK ver1.2
"""
import dataclasses
import re
import time
from typing import Tuple, Union, Any, TypeVar, Optional, Literal

import requests
from requests import Response

_R = TypeVar("_R")


class Errors:
    NO_INFO_AVAIL = {
        "status": -1,
        "info": "API not yet ready / no information available"
    }
    INFO_INCORRECT_STRUCTURE = {
        "status": -1,
        "info": "API internal structure error"
    }


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


def parse_jsonp(jsonp_str: str) -> str:
    """
    Parses the jsonp string into a json string.
    :param jsonp_str: JSONP string
    :return: JSON String
    """
    try:
        return re.search('^[^(]*?\((.*)\)[^)]*$', jsonp_str).group(1)
    except Exception:
        return "Invalid JSONP"


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
                     proxies: Optional[dict] = None,
                     timeout: Union[int, float] = 3.5,
                     add_time: bool = False,
                     to_json: bool = False,
                     to_dataclass: Optional[_R] = None,
                     verify: bool = True) \
        -> Union[
            Tuple[Literal[True], Union[Response, _R, dict]],
            Tuple[Literal[False], str]
        ]:
    """
    Makes web requests to API, URL, etc.

    :param url: The URL to get
    :param proxies: The proxy information
    :param timeout: The timeout
    :param add_time: Whether to add time after the url
    :param to_json: Whether to return it as JSON
    :param to_dataclass: whether to decode to a dataclass
    :param verify: Whether to verify the certificate
    :return: Raw response if to_json is False; JSON if to_json is True
    """
    try:
        if add_time:
            url += f"?time={int(time.time())}"
        response = requests.get(url=url,
                                proxies=proxies,
                                timeout=timeout,
                                verify=verify)
        response.encoding = 'utf-8'
        if not _response_verify(response):
            return False, f"Failed response verifying (code={response.status_code})"
        if to_dataclass:
            if not dataclasses.is_dataclass(to_dataclass):
                return False, f"Arguments passed in was not a dataclass " \
                              f"but a {type(to_dataclass)}"
            else:
                try:
                    return True, to_dataclass.from_json(response.text)
                except Exception as e:
                    return False, f"Failed to deserialize to a dataclass: {e}"
        elif to_json:
            return True, response.json()
        else:
            return True, response
    except Exception as e:
        return False, f"Exception occurred: {e}"


def api_return(dataclass: Union[None, _R]) -> dict:
    if dataclass is None:
        return Errors.NO_INFO_AVAIL
    elif not dataclasses.is_dataclass(dataclass):
        return Errors.INFO_INCORRECT_STRUCTURE
    else:
        return dataclass.to_dict()
