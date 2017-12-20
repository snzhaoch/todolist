import time
from models import Model
from models.session import Session


class Todo(Model):
    """
    保存 Todo 的 model
    """

    def __init__(self, form):
        super().__init__(form)
        self.task = form.get('task', '')
        self.completed = False
        # user_id = -1 表示为游客
        self.user_id = form.get('user_id', -1)
        self.created_time = form.get('created_time')
        self.updated_time = form.get('updated_time')

    @classmethod
    def new(cls, form):
        """
        新增 Todo
        """
        # apiTodoAdd 传过来的 form 中 cookie 是 { cookie : sid=adsfwerqwedas } 形式的
        session_id = form.get('cookie', None).split('=')[1]
        # 查询 session 是否有相应的用户，有的话设置成相应的 user_id
        s = Session.find_by(session_id=session_id)
        if s is not None:
            user_id = s.user_id
            form['user_id'] = user_id
        m = super().new(form)
        m.session_id = session_id

        t = int(time.time())
        m.created_time = t
        m.updated_time = t
        m.save()
        return m

    @classmethod
    def update(cls, id, form):
        """
        更新 Todo 内容
        """
        t = cls.find(id)
        valid_names = [
            'task',
        ]
        for key in form:
            # 只更新 valid_names 中的内容
            if key in valid_names:
                setattr(t, key, form[key])
        t.updated_time = int(time.time())
        t.save()
        return t

    @classmethod
    def done(cls, id):
        """
        将 Todo 状态设置为完成
        """
        t = cls.find(id)
        t.completed = True
        t.completed_time = int(time.time())
        t.save()
        return t
