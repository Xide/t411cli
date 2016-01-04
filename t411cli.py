#!/usr/bin/env python3
"""
Command line entry point
"""


from configuration import Configuration, from_env, CONF
from API import T411API
from API import ConnectionError, ServiceError, APIError
import functions
import argparse


def get_args_parser():
    """
    Get command line argument parser, crafted with argparse module
    :return: parser object
    """
    parser = argparse.ArgumentParser(prog='t411')
    # group = parser.add_mutually_exclusive_group(required=True)
    subparsers = parser.add_subparsers(help='sub-command help', dest='command')

    search = subparsers.add_parser('search', help='search for a torrent')
    details = subparsers.add_parser('details', help='Get details for a specific torrent')
    download = subparsers.add_parser('download', help='Download a torrent file')

    parser.add_argument('-c', '--configuration', help='Custom configuration file path')
    parser.add_argument('-l', '--limit', type=int, help='Maximum number of fetched torrent at once')
    parser.add_argument('-u', '--username', type=str, help='T411 username ( override configuration )')
    parser.add_argument('-p', '--password', type=str, help='T411 password ( override configuration )')

    search.add_argument('query', type=str, help='String to search for')

    details.add_argument('torrentID', type=int, help='ID of the torrent')

    download.add_argument('torrentID', type=int, help='ID of the torrent')
    download.add_argument('name', type=str, nargs='?', help='Optional torrent filename')
    download.add_argument('--cmd', type=str, help='Command to invoke upon torrent completion \
    (torrent file is available with bash $torrent variable)')
    return parser


def check_arguments(args):
    """
    TODO: Check for argument validity ?
    :param args:
    :return:
    """
    pass


def main():
    global CONF
    parser = get_args_parser()
    args = parser.parse_args()
    ftab = {
        'search': functions.search,
        'download': functions.download,
        'details': functions.details
    }

    # CLI argument override configuration file
    CONF = from_env(args.username, args.password)
    if args.username:
        CONF['account']['username'] = args.username
    if args.password:
        CONF['account']['password'] = args.password
    if args.limit:
        CONF['config']['limit'] = str(args.limit)

    elif not args.command:
        parser.print_usage()
        return
    api = T411API()

    try:
        api.connect(CONF['account']['username'], CONF['account']['password'])
    except ConnectionError as e:
        print('[Error] Connection error :', e)
    except ServiceError as e:
        print('[Error] Service error :', e)
    else:
        try:
            # Command execution (search/download/...)
            ftab[args.command](api, CONF, args)
        except APIError as e:
            print('[Error] API failed :', e)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('\nOkay, fine, see ya')
