import requests
import logging
from urllib.parse import urljoin

logger = logging.getLogger()

# Surpress warnings 'Unverified HTTPS request is being made"
requests.packages.urllib3.disable_warnings()


class API:

    session = requests.Session()

    def __init__(self, url, user=None, password=None):
        self.url = url
        if user and password:
            self.session.auth = (user, password)

    def request(self, method, endpoint, **kwargs):
        params = {}
        if kwargs is not None:
            for key, value in kwargs.items():
                params[key] = value

        full_url = urljoin(self.url, endpoint)
        logger.debug('{0} to {1}'.format(method, full_url))
        response = self.session.request(method, full_url, params=params)
        response.raise_for_status()
        content = response.json()
        logger.info('Got response from {}: {}'.format(self.url, content))
        if not content['ok']:
            logger.error('API returned error: {}'.format(content['description']))
        return content['result']

    def get(self, endpoint, **kwargs):
        return self.request('GET', endpoint, **kwargs)

    def post(self, endpoint, **kwargs):
        return self.request('POST', endpoint, **kwargs)

    def get_updates(self, **kwargs):
        return self.get('getUpdates', **kwargs)

    def send_message(self, chat_id, text, **kwargs):
        return self.post('sendMessage', chat_id=chat_id, text=text, **kwargs)
