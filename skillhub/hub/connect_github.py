from github.OAuth import OAuth

from hub.models import Account
from settings import GITHUB_CLIENT_ID, GITHUB_CLIENT_SECRET


class ConnectGitHub(object):

    oauth = OAuth(client_id=GITHUB_CLIENT_ID, client_secret=GITHUB_CLIENT_SECRET)

    def authorize_url(self):
        return self.oauth.authorize_url()

    def authorize(self, code):
        token = self.oauth.get_access_token(code)
        account = Account(github_token=token)
        account.save()
        return account
