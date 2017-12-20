import time


def formatted_time(unixtime):
    dt = time.localtime(unixtime)
    ds = time.strftime('%Y-%m-%d %H:%M:%S', dt)
    return ds


def gmt_time(month=0):
    format = '%a, %d %b %Y %H:%M:%S GMT'
    second = month * 30 * 24 * 60 * 60
    value = time.localtime(int(time.time()) + second)
    dt = time.strftime(format, value)
    return dt