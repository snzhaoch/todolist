import json
import urllib.parse


class Request(object):
    """
    解析 request 的 model
    """
    def __init__(self, raw_data):
        header, self.body = raw_data.split('\r\n\r\n', 1)
        h = header.split('\r\n')

        parts = h[0].split()
        self.method = parts[0]
        path = parts[1]
        self.path = ""
        self.query = {}
        self.parse_path(path)

        self.headers = {}
        self.cookies = {}
        self.add_headers(h[1:])
        self.add_cookies()

    def add_cookies(self):
        """
        解析 cookies
        """
        cookies = self.headers.get('Cookie', '')
        kvs = cookies.split('; ')
        for kv in kvs:
            if '=' in kv:
                k, v = kv.split('=')
                self.cookies[k] = v

    def add_headers(self, header):
        """
        解析 headers
        """
        lines = header
        for line in lines:
            k, v = line.split(': ', 1)
            self.headers[k] = v

    def form(self):
        """
        解析 body
        """
        body = urllib.parse.unquote(self.body)
        args = body.split('&')
        f = {}
        for arg in args:
            k, v = arg.split('=')
            f[k] = v
        return f

    def parse_path(self, path):
        """
        解析 URL 中的 path
        """
        index = path.find('?')
        if index == -1:
            self.path = path
            self.query = {}
        else:
            path, query_string = path.split('?', 1)
            args = query_string.split('&')
            query = {}
            for arg in args:
                k, v = arg.split('=')
                query[k] = v
            self.path = path
            self.query = query

    def json(self):
        """
        把 body 中的 json 格式字符串解析成 dict 或者 list 并返回
        """
        return json.loads(self.body)