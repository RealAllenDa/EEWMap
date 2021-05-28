def response_verify(resp):
    """
     Verify if the response's status code is 200 or not.

     :return: True if response code is 200.
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
