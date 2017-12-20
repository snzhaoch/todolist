var log = function() {
    console.log.apply(console, arguments)
}

var e = function(selector) {
    return document.querySelector(selector)
}

// unix 时间戳转换为可读时间
var commonTime = function(unixtime) {
    var unixTimestamp = new Date(unixtime* 1000)
    var commonTime = unixTimestamp.toLocaleString()
    return commonTime
}

// 获取页面 cookie 中的 sid 字段
var get_cookie = function() {
    var c = document.cookie.split('; ')
    for (var i=0; i<c.length; i++) {
        if (c[i].substring(0,4) === 'sid=') {
            return c[i]
        }
    }
}

// ajax 函数
var ajax = function(method, path, data, responseCallback) {
    var r = new XMLHttpRequest()
    // 设置请求方法和请求地址
    r.open(method, path, true)
    // 设置发送的数据的格式为 application/json
    r.setRequestHeader('Content-Type', 'application/json')
    // 注册响应函数
    r.onreadystatechange = function() {
        if(r.readyState === 4) {
            // r.response 存的是服务器发过来的放在 HTTP BODY 中的数据
            responseCallback(r.response)
        }
    }
    // 把数据转换为 json 格式字符串
    data = JSON.stringify(data)
    // 发送请求
    r.send(data)
}
