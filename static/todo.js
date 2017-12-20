// TODO API
// 获取所有 todo
var apiTodoAll = function(cookie, callback) {
    var path = `/api/todo/all?${cookie}`
    ajax('GET', path, '', callback)
}

// 删除一个 todo
var apiTodoDelete = function(id, callback) {
    var path = `/api/todo/delete?id=${id}`
    ajax('GET', path, '', callback)
}

// 增加一个 todo
var apiTodoAdd = function(form, callback) {
    var path = '/api/todo/add'
    ajax('POST', path, form, callback)
}

// 更新一个 todo
var apiTodoUpdate = function(form, callback) {
    var path = '/api/todo/update'
    ajax('POST', path, form, callback)
}

// 完成一个 todo
var apiTodoDone = function(id, callback) {
    var path = `/api/todo/done?id=${id}`
    ajax('GET', path, '', callback)
}

// 获取用户名
var apiLoadUsername = function(cookie, callback) {
    // cookie 是 sid=sjgb4ee5lej2kr2k 格式的，不能写成 cookie=${cookie} 形式，否则 Request 会解析错误
    var path = `/api/todo/finduser?${cookie}`
    ajax('GET', path, '', callback)
}


// TODO DOM
// 新增 todo 模板
var todoNewTemplate = function(todo) {
    var t = `
    <tr class="todo-cell">
        <td class="todo-task">${todo.task}</td>
        <td class="td-mid"></td>
        <td class="td-mid">${todo.created_time}</td>
        <td class="td-mid">${todo.updated_time}</td>
        <td class="td-mid"><button class="btn btn-info btn-xs todo-edit" data-id=${todo.id}>编辑</button> / <button class="btn btn-success btn-xs todo-done" data-id=${todo.id}>完成</button> / <button class="btn btn-xs btn-danger todo-delete new-todo-delete" data-id=${todo.id}>删除</button></td>
    </tr>
    `
    return t
}

// 已完成 todo 模板
var todoDoneTemplate = function(todo) {
    var t = `
    <tr class="done-cell">
        <td class="todo-task">${todo.task}</td>
        <td class="td-mid">${todo.completed_time}</td>
        <td class="td-mid">${todo.created_time}</td>
        <td class="td-mid">${todo.updated_time}</td>
        <td class="td-mid"><button class="btn btn-xs btn-danger todo-delete done-todo-delete" data-id=${todo.id}>删除</button></td>
    </tr>
    `
    return t
}

//　todo 更新模板
var todoUpdateTemplate = function(todo_id) {
    var t = `
        <td colspan="4">
              <label for="id-todo-edit" class="sr-only">Input</label>
              <input type="text" class="form-control todo-update-input" data-id=${todo_id} id="id-todo-edit" placeholder="输入更改后的Todo，按Enter键完成" required="required">
        </td>
    `
    return t
}

// 在页面中插入一个 todo
var insertTodo = function(todo) {
    todo.created_time = commonTime(todo.created_time)
    todo.updated_time = commonTime(todo.updated_time)
    // 插入 todo-list
    var completed = todo.completed
    if (completed === false){
        var todoCell = todoNewTemplate(todo)
        var todo = e('.todo-list')
        var count = e('#id-todo-count')
    } else {
        todo.completed_time = commonTime(todo.completed_time)
        var todoCell = todoDoneTemplate(todo)
        var todo = e('.done-list')
        var count = e('#id-done-count')
    }
    todo.insertAdjacentHTML('afterbegin', todoCell)
    count.innerHTML = parseInt(count.innerHTML) + 1
}

// 在页面中插入用户名
var insertUsername = function(username) {
    var n = e(".name-login")
    if (username === '游客') {
        n.innerHTML = `<a>游客</a>`
        n.insertAdjacentHTML('afterend',`<li><a href="/login">登录/注册</a></li>`)
    } else {
        n.innerHTML = `<a>${username}</a>`
        n.insertAdjacentHTML('afterend',`<li><a href="/logout">退出</a></li>`)
    }
}

// 在页面中加载所有 todo
var loadTodos = function() {
    // 调用 ajax api 来载入数据
    var cookie = get_cookie()
    apiTodoAll(cookie, function(r) {
        console.log('load all', r)
        // 解析为 数组
        var todos = JSON.parse(r)
        // 循环添加到页面中
        for(var i = 0; i < todos.length; i++) {
            var todo = todos[i]
            insertTodo(todo)
        }
    })
}

// 为输入栏中的回车动作，绑定 TodoAdd 事件
var bindEventTodoAdd = function() {
    var b = e('#id-todo-add')
    b.addEventListener('keyup', function(event){
        if (event.keyCode === 13){
            var cookie = get_cookie()
            var task = b.value
            b.value = null
            var form = {
                task: task,
                cookie: cookie,
            }
            apiTodoAdd(form, function(response) {
                var todo = JSON.parse(response)
                insertTodo(todo)
        })
    }})
}


// 为删除按钮绑定 TodoDelete 事件
var bindEventTodoDelete = function() {
    var todoList = e('body')
    todoList.addEventListener('click', function (event) {
        var self = event.target
        if (self.classList.contains('todo-delete')) {
            var todo_id = self.dataset.id
            apiTodoDelete(todo_id, function(response) {
                // 删除 self 的父节点
                if (self.classList.contains('new-todo-delete')){
                    var count = e('#id-todo-count')
                } else {
                    var count = e('#id-done-count')
                }
                count.innerHTML = parseInt(count.innerHTML) - 1
                self.parentElement.parentElement.remove()
            })
        }
    })
}

// 为编辑按钮绑定 TodoEdit 事件
var bindEventTodoEdit = function() {
    var todoList = e('.todo-list')
    todoList.addEventListener('click', function (event) {
        var self = event.target
        if (self.classList.contains('todo-edit')) {
            // 获取当前 todo 下一行,以及第一个元素，判断是应该插入编辑框还是去除编辑框
            var n = self.parentElement.parentElement.nextElementSibling
            // var e = n.firstElementChild.firstElementChild        e != null
            if (n != null && n.firstElementChild.firstElementChild != null) {
                n.remove()
            }
            else {
                var todo_id = self.dataset.id
                var t = todoUpdateTemplate(todo_id)
                self.parentElement.parentElement.insertAdjacentHTML('afterend', t)
            }
        }
    })
}

// 为更新按钮绑定 TodoUpdate 事件
var bindEventTodoUpdate = function() {
    var todoList = e('.todo-list')
    todoList.addEventListener('keyup', function (event) {
        var self = event.target
        if (event.keyCode === 13 && self.classList.contains('todo-update-input')) {
            var value = self.value
            var todoId = self.dataset.id
            var form = {
                id: todoId,
                task: value,
            }
            apiTodoUpdate(form, function(response) {
                var updateForm = self.parentElement.parentElement
                var todoTag = updateForm.previousElementSibling.firstElementChild
                updateForm.remove()

                var todo = JSON.parse(response)
                todoTag.innerHTML = todo.task
            })

        }
    })
}

// 为完成按钮绑定 TodoDone 事件
var bindEventTodoDone = function() {
    var todoList = e('.todo-list')
    todoList.addEventListener('click', function (event) {
        var self = event.target
        if (self.classList.contains('todo-done')) {
            var todoCell = self.closest('.todo-cell')
            var todoId = self.dataset.id
            apiTodoDone(todoId, function(response) {
                self.parentElement.parentElement.remove()
                var todo = JSON.parse(response)
                insertTodo(todo)

                // insertTodo 将 id-done-count + 1，因此这里这需要将 id-todo-count -1就够了
                var count = e('#id-todo-count')
                count.innerHTML = parseInt(count.innerHTML) - 1
            })

        }
    })
}

// 在页面中加载用户名
var loadUsername = function() {
    var cookie = get_cookie()
    apiLoadUsername(cookie, function(response) {
        var username = JSON.parse(response)
        insertUsername(username)
    })
}


var bindEvents = function() {
    bindEventTodoAdd()
    bindEventTodoDelete()
    bindEventTodoEdit()
    bindEventTodoUpdate()
    bindEventTodoDone()
}

var __main = function() {
    bindEvents()
    loadTodos()
    loadUsername()
}

__main()
