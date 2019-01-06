from google_auth_oauthlib.flow import InstalledAppFlow

import requests


class YoutubeAPI:
    def __init__(self):
        self._access_token = None
        self._base_url = 'https://www.googleapis.com/youtube/v3/'
        self._api_key = None

    def authorize(self, client_secret_json_path, scopes):
        flow = InstalledAppFlow.from_client_secrets_file(client_secret_json_path, scopes=scopes)
        credentials = flow.run_console()
        self._access_token = credentials.token

    def get(self, endpoint, **kwargs):
        if self._access_token is None:
            if self._api_key is None:
                print('Need api key')
            else:
                kwargs['api_key'] = self._api_key
        else:
            kwargs['access_token'] = self._access_token
        kwargs['part'] = 'snippet, id'
        return self._get(self._base_url + endpoint, params=kwargs)

    def post(self, endpoint, body=None, **kwargs):
        if self._access_token is None:
            if self._api_key is None:
                print('Need api key')
            else:
                kwargs['api_key'] = self._api_key
        else:
            kwargs['access_token'] = self._access_token
        kwargs['part'] = 'snippet, id'

        return self._post(self._base_url + endpoint, params=kwargs, body=body)

    def delete(self, endpoint, **kwargs):
        if self._access_token is None:
            print('You need an access token to delete')
        else:
            kwargs['access_token'] = self._access_token
            return self._delete(self._base_url + endpoint, params=kwargs)

    @staticmethod
    def _get(url, params=None):
        response = requests.get(url, params=params)
        return response

    @staticmethod
    def _post(url, params=None, body=None):
        response = requests.post(url, params=params, json=body)
        return response

    @staticmethod
    def _delete(url, params=None):
        response = requests.delete(url, params=params)
        return response