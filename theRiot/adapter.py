import requests
import requests.packages
from typing import List, Dict
from json import JSONDecodeError
from models import Result
import logging
from exception import RiotException

class adapter:
    def __init__(self, hostname: str, api_key: str = 'RGAPI-685f2a3d-4044-4da1-a04c-1df556720d98', ver: str = 'v1', ssl_verify: bool = True, logger: logging.Logger=None):
        self.url = "https://{}/{}/".format(hostname, ver)
        self._api_key = api_key
        self._ssl_verify = ssl_verify
        if not ssl_verify:
            # noinspection PyUnresolvedReferences
            requests.packages.urllib3.disable_warnings()
        self._logger = logger or logging.getLogger(__name__)

    def _do(self, http_method: str, endpoint: str, ep_params: Dict = None, data: Dict = None) -> Result:
        full_url = self.url + endpoint
        headers = {'x-api-key': self._api_key}
        try:
            response = requests.request(method=http_method, url=full_url, verify=self._ssl_verify, 
                                    headers=headers, params=ep_params, json=data)
        except requests.exceptions.RequestException as e:
            raise RiotException("Request failed") from e
        data = response.json()
        if response.status_code >= 200 and response.status_code <= 299:     # OK
            return data
        raise Exception(data["message"])
        

    def get(self, endpoint: str, ep_params: Dict = None) -> List[Dict]:
        return self._do(http_method='GET', endpoint=endpoint, ep_params=ep_params)

    def post(self, endpoint: str, ep_params: Dict = None, data: Dict = None) -> Result:
        return self.do(http_method='POST', endpoint=endpoint, ep_params=ep_params, data=data)

    def delete(self, endpoint: str, ep_params: Dict = None, data: Dict = None) -> Result:
        return self.do(http_method='DELETE', endpoint=endpoint, ep_params=ep_params, data=data)
    