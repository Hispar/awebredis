import redis


def sscan(r, sets, key):
    """
    Scan for sets
    :param r: Redis instance
    :param sets:
    :param key:
    :return:
    """
    for key2 in r.sscan_iter(key):
        if len(sets[key]) > 1000:
            break
        try:
            newkey = r.get(key2)
        except redis.exceptions.ResponseError as e:
            newkey = 'Set/Hash/SortedSet'
        if newkey is None:
            sets[key].append(key2)
        else:
            sets[key].append({
                'key': key2,
                'value': newkey
            })


def hscan(r, hashes, key):
    """
    Scan for hashes
    :param r: Redis instance
    :param hashs:
    :param key:
    :return:
    """
    for key2 in r.hscan_iter(key):
        if len(hashes[key]) > 1000:
            break
        hashes[key][key2] = r.get(key2)


def zscan(r, sets, key):
    """
    Scan for ordered sets
    :param r: Redis instance
    :param sets:
    :param key:
    :return:
    """
    for key2 in r.zscan_iter(key):
        if len(sets[key]) > 1000:
            break
        sets[key][key2] = r.get(key2)
