from models.session import Session
from routes import (
    redirect,
    http_response,
    add_session_headers,
    current_session,
    template,
)
from models.user import User


def route_login(request):
    """
    登录的处理函数, 返回主页的响应
    """
    if request.method == 'POST':
        form = request.form()
        u = User(form)
        user = User.find_by(username=u.username)
        if u.validate_login():
            # 为登录用户的 cookie 有效期设置为 1 年
            headers = add_session_headers(user, expired_month=12)
            return redirect('/', headers)
    body = template('login.html')
    return http_response(body)


def route_register(request):
    """
    注册的处理函数, 返回主页的响应
    """
    if request.method == 'POST':
        form = request.form()
        user = User.new(form)
        if user.validate_register():
            user.save()
            # 为登录用户的 cookie 有效期设置为 1 年
            headers = add_session_headers(user, expired_month=12)
            return redirect('/', headers)
        else:
            return redirect('/login')
    body = template('login.html')
    return http_response(body)


def route_logout(request):
    """
    注销登录
    """
    session = current_session(request)
    session_id = int(session.id)
    Session.delete(session_id)
    return redirect('/')


def route_dict():
    r = {
        '/login': route_login,
        '/register': route_register,
        '/logout': route_logout,
    }
    return r
