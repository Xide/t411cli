"""
Wrappers to command line options
normalized functions receiving api,
file configuration and command line arguments
"""

from os import system
from t411cli.helpers import sizeof_fmt
from colorama import Fore


def search(api, conf, args):
    """
    Handle search requests
    :param api:
    :param conf:
    :param args:
    :return:
    """

    # TODO : Limitation on API
    # limit is put on a big number at the moment as
    # we don't know how to sort results via the API
    # so we basiclly just get everything and sort afterward
    # this can cause BIG SLOWDOWN on tiny requests like 'a'
    resp = api.search(args.query, limit=500000)

    print(Fore.WHITE,
          'Search for query \'%s\' : %s results' % (args.query, resp['total']))
    sortlst = sort_torrents(resp['torrents'], args.sort, args.order)
    display_list(sortlst, conf['config']['limit'])


def sort_torrents(torrents, key, order):
    """
    Sort a list of torrents
    :param torrents: list of torrents returned by t411 API
    :param key: one of 'seed', 'leech', 'size', 'download'
    :param order: 'asc' or 'desc'
    :return: dict with sorted torrents
    """
    ctab = {
        'seed': 'seeders',
        'leech': 'leechers',
        'size': 'size',
        'download': 'times_completed'
    }
    assert isinstance(torrents, list),\
        'sort_torrents is supposed to finc a list of torrents'
    order = 1 if order == 'asc' else -1
    return sorted(torrents, key=lambda x: order * int(x[ctab[key]]))


def bookmarks(api, conf, args):
    if not args.books or 'list' in args.books:
        display_list(api.bookmarks(), conf['config']['limit'])
        return
    elif 'add' in args.books:
        api.add_bookmark(args.torrentID)
    else:
        api.del_bookmark(args.torrentID)
    print(Fore.GREEN, 'Done')


def top(api, conf, args):
    try:
        resp = api.top(args.top)
    except ValueError:
        print(Fore.RED, '[Error] Incorrect top parameter')
    else:
        sortlst = sort_torrents(resp, args.sort, args.order)
        display_list(sortlst, conf['config']['limit'])


def display_list(torrents, limit):
    if not len(torrents):
        print(Fore.LIGHTBLUE_EX, 'Nothing to display.')
    else:
        print(Fore.LIGHTWHITE_EX, '%10s %5s %5s %10s    %s' %
              ('Torrent ID', 'Seed', 'Leech', 'Size', 'Name'))
        for idx in range(min(int(limit), len(torrents))):
            item = torrents[idx]
            print('%s%10s %s %5s %s %5s %s %10s %s %s' % (
                Fore.WHITE, item['id'], Fore.GREEN,
                item['seeders'], Fore.RED,
                item['leechers'], Fore.MAGENTA,
                sizeof_fmt(int(item['size'])),
                Fore.LIGHTBLUE_EX, item['name']
            ))


def details(api, conf, args):
    """
    Handle request for torrent details
    :param api:
    :param conf:
    :param args:
    :return:
    """
    resp = api.details(args.torrentID)
    print(Fore.LIGHTBLUE_EX, 'Torrent name        :', resp['name'])
    print(Fore.LIGHTBLUE_EX, 'Torrent ID          :', resp['id'])
    print(Fore.LIGHTBLUE_EX, 'Category            :', resp['categoryname'])
    print(Fore.LIGHTBLUE_EX, 'From                :', resp['username'])
    for item in resp['terms'].keys():
        print(Fore.LIGHTBLUE_EX, '%-20s:' % item, resp['terms'][item])


def download(api, conf, args):
    """
    Download a torrent
    :param api:
    :param conf:
    :param args:
    :return:
    """

    fname = api.download(args.torrentID,
                         base=conf['config']['torrent_folder'])
    print(Fore.GREEN, 'Torrent %s saved.' % fname)
    if args.cmd:
        print('Executing command "', args.cmd, '" with %torrent=', fname)
        system('torrent=%s; %s' %
               (fname, args.cmd.replace('%torrent', '$torrent')))
