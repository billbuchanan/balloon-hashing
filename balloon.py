import hashlib
import random
import string

hash_functions = {
    'md5': hashlib.md5,
    'sha1': hashlib.sha1,
    'sha224': hashlib.sha224,
    'sha256': hashlib.sha256,
    'sha384': hashlib.sha384,
    'sha512': hashlib.sha512
}

HASH_TYPE = 'sha256'

def hash_func(*args):
    t = ''.join([str(arg) for arg in args])
    return hash_functions[HASH_TYPE](t).digest()

def expand(buf, cnt, space_cost):
    for s in range(1, space_cost):
        buf.append(hash_func(cnt, buf[s - 1]))
        cnt += 1

def mix(buf, cnt, delta, salt, space_cost, time_cost):
    for t in range(time_cost):
        for s in range(space_cost):
            buf[s] = hash_func(cnt, buf[s - 1], buf[s])
            cnt += 1
            for i in range(delta):
                other  = int(hash_func(cnt, salt, t, s, i).encode('hex'), 16) % space_cost
                cnt   += 1
                buf[s] = hash_func(cnt, buf[s], buf[other])
                cnt   += 1

def extract(buf):
    return buf[-1]

def balloon(password, salt, space_cost, time_cost, delta=3):
    buf = [hash_func(0, password, salt)]
    cnt = 1

    expand(buf, cnt, space_cost)
    mix(buf, cnt, delta, salt, space_cost, time_cost)
    return extract(buf)

def balloon_hash(password, salt):
    delta      = 4
    time_cost  = 20
    space_cost = 16
    return balloon(password, salt, space_cost, time_cost, delta=delta).encode('hex')