TodoList     
===========================
好用的待办事项列表
------------------------------------------------

## 功能简介/演示
* 注册登录
    * 注册
        * 用户名长度大于2
        * 密码长度大于2
        * 注册成功跳转到首页
    * 登录
        * 登陆成功跳转到首页
    * 退出
        * 以游客状态显示首页
    * 首页右上角根据登录状态显示不同内容

    ![image](https://github.com/snzhaoch/todolist/tree/master/demo/login.gif)


* TodoList
    * 有未完成和已完成两个版块
    * 记录创建时间、修改时间、完成时间、版块内 todolist 数量
    * 使用 AJAX 进行数据交互，页面不刷新
    * 可以编辑，完成，删除
    * 编辑功能详解
        * 第二次点击编辑按钮，编辑栏会回收
        * 可同时点开多个编辑栏，且可不按点击顺序进行更新
    * 设置 cookie 过期时间，即使游客关闭浏览器，再次访问页面也可找回数据

    ![image](https://github.com/snzhaoch/todolist/tree/master/demo/todolist.gif)
