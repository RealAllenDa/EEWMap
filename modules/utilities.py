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