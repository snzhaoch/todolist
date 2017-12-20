from routes import (
    http_response,
    current_user,
    current_session,
    add_session_headers,
    template
)


def index(request):
    """
    返回 Todolist 主页，
    若请求没有 session 则添加一个 Set-Cookie 字段
    """
    body = template('index.html')
    u = current_user(request)
    s = current_session(request)
    if u is None and s is None:
        # 为游客的 cookie 有效期设置为 1 个月
        headers = add_session_headers(expired_month=1)
        return http_response(body, headers)
    return http_response(body)


def route_dict():
    d = {
        '/': index,
    }
    return d