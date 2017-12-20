import socket
import _thread
from request import Request
from routes import error
from routes.routes_todo import route_dict as todo_routes
from routes.api_todo import route_dict as todo_api
from routes.routes_user import route_dict as user_routes
from routes.routes_static import route_dict as static_routes


def response_for_path(request):
    """
    根据 path 调用相应的处理函数
    没有处理的 path 会返回 404
    """
    r = {}
    # 注册外部的路由
    r.update(todo_routes())
    r.update(todo_api())
    r.update(user_routes())
    r.update(static_routes())
    response = r.get(request.path, error)
    return response(request)


def process_request(connection):
    with connection:
        r = connection.recv(10240)
        r = r.decode()
        # 把原始请求数据传给 Request 对象
        request = Request(r)
        # 用 response_for_path 函数来得到 path 对应的响应内容
        response = response_for_path(request)
        connection.sendall(response)


def run(host, port):
    """
    启动服务器
    """
    with socket.socket() as s:
        # 保证程序重启后使用原有端口
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((host, port))
        s.listen(5)
        while True:
            connection, address = s.accept()
            _thread.start_new_thread(process_request, (connection,))


if __name__ == '__main__':
    # 生成配置并且运行程序
    config = dict(
        host='127.0.0.1',
        port=8800,
    )
    run(**config)
