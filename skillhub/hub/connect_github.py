import urllib

from github.Requester import Requester

from hub.models import Account
from settings import (GITHUB_CLIENT_ID, GITHUB_CLIENT_SECRET, DEFAULT_TIMEOUT,
    DEFAULT_USER_AGENT, GITHUB_BASE_URL, GITHUB_AUTHORIZE_URL, GITHUB_TOKEN_URL)


class ConnectGitHub(object):

    def __init__(self, client_id=GITHUB_CLIENT_ID, client_secret=GITHUB_CLIENT_SECRET):
        self.client_id = client_id
        self.client_secret = client_secret

        self.requester = Requester(
            client_id=self.client_id, client_secret=self.client_secret,
            base_url=GITHUB_BASE_URL, login_or_token=None, password=None,
            timeout=DEFAULT_TIMEOUT, user_agent=DEFAULT_USER_AGENT, per_page=10,
            api_preview=False)

    def authorize_url(self, **kwargs):
        """First step of the authentication process -
            Redirect user to request GitHub access.
        """
        kwargs.update({'client_id': self.client_id})
        return GITHUB_AUTHORIZE_URL + "?" + urllib.urlencode(kwargs)

    def get_access_token(self, code):
        """Second step of the authentication process -
            GitHub redirects back to your site.
        A temporary `code` is given after the first step is successfully
        completed. Use the code to request an access token for the user.

        """
        params = {'client_id': self.client_id,
                  'client_secret': self.client_secret,
                  'code': code}
        headers, data = self.requester.requestJsonAndCheck(
            verb="POST", url=GITHUB_TOKEN_URL, parameters=params)

        return data['data'].split('&')[0].split('=')[-1]
