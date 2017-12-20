from routes import json_response
from models.todo import Todo
from models.session import Session
from models.user import User


def all(request):
    """
    返回当前用户所有 Todo，若是登录用户则根据 user_id 返回，否则根据 session_id 返回
    """
    session_id = request.query.get('sid')
    s = Session.find_by(session_id=session_id)
    if s is not None:
        user_id = s.user_id
        todos = Todo.find_all_json(user_id=user_id)
    else:
        todos = Todo.find_all_json(session_id=session_id)
    return json_response(todos)


def add(request):
    """
    新增 todo
    """
    form = request.json()
    t = Todo.new(form)
    return json_response(t.json())


def delete(request):
    """
    删除 todo
    """
    todo_id = int(request.query.get('id'))
    t = Todo.delete(todo_id)
    return json_response(t.json())


def update(request):
    """
    更新 todo
    """
    form = request.json()
    todo_id = int(form.get('id'))
    t = Todo.update(todo_id, form)
    return json_response(t.json())


def done(request):
    """
    完成 todo
    """
    todo_id = int(request.query.get('id'))
    t = Todo.done(todo_id)
    return json_response(t.json())


def find_user(request):
    """
    查找当前用户的用户名
    """
    session = request.query.get('sid')
    s = Session.find_by(session_id=session)
    if s.session_id == s.user_id:
        username = "游客"
    else:
        user_id = s.user_id
        user = User.find(user_id)
        username = user.username
    return json_response(username)


def route_dict():
    d = {
        '/api/todo/all': all,
        '/api/todo/add': add,
        '/api/todo/delete': delete,
        '/api/todo/update': update,
        '/api/todo/done': done,
        '/api/todo/finduser': find_user,
    }
    return d
