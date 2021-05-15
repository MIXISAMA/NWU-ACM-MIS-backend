# Endpoints文档

## 目录

- [Endpoints文档](#endpoints文档)
  - [目录](#目录)
  - [规则](#规则)
  - [drf通用错误响应](#drf通用错误响应)
    - [400 Bad Request](#400-bad-request)
    - [401 Unauthorized](#401-unauthorized)
    - [403 Forbidden](#403-forbidden)
    - [404 Not Found](#404-not-found)
  - [1 普通用户](#1-普通用户)
    - [1.1 用户注册 `POST` `/user/email-register/`](#11-用户注册-post-useremail-register)
    - [1.2 向用户提供的邮箱发送验证码 `POST` `/user/email-verification/<str:email>/`](#12-向用户提供的邮箱发送验证码-post-useremail-verificationstremail)
    - [1.3 邮箱&密码登入 `POST` `/user/email-login/`](#13-邮箱密码登入-post-useremail-login)
    - [1.4 查询用户信息 `GET` `/user/user/<str:email>/`](#14-查询用户信息-get-useruserstremail)
    - [1.5 修改用户信息 `PUT` `/user/user/<str:email>/`](#15-修改用户信息-put-useruserstremail)
    - [1.6 上传用户头像 `POST|PUT` `/user/user/<str:email>/avatar/`](#16-上传用户头像-postput-useruserstremailavatar)
  - [2 任务计划](#2-任务计划)
    - [2.1 获取所有公告 `GET` `/plan/announcement/`](#21-获取所有公告-get-planannouncement)
    - [2.2 获取单个公告 `GET` `/plan/announcement/<int:id>/`](#22-获取单个公告-get-planannouncementintid)

## 规则

- url务必以`/`结束
  - `/user/<int:pk>/` ⭕️
  - `/user/` ⭕️
  - `/user` ❌
- 特殊错误响应应有`detail`以及错误原因, 例:

```json
{
  "detail" : "该用户已存在, 无法重新注册用户"
}
```

- 不同类型错误响应尽量使用不同的HTTP状态码，以方便前端根据状态码展示错误信息

## drf通用错误响应

### 400 Bad Request

```json
{
  "detail": [
    "xx字段xx错误"
  ]
}
```

### 401 Unauthorized

```json
{
  "detail": "身份认证信息未提供。"
}
```

### 403 Forbidden

```json
{
  "detail": "您没有执行该操作的权限。"
}
```

### 404 Not Found

```json
{
  "detail": "未找到。"
}
```

## 1 普通用户

### 1.1 用户注册 `POST` `/user/email-register/`

|字段名|类型|例子|备注|必填|
|-|-|-|-|-|
|email|str|register_email@xx.xx|账号邮箱|✅|
|code|str|asdfgh|6位验证码|✅|
|nickname|str|bad apple|昵称|✅|
|password|str|1234qwer|密码|✅|

- 成功状态码 `201`

```json
{
    "token": "Token xxx"
}
```

- 状态码 `403`

```json
{
  "detail": "验证码无效"
}
```

### 1.2 向用户提供的邮箱发送验证码 `POST` `/user/email-verification/<str:email>/`

- 成功状态码 `204`

- 状态码 `403`

```json
{
    "detail": "该用户已注册"
}
```

- 状态码 `412`

```json
{
    "detail": "验证邮件发送失败"
}
```

### 1.3 邮箱&密码登入 `POST` `/user/email-login/`

|字段名|类型|例子|备注|必填|
|-|-|-|-|-|
|username|str|login_email@xx.xx|账号邮箱|✅|
|password|str|1234qwer|密码|✅|

- 成功状态码 `200`

```json
{
    "token": "Token xxx"
}
```

### 1.4 查询用户信息 `GET` `/user/user/<str:email>/`

- 成功状态码 `200`

```json
{
    "email": "user_email@xx.xx",
    "nickname": "user nickname",
    "role": "I",
    "avatar": "/media/avatar/avatar_Pznn3VO.jpg",
    "date_joined": "2021-05-14T20:41:30.022715+08:00",
    "college": "西北大学"
}
```

role:

- I: 本校生
- M: 队员
- C: 教练
- E: 外校人士

### 1.5 修改用户信息 `PUT` `/user/user/<str:email>/`

|字段名|类型|例子|备注|必填|
|-|-|-|-|-|
|nickname|str|bad apple|昵称||
|college|str|西北工业大学|学校||

- 成功状态码 `200`

```json
{
    "email": "user_email@xx.xx",
    "nickname": "bad apple",
    "role": "I",
    "avatar": "/media/avatar/avatar_Pznn3VO.jpg",
    "date_joined": "2021-05-14T20:41:30.022715+08:00",
    "college": "西北工业大学"
}
```

### 1.6 上传用户头像 `POST|PUT` `/user/user/<str:email>/avatar/`

|字段名|类型|例子|备注|必填|
|-|-|-|-|-|
|avatar|file||图片文件|✅|

- 成功状态码 `200`

```json
{
    "email": "user_email@xx.xx",
    "nickname": "bad apple",
    "role": "I",
    "avatar": "/media/avatar/avatar_Pznn3VO.jpg",
    "date_joined": "2021-05-14T20:41:30.022715+08:00",
    "college": "西北工业大学"
}
```

## 2 任务计划

### 2.1 获取所有公告 `GET` `/plan/announcement/`

- 成功状态码 `200`

```json
[
    {
        "id": 1,
        "title": "公告标题1",
        "created_date": "",
        "changed_date": "",
    },
    {
        "id": 2,
        "title": "公告标题2",
        "created_date": "",
        "changed_date": "",
    }
]
```

### 2.2 获取单个公告 `GET` `/plan/announcement/<int:id>/`

- 成功状态码 `200`

```json
{
    "id": 1,
    "title": "公告标题1",
    "content": "markdown",
    "created_date": "",
    "changed_date": "",
}
```
