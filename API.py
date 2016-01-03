import requests
import os

API_URL = 'http://api.t411.in'

class APIError(Exception):
    """
    Exception thrown upon an unknow API error
    Base class for every API exceptions
    """
    pass

class ConnectionError(APIError):
    """
    Exception thrown when an error occur
    on client side ( most likely receivable error )
    """
    pass

class ServiceError(APIError):
    """
    Exception thrown when T411 service encounter an error
    """
    pass


class T411API:
    def __init__(self):
        self.token = None
        self.uid = None

    def connect(self, username: str, password: str):
        r = requests.post(API_URL + '/auth', data={
            'username': username,
            'password': password,
        })

        if r.status_code != 200:
            raise ServiceError('Unexpected HTTP code %d upon connection'
                               % r.status_code)
        response = r.json()
        if 'token' not in response.keys():
            raise ConnectionError('Unexpected T411 error : %s (%d)'
                                  % (response['error'], response['code']))
        self.token= response['token']

    def _raw_query(self, path, params):
        if not self.token:
            raise ConnectionError('You must be logged in to use T411 API')

        if not params:
            params = {}

        r = requests.get(API_URL + path, params, headers={'Authorization': self.token})
        if r.status_code != 200:
            raise ServiceError('Unexpected HTTP code %d upon connection'
                               % r.status_code)
        return r

    def _query(self, path, params=None):
        r = self._raw_query(path, params)
        response = r.json()
        if 'error' in response:
            raise ServiceError('Unexpected T411 error : %s (%d)'
                               % (response['error'], response['code']))
        return response

    def details(self, torrent_id: int):
        """
        Return details of the torrent
        :param torrent_id: id of the torrent (can be found with search)
        :return: JSON  sample: {
            "id":123,
            "name":"Very scary movie",
            "rewriteName":"very-scary-movie",
            "category":12,
            "categoryName":"Movie",
            "terms":{
                "video quality":"1080p"
            }
        }
        """
        return self._query('/torrents/details/%d' % torrent_id)

    def download(self, torrent_id: int, filename: str ='', base: str =''):
        """
        Download torrent on filesystem
        :param torrent_id:
        :param filename: torrent file name
        :param base: directory to put torrent into
        :return:
        """
        if not filename:
            details = self.details(torrent_id)
            filename = details['name']
        if not base:
            base = os.getcwd()
        if not filename.endswith('.torrent'):
            filename += '.torrent'
        with open(os.path.join(base, filename), 'w') as out:
            raw = self._raw_query('/torrents/download/%d' % torrent_id, {})
            out.write(raw.text)
        return os.path.join(base, filename)

    def search(self, query: str, **kwargs):
        params = {
            'offset': 0,
        }

        params.update(kwargs)
        response = self._query('/torrents/search/' + query, params)
        return response
