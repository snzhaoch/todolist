def route_static(request):
    """
    读取静态文件并生成响应返回
    """
    filename = request.query.get('file', )
    path = 'static/' + filename
    with open(path, 'rb') as f:
        header = b'HTTP/1.1 200 OK\r\n\r\n'
        binary = header + f.read()
        return binary


def route_dict():
    r = {
        '/static': route_static,
    }
    return r
