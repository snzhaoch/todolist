import json
import random
from models.session import Session
from utils import gmt_time
from models.user import User


def random_str():
    """
    生成一个 16 位随机的字符串，用来设置 session
    """
    seed = 'bdjsdlkgjsklgelgjelgjsegker234252542342525g'
    s = ''
    for i in range(16):
        random_index = random.randint(0, len(seed) - 1)
        s += seed[random_index]
    return s


def add_session_headers(user=None, expired_month=0):
    """
     为注册或登录成功的 user 响应头加上 session
    """
    session_id = random_str()
    if user is None:
        user_id = session_id
    else:
        user_id = user.id
    Session.new(dict(
        session_id=session_id,
        user_id=user_id,
    ))
    expired_time = gmt_time(expired_month)
    headers = {
        'Set-Cookie': 'sid={}; Expires={}'.format(session_id, expired_time),
    }
    return headers


def current_user(request):
    """
    根据 session_id 找到当前请求对应的 user 实例
    """
    session_id = request.cookies.get('sid', '')
    sessions = Session.all()
    for s in sessions:
        if s.session_id == session_id:
            u = User.find_by(id=s.user_id)
            return u
    return None


def current_session(request):
    """
    根据 session_id 找到当前请求对应的 session 实例，
    用户登出时在服务器删除对应的 session 实例
    """
    session_id = request.cookies.get('sid', '')
    sessions = Session.all()
    for s in sessions:
        if s.session_id == session_id:
            return s
    return None


def response_with_headers(headers=None, status_code=200):
    """
    生成响应头，例子如下所示：
    Content-Type: text/html
    Set-Cookie: user=gua
    """
    header = 'HTTP/1.1 {} OK\r\nContent-Type: text/html\r\n'
    header = header.format(status_code)
    if headers is not None:
        header += ''.join([
            '{}: {}\r\n'.format(k, v) for k, v in headers.items()
        ])
    return header


def redirect(location, headers=None):
    """
    浏览器在收到 302 响应的时候
    会自动在 HTTP header 里面找 Location 字段并获取一个 url
    然后自动请求新的 url
    """
    h = {
        'Location': location
    }
    if headers is not None:
        h.update(headers)
    # 302 状态码的含义, Location 的作用
    header = response_with_headers(h, 302)
    r = header + '\r\n' + ''
    return r.encode()


def login_required(route_function):
    """
    登录状态验证，若未登录则转向登录页面
    """

    def f(request):
        u = current_user(request)
        if u is None:
            return redirect('/login')
        else:
            return route_function(request)

    return f


def error(request, code=404):
    """
    返回错误请求的响应，目前只有 404
    """
    e = {
        404: b'HTTP/1.x 404 NOT FOUND\r\n\r\n<h1>NOT FOUND</h1>',
    }
    return e.get(code, b'')


def http_response(body, headers=None):
    """
    返回对应的 HTTP byte 形式响应，headers 是可新增的字典格式的 HTTP 头部
    """
    header = response_with_headers(headers)
    r = header + '\r\n' + body
    return r.encode()


def template(name):
    """
    根据名字读取 templates 文件夹里的一个文件并返回
    """
    path = 'templates/' + name
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()


def json_response(data):
    """
    与前端进行数据交互，返回 json 格式的 body 数据，
    """
    header = 'HTTP/1.1 200 OK\r\nContent-Type: application/json\r\n'
    # ensure_ascii=False 可以正确处理中文
    body = json.dumps(data, ensure_ascii=False, indent=2)
    r = header + '\r\n' + body
    return r.encode()
