from os import system


def search(api, conf, args):
    resp = api.search(args.query, limit=500000, order='seeders')
    print('Search for query \'%s\' : %s results' % (args.query, resp['total']))
    print('%10s %5s %5s %s' % ('Torrent ID', 'Seed', 'Leech', 'Name'))
    sortlst = sorted(resp['torrents'],
                     key=lambda x: -int(x['seeders']))
    for idx in range(min(int(conf['config']['limit']), len(sortlst))):
        print('ta mere', idx)
        item = sortlst[idx]
        print('%10s %5s %5s %s' % (
            item['id'], item['seeders'], item['leechers'], item['name']
        ))


def details(api, conf, args):
    pass


def download(api, conf, args):
    fname = api.download(args.torrentID,
                         base=conf['config']['torrent_folder'])
    print('Torrent %s saved.' % fname)
    if args.cmd:
        print('Executing command "', args.cmd, '" with $torrent=', fname)
        system('torrent=%s; %s' % (fname, args.cmd))
