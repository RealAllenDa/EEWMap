import traceback

import requests

from config import PROXY
from modules.utilities import response_verify
from .parse_jma_tsunami import parse_jma_tsunami


def get_jma_tsunami(app):
    """
    Gets the JMA tsunami info.
    :param app: The Flask app instance.
    """
    try:
        response = requests.get(url="http://www.data.jma.go.jp/developer/xml/feed/eqvol.xml",
                                proxies=PROXY, timeout=5)
        response.encoding = "utf-8"
        if not response_verify(response):
            app.logger.warn("Failed to fetch JMA XML data. (response code not 200)")
            return
    except:
        app.logger.warn("Failed to fetch JMA XML data. Exception occurred: \n" + traceback.format_exc())
        return
    parse_jma_tsunami(response, app)
