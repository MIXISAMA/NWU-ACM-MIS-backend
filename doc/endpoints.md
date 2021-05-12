# Endpoints文档

## 目录

[toc]

## 规则

* url务必以`/`结束
  * `/user/<int:pk>/` ⭕️
  * `/user/` ⭕️
  * `/user` ❌
* 错误响应应有`detail`以及错误原因
  * 例

```json
{
    "detail" : "该用户已存在, 无法重新注册用户"
}
```

* 不同类型错误响应尽量使用不同的HTTP状态码，以方便前端根据状态码显示错误信息
* 通用权限错误响应状态码为401

```json
{
    "detail": "身份认证信息未提供。"
}
```

## Endpoints

### 1 登陆注册

#### 1.1 用户注册

* `/user/email-register/`:`POST`

```json
{
    "email": "xxx@xxx.xxx",
    "code": "123qwe",
    "nickname": "xxx",
    "password": "xxx"
}
```

* 201

```json
{
    "token": "Token xxx"
}
```

* 400

```json
{
    "detail": [
        "xx字段xx错误"
    ]
}
```

* 403

```json
{
    "detail": "验证码无效"
}
```

#### 1.2 向用户提供的邮箱发送验证码

* `/user/email-verification/<str:email>/`:`POST`
* 204
* 400

```json
{
    "detail": [
        "xx字段xx错误"
    ]
}
```

* 403

```json
{
    "detail": "该用户已注册"
}
```

* 412

```json
{
    "detail": "验证邮件发送失败"
}
```

#### 1.3 邮箱&密码登入

* `/user/email-login/`:`POST`

```json
{
    "username": "xxx@xxx.xxx",
    "password": "xxx"
}
```

* 200

```json
{
    "token": "Token xxx"
}
```

* 400

```json
{
    "non_field_errors": [
        "无法使用提供的认证信息登录。"
    ]
}
```
