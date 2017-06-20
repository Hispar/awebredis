import redis

from flask import Flask, render_template

from code.utilities.groups import group_set
from code.utilities.redis import sscan

app = Flask(__name__)

HOST = '192.168.99.100'
PORT = 6379

r = redis.Redis(
    host=HOST,
    port=PORT)


@app.route("/")
def index():
    try:
        info = r.info()
    except Exception:
        return render_template('inactive.html')
    return render_template('index.html', info=info)


@app.route("/keys")
def keys():
    keys = dict()

    try:
        for key in r.scan_iter():
            if len(keys) > 1000:
                break
            try:
                keys[key] = r.get(key)
            except redis.exceptions.ResponseError as e:
                pass

        print(keys)
    except Exception:
        return render_template('inactive.html')

    return render_template('keys.html', keys=keys)


@app.route("/sets")
def sets():
    sets = dict()

    try:
        for key in r.scan_iter():
            try:
                r.get(key)
            except redis.exceptions.ResponseError as e:
                if len(sets) > 1000:
                    break
                sets[key] = []
                try:
                    sscan(r, sets, key)
                except redis.exceptions.ResponseError as e2:
                    pass

        print(sets)
        group_set(sets)
    except Exception:
        return render_template('inactive.html')
    return render_template('sets.html', sets=sorted(sets))


# @app.route("/hashs")
# def hashs():
#     if not active:
#         return render_template('inactive.html')
#     hashs = dict()
#
#     for key in r.scan_iter():
#         try:
#             r.get(key)
#         except redis.exceptions.ResponseError as e:
#             try:
#                 r.sscan(key, 0)
#             except redis.exceptions.ResponseError as e2:
#                 try:
#                     hscan(hashs, key)
#                 except redis.exceptions.ResponseError as e3:
#                     pass
#     print(hashs)
#
#     return render_template('sets.html', sets=hashs)


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8888)
