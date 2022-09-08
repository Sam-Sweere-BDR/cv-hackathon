def rhash(n):
    return n * 387420489 % 4000000000


def un_rhash(h):
    return h * 3513180409 % 4000000000
