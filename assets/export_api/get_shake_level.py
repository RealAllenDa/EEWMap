import requests
import time
from assets.earthquake_info import response_verify
from assets.config import proxies

def get_shake_level():
    """
     Get the shaking level.
    """
    try:
        response = requests.get(url="http://kwatch-24h.net/EQLevel.json?" + str(int(time.time())),
                                timeout=3.5, proxies=proxies)
        response.encoding = 'utf-8'
        if not response_verify(response):
            return {"status": -1}
    except:
        return {"status": -1}
    return {"status": 0, "shake_level": response.json()["l"]}

