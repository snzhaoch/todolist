from models import Model


class Session(Model):
    """
    保存 session 的 model
    """

    def __init__(self, form):
        super().__init__(form)
        self.session_id = form.get('session_id', '')
        self.user_id = form.get('user_id', '')

    @classmethod
    def new(cls, form):
        """
        新增 session
        """
        m = super().new(form)
        m.save()
        return m