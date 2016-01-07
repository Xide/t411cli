"""
Configuration file parser
"""

import configparser
import os
from getpass import getpass
from os.path import expanduser
from colorama import Fore

CONF = None


class Configuration:
    @staticmethod
    def load(path: str):
        global CONF
        CONF = configparser.ConfigParser()
        CONF.read(path)

        success, rep = Configuration.check_arguments()
        if not success:
            CONF = None
            raise ValueError('Incorrect configuration file : %s' % rep)
        return CONF

    @staticmethod
    def default_config():
        return {
            'limit': 10,
            'torrent_folder': expanduser('~') + '/Downloads',
        }

    @staticmethod
    def check_arguments():
        global CONF
        try:
            assert 'account' in CONF,\
                'Invalid configuration file :\
                 account information section is missing'

            for entry in ['password', 'username']:
                assert entry in CONF['account'].keys(), \
                    'Section account entry missing : %s' % entry

            if not CONF['account']['username'] or \
                    not CONF['account']['password']:
                raise AssertionError('Username/Password must not be empty')

            if not CONF['config']:
                CONF['config'] = Configuration.default_config()
            assert int(CONF['config']['limit']) > 0, \
                'torrent limit must be a positive integer'
        except AssertionError as e:
            return False, str(e)
        else:
            return True, 'Success'

    @staticmethod
    def write_config(path):
        global CONF
        with open(path, 'w') as conf_file:
            CONF.write(conf_file)

    @staticmethod
    def generate_default():
        config = configparser.ConfigParser()
        config['account'] = {
            'username': '',
            'password': ''
        }
        config['config'] = Configuration.default_config()
        return config


def conf_generator(username, password):
    try:
        import readline
    except ImportError:
        pass

    conf = Configuration.generate_default()
    conf['account']['username'] = input('T411 Username: ')\
        if not username else username
    conf['account']['password'] = getpass('T411 Password: ')\
        if not password else password
    conf['config']['torrent_folder'] = \
        os.path.expanduser(input('Folder to download torrents in: '))
    return conf


def from_env(username=None, password=None, generate=True):
    """
    Try to load configuration from environment
    :param username:
    :param password:
    :param generate: if no config is found, ask the user to
    create a new one
    :return:
    """
    global CONF
    home = expanduser("~")
    if os.access('%s/.config/t411cli.conf' % home, os.R_OK | os.F_OK):
        conf = Configuration.load('%s/.config/t411cli.conf' % home)
    elif os.access('/etc/t411cli.conf', os.F_OK | os.R_OK):
        conf = Configuration.load('/etc/t411cli.conf' % home)
    else:
        print(Fore.YELLOW, 'Configuration not found', Fore.RESET)
        if generate:
            conf = conf_generator(username, password)
            with open('%s/.config/t411cli.conf' % home, 'w') as fp:
                conf.write(fp)
        else:
            conf = None
    CONF = conf
    return conf
