"""
 EEWMap - Modules - Utilities
 The utilities for the whole project.
"""
def response_verify(resp):
    """
     Verify if the response's status code is 200 or not.

     :return: True if response code is 200
     :rtype: bool
    """
    if resp.status_code != 200 or resp.text == "":
        return False
    else:
        return True


def generate_list(name):
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
def relpath(file):
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
