from os import system


def search(api, conf, args):
    """
    Handle search requests
    :param api:
    :param conf:
    :param args:
    :return:
    """

    # TODO : Limitation on API
    #  limit is put on a big number at the moment as
    # we don't know how to sort results via the API
    # so we basiclly just get everything and sort afterward
    # this can cause BIG SLOWDOWN on tiny requests like 'a'

    resp = api.search(args.query, limit=500000)
    sortlst = sorted(resp['torrents'],
                     key=lambda x: -int(x['seeders']))

    print('Search for query \'%s\' : %s results' % (args.query, resp['total']))
    print('%10s %5s %5s %s' % ('Torrent ID', 'Seed', 'Leech', 'Name'))
    for idx in range(min(int(conf['config']['limit']), len(sortlst))):
        item = sortlst[idx]
        print('%10s %5s %5s %s' % (
            item['id'], item['seeders'], item['leechers'], item['name']
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
    print('Torrent name        :', resp['name'])
    print('Torrent ID          :', resp['id'])
    print('Category            :', resp['categoryname'])
    print('From                :', resp['username'])
    for item in resp['terms'].keys():
        print('%-20s:' % item, resp['terms'][item])

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
    print('Torrent %s saved.' % fname)
    if args.cmd:
        print('Executing command "', args.cmd, '" with $torrent=', fname)
        system('torrent=%s; %s' % (fname, args.cmd))
