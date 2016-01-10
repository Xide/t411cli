"""
T411 API wrapper
May throw APIError -> (ConnectError, ServiceError)
"""

import os

import requests

from t411cli import helpers

try:
    from simplejson.scanner import JSONDecodeError
except (ImportError, SyntaxError):
    from json import JSONDecodeError

API_URL = 'http://api.t411.in'


class APIError(Exception):
    """
    Exception thrown upon an unknow API error
    Base class for every API exceptions
    """
    pass


class ConnectError(APIError):
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
        """
        Connect to the T411 service
        May raise a ServiceError or a ConnectError
        :param username: T411 username
        :param password: user password (in plain text)
        :return: Nothing
        """
        try:
            r = requests.post(API_URL + '/auth', data={
                'username': username,
                'password': password,
            })
        except Exception as e:
            # Broad clause, might change in the future, but not yet
            # useful
            raise ConnectError('Could not connect to API server: %s' % e)
        if r.status_code != 200:
            raise ServiceError('Unexpected HTTP code %d upon connection'
                               % r.status_code)
        try:
            response = r.json()
        except JSONDecodeError:
            raise ServiceError('Unexpected non-JSON API response : %s' % r.content)

        if 'token' not in response.keys():
            raise ConnectError('Unexpected T411 error : %s (%d)'
                               % (response['error'], response['code']))
        self.token = response['token']
        self.uid = int(response['uid'])

    def _raw_query(self, path, params):
        """
        Wraps API communication, with token and
         HTTP error code handling
        :param path: url to query
        :param params: http request parameters
        :return: Response object
        """
        if not self.token:
            raise ConnectError('You must be logged in to use T411 API')

        if not params:
            params = {}

        r = requests.get(API_URL + path, params,
                         headers={'Authorization': self.token})

        if r.status_code != 200:
            raise ServiceError('Unexpected HTTP code %d upon connection'
                               % r.status_code)
        return r

    def _query(self, path, params=None):
        """
        Handle API response and errors
        :param path:
        :param params:
        :return:
        """
        r = self._raw_query(path, params)
        try:
            response = r.json()
        except JSONDecodeError as e:
            raise ServiceError('Unexpected non-JSON response from T411: %s'
                               % r.content if r else 'response is None')

        if isinstance(response, int):
            return response
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

    def top(self, tp: str):
        """
        return T411 top torrents
        :param tp: one of '100', 'day', 'week', 'month'
        :return:
        """
        ctab = {
            '100': '/torrents/top/100',
            'day': '/torrents/top/today',
            'week': '/torrents/top/week',
            'month': '/torrents/top/month'
        }
        if tp not in ctab.keys():
            raise ValueError('Incorrect top command parameter')
        return self._query(ctab[tp])

    def categories(self):
        return self._query('/categories/tree')

    def download(self, torrent_id: int, filename: str = '', base: str = ''):
        """
        Download torrent on filesystem
        :param torrent_id:
        :param filename: torrent file name
        :param base: directory to put torrent into
        :return:
        """
        if not filename:
            details = self.details(torrent_id)
            filename = helpers.sanitize(details['name'])
        if not base:
            base = os.getcwd()
        if not filename.endswith('.torrent'):
            filename += '.torrent'
        with open(os.path.join(base, filename), 'wb') as out:
            raw = self._raw_query('/torrents/download/%d' % torrent_id, {})
            out.write(raw.content)
        return os.path.join(base, filename)

    def search(self, query: str, **kwargs):
        """
        Search for a torrent, results are unordered
        :param query:
        :param kwargs:
        :return:
        """

        params = {
            'offset': 0,
        }

        params.update(kwargs)
        response = self._query('/torrents/search/' + query, params)
        return response

    def bookmarks(self):
        """
        retrieve list of user bookmarks
        :return:
        """
        return self._query('/bookmarks')

    def add_bookmark(self, torrent_id: int):
        """
        Add a new bookmark
        :param torrent_id:
        :return: number of torrents added
        """
        return self._query('/bookmarks/save/%d' % torrent_id)

    def del_bookmark(self, *args):
        """
        Remove a bookmark
        :param args: tuple of torrent id's
        :return: Number of torrents deleted
        """
        query = ','.join([str(i) for i in args])
        return self._query('/bookmarks/delete/%s' % query)

    def user(self, uid: int = None):
        """
        Get stats about an user
        :param uid: user id
        :return:
        """
        if not uid:
            uid = self.uid
        user = self._query('/users/profile/%d' % uid)
        if 'uid' not in user:
            user['uid'] = uid
        return user
