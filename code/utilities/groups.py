def group_set(set):
    group = dict()
    for element in set:
        explode = str(element).split(':')
        count = 0
        keys = []
        for idx, part in enumerate(explode):
            if len(part) <= 0:
                count -= 1
                continue

            last = False
            if idx == (len(explode) - 1):
                last = True

            if count == 0:
                key_set(group, part, last)
            else:
                g = group
                for key in keys:
                    g = g[key]
                key_set(g, part, last)

                print(g)

            keys.append(part)

    print(group)


def key_set(set, key, last=False):
    if key not in set:
        if not last:
            set[key] = dict()
        else:
            if 'keys' not in set:
                set['keys'] = []
            set['keys'].append(key)
    return set
