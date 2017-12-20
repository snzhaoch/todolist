import json


def save(data, path):
    """
    保存数据到指定文件
    """
    s = json.dumps(data, indent=2, ensure_ascii=False)
    with open(path, 'w+', encoding='utf-8') as f:
        f.write(s)


def load(path):
    """
    读取指定文件的数据
    """
    with open(path, 'r', encoding='utf-8') as f:
        s = f.read()
        return json.loads(s)


class Model(object):
    """
    Model 是所有 model 的基类
    """

    def __init__(self, form):
        self.id = form.get('id', None)

    @classmethod
    def db_path(cls):
        """
        返回文件的路径，文件名与 cls 的名字相同
        """
        classname = cls.__name__
        path = 'data/{}.txt'.format(classname)
        return path

    @classmethod
    def _new_from_dict(cls, d):
        # 根据 txt 文件里的数据初始化一个 cls 实例
        m = cls({})
        for k, v in d.items():
            setattr(m, k, v)
        return m

    @classmethod
    def all(cls):
        """
        返回所有的实例
        """
        path = cls.db_path()
        models = load(path)
        ms = [cls._new_from_dict(m) for m in models]
        return ms

    @classmethod
    def new(cls, form):
        """
        初始化一个 cls，单独设置此函数可以实现功能扩充：保存，log等
        """
        m = cls(form)
        return m

    @classmethod
    def find_by(cls, **kwargs):
        """
        根据指定条件，返回第一个符合的 cls 实例
        """
        for m in cls.all():
            exist = False
            for key, value in kwargs.items():
                k, v = key, value
                if v == getattr(m, k):
                    exist = True
                else:
                    exist = False
            if exist:
                return m
        return None

    @classmethod
    def find(cls, id):
        """
        根据 id 查找 cls 实例
        """
        return cls.find_by(id=id)

    @classmethod
    def find_all(cls, **kwargs):
        """
        根据指定条件，返回所有符合的 cls 实例
        """
        models = []
        for m in cls.all():
            exist = False
            for key, value in kwargs.items():
                k, v = key, value
                if v == getattr(m, k):
                    exist = True
                else:
                    exist = False
            if exist:
                models.append(m)
        return models

    def __repr__(self):
        """
        设置打印字符串格式为：
        < Todo
        id: (10)
        task: (756)
        completed: (False)
        user_id: (1)
        created_time: (1512446589)
        updated_time: (1512446589)
        session_id: (gg4j2g2jdej24252)
        >
        """
        classname = self.__class__.__name__
        properties = ['{}: ({})'.format(k, v) for k, v in self.__dict__.items()]
        s = '\n'.join(properties)
        return '< {}\n{} \n>\n'.format(classname, s)

    def save(self):
        """
        把 cls 实例保存到 txt 文件中
        """
        models = self.all()

        first_index = 0
        # 新 cls 没有 id，自动为 cls 添加 id 并将 cls 加入 models 中
        if self.id is None:
            if len(models) > 0:
                self.id = models[-1].id + 1
            else:
                self.id = first_index
            models.append(self)
        # cls 更新时，根据已有 id 完成新旧 cls 的替换
        else:
            for i, m in enumerate(models):
                if m.id == self.id:
                    models[i] = self

        # 保存
        l = [m.__dict__ for m in models]
        path = self.db_path()
        save(l, path)

    @classmethod
    def delete(cls, id):
        """
        根据 id 删除指定的 cls 实例
        """
        models = cls.all()
        index = -1
        for i, e in enumerate(models):
            if e.id == id:
                index = i
                break
        # 判断是否找到了这个 id 的数据
        if index != -1:
            o = models.pop(index)
            l = [m.__dict__ for m in models]
            path = cls.db_path()
            save(l, path)
            # 返回被删除的元素
            return o

    def json(self):
        """
        返回当前 cls 的字典表示
        """
        d = self.__dict__
        return d

    @classmethod
    def all_json(cls):
        """
        返回所有 json 格式实例
        """
        ms = cls.all()
        jsons = [t.json() for t in ms]
        return jsons

    @classmethod
    def find_all_json(cls, **kwargs):
        """
        返回指定条件的所有 json 格式实例
        """
        ms = cls.find_all(**kwargs)
        jsons = [t.json() for t in ms]
        return jsons
