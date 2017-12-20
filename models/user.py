from models import Model
import hashlib


class User(Model):
    """
    保存用户数据的 model
    """

    def __init__(self, form):
        super().__init__(form)
        self.username = form.get('username', '')
        self.password = form.get('password', '')

    @staticmethod
    def salted_password(password, salt='$!@><?>HUI&DWQa`'):
        """
         密码加盐
         """
        salted = password + salt
        hash = hashlib.sha256(salted.encode('ascii')).hexdigest()
        return hash

    def validate_login(self):
        """
        验证登录
        """
        u = User.find_by(username=self.username)
        if u is not None:
            return u.password == self.salted_password(self.password)
        else:
            return False

    def validate_register(self):
        """
        验证注册，条件 ：用户名不存在；用户名长度大于2；密码长度大于2
        """
        u = User.find_by(username=self.username)
        valid = u is None and len(self.username) > 2 and len(self.password) > 2
        if valid:
            p = self.password
            self.password = self.salted_password(p)
            return True
        else:
            return False
