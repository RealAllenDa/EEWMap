"""
 EEWMap - API - Tsunami - Get_Tsunami
 Gets JMA XML.
"""
import traceback

from config import PROXY
from modules.sdk import make_web_request
from .parse_jma_tsunami import parse_jma_tsunami


def get_jma_tsunami(app):
    """
    Gets the JMA tsunami info.

    :param app: The Flask app instance
    """
    try:
        response = make_web_request(url="http://www.data.jma.go.jp/developer/xml/feed/eqvol.xml",
                                proxies=PROXY, timeout=5)
        if not response[0]:
            app.logger.warn(f"Failed to fetch JMA XML data: {response[1]}.")
            return
    except:
        app.logger.warn("Failed to fetch JMA XML data. Exception occurred: \n" + traceback.format_exc())
        return
    parse_jma_tsunami(response[1], app)
