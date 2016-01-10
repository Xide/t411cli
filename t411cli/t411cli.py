#!/usr/bin/env python3
"""
Command line entry point
"""

import argparse

from colorama import init, Fore

from t411cli import functions
from t411api.API import ConnectError, ServiceError, APIError
from t411api.API import T411API
from t411cli.configuration import from_env


def get_args_parser():
    """
    Get command line argument parser, crafted with argparse module
    :return: parser object
    """
    parser = argparse.ArgumentParser(prog='t411')
    subparsers = parser.add_subparsers(help='sub-command help', dest='command')

    search = subparsers.add_parser('search', help='search for a torrent')
    bookmarks = subparsers.add_parser(
            'bookmark', help='Use and manage your T411 bookmarks')
    book_subparsers = bookmarks.add_subparsers(
            help='sub-command help', dest='books')
    book_add = book_subparsers.add_parser('add', help='add a bookmark')
    book_list = book_subparsers.add_parser(
            'list', help='list your bookmarks')
    book_del = book_subparsers.add_parser(
            'del', help='delete a bookmark')
    details = subparsers.add_parser(
            'details', help='Get details for a specific torrent')
    download = subparsers.add_parser(
            'download', help='Download a torrent file')
    categories = subparsers.add_parser(
            'categories', help='Download a torrent file')
    top = subparsers.add_parser(
            'top', help='Retreive T411 current top torrents list')
    user = subparsers.add_parser('user', help='get stats about an user')

    book_del.add_argument('torrentID', type=int, help='ID of the torrent')
    book_add.add_argument('torrentID', type=int, help='ID of the torrent')

    parser.add_argument('-c', '--configuration',
                        help='Custom configuration file path')
    parser.add_argument('-l', '--limit', type=int,
                        help='Maximum number of fetched torrent at once')
    parser.add_argument('-u', '--username', type=str,
                        help='T411 username ( override configuration )')
    parser.add_argument('-p', '--password', type=str,
                        help='T411 password ( override configuration )')

    top.add_argument('top', choices=['100', 'day', 'week', 'month'],
                     help='Witch top to display')
    top.add_argument('sort', type=str,
                     choices=['seed', 'leech', 'size', 'download'],
                     default='seed', help='Result sorting parameter',
                     nargs='?')
    top.add_argument('order', type=str,
                     choices=['asc', 'desc'], default='desc', nargs='?')

    search.add_argument('query', type=str, help='String to search for')
    search.add_argument('-c', '--category', type=str, nargs=1,
                        help='Category to search in ( allow python regexp format )')
    search.add_argument('sort', type=str,
                        choices=['seed', 'leech', 'size', 'download'],
                        default='seed', help='Result sorting parameter',
                        nargs='?')
    search.add_argument('order', type=str, choices=['asc', 'desc'],
                        default='desc', nargs='?')

    details.add_argument('torrentID', type=int, help='ID of the torrent')

    download.add_argument('torrentsID', nargs='+', help='ID of the torrents')
    download.add_argument('name', type=str, nargs='?',
                          help='Optional torrent filename')
    download.add_argument('--cmd', type=str,
                          help='Command to invoke upon torrent completion '
                               '(torrent file variable : %torrent)')

    user.add_argument('uid', type=int, help='user id (optional)', nargs='?', default=None)

    return parser


def check_arguments(args):
    """
    TODO: Check for argument validity ?
    :param args:
    :return:
    """
    pass


def t411cli():
    parser = get_args_parser()
    args = parser.parse_args()
    ftab = {
        'search': functions.search,
        'download': functions.download,
        'details': functions.details,
        'top': functions.top,
        'categories': functions.categories,
        'user': functions.user,
        'bookmark': functions.bookmarks
    }

    # CLI argument override configuration file
    conf = from_env(args.username, args.password)
    if args.username:
        conf['account']['username'] = args.username
    if args.password:
        conf['account']['password'] = args.password
    if args.limit:
        conf['config']['limit'] = str(args.limit)

    elif not args.command:
        parser.print_usage()
        return
    api = T411API()

    try:
        api.connect(conf['account']['username'], conf['account']['password'])
    except ConnectError as e:
        print(Fore.RED, '[Error] Connection error :', e)
    except ServiceError as e:
        print(Fore.RED, '[Error] Service error :', e)
    else:
        try:
            # Command execution (search/download/...)
            ftab[args.command](api, conf, args)
        except APIError as e:
            print(Fore.RED, '[Error] API failed :', e)


def main():
    try:
        init()
        t411cli()
    except KeyboardInterrupt:
        print(Fore.GREEN, '\nExiting properly.')


if __name__ == '__main__':
    main()
