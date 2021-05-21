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
    - [1.5 修改用户信息 `PATCH|PUT` `/user/user/<str:email>/`](#15-修改用户信息-patchput-useruserstremail)
    - [1.6 上传用户头像 `POST|PUT` `/user/user/<str:email>/avatar/`](#16-上传用户头像-postput-useruserstremailavatar)
  - [2 协会队员](#2-协会队员)
    - [2.1 获取所有队员信息 `GET` `/member/member/`](#21-获取所有队员信息-get-membermember)
    - [2.2 获取某一队员信息 `GET` `/member/member/<str:email>/`](#22-获取某一队员信息-get-membermemberstremail)
    - [2.3 修改队员信息 `PATCH|PUT` `/member/member/<str:email>/`](#23-修改队员信息-patchput-membermemberstremail)
    - [2.4 加入某一队伍 `POST` `/member/join-team/<int:team_id>/`](#24-加入某一队伍-post-memberjoin-teamintteam_id)
    - [2.5 请离当前队伍中某队员 `DELETE` `/member/leave-team/<str:email>/`](#25-请离当前队伍中某队员-delete-memberleave-teamstremail)
    - [2.6 添加自己的标签 `POST` `/member/tag/<str:tag_name>/`](#26-添加自己的标签-post-membertagstrtag_name)
    - [2.7 删除自己的标签 `DELETE` `/member/tag/<str:tag_name>/`](#27-删除自己的标签-delete-membertagstrtag_name)
    - [2.8 获取所有队伍信息 `GET` `/member/team/`](#28-获取所有队伍信息-get-memberteam)
    - [2.9 获取某一队伍信息 `GET` `/member/team/<int:team_id>/`](#29-获取某一队伍信息-get-memberteamintteam_id)
    - [2.10 创建并加入队伍 `POST` `/member/team/`](#210-创建并加入队伍-post-memberteam)
    - [2.11 修改队伍的信息 `PATCH|PUT` `/member/team/<int:team_id>/`](#211-修改队伍的信息-patchput-memberteamintteam_id)
    - [2.12 解散队伍 `DELETE` `/member/team/<int:tead_id>/`](#212-解散队伍-delete-memberteaminttead_id)
  - [3 任务计划](#3-任务计划)
    - [3.1 获取所有公告 `GET` `/plan/announcement/`](#31-获取所有公告-get-planannouncement)
    - [3.2 获取单个公告 `GET` `/plan/announcement/<int:id>/`](#32-获取单个公告-get-planannouncementintid)

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
- PATCH方法可修改部分字段，PUT方法需要修改全部字段，建议使用PATCH

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

### 1.5 修改用户信息 `PATCH|PUT` `/user/user/<str:email>/`

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

## 2 协会队员

### 2.1 获取所有队员信息 `GET` `/member/member/`

- 成功状态码 `200`

```json
[
    {
        "user": {
            "email": "wrong7@wrong.wrong",
            "nickname": "测试队员1",
            "avatar": "http://127.0.0.1:8070/media/avatar/avatar_p5e3poE.jpg"
        },
        "role": "N",
        "realname": "测试姓名1",
        "stu_id": "2019123001"
    },
    {
        "user": {
            "email": "wrong8@wrong.wrong",
            "nickname": "测试队员2",
            "avatar": "http://127.0.0.1:8070/media/avatar/avatar_YQH5F6m.jpg"
        },
        "role": "N",
        "realname": "测试姓名2",
        "stu_id": "2019123002"
    }
]
```

### 2.2 获取某一队员信息 `GET` `/member/member/<str:email>/`

可以用`self`表示自己的email

- 成功状态码 `200`

```json
{
    "user": {
        "email": "wrong12@wrong.wrong",
        "nickname": "测试昵称6",
        "avatar": "http://127.0.0.1:8070/media/avatar/avatar_VYEbS3z.jpg",
        "role": "M",
        "college": "西北大学",
        "date_joined": "2021-05-15T17:30:06.321773+08:00"
    },
    "role": "R",
    "stu_id": "2017123006",
    "realname": "测试姓名6",
    "college": "软件学院",
    "department": "软件工程",
    "grade": 2017,
    "cf_id": "wrong_cf_id_6",
    "vj_id": "wrong_vj_id_6",
    "need_peer": false,
    "team": {
        "id": 1,
        "name_ch": "测试队伍1",
        "name_en": "test_team_1",
        "members": [
            {
                "user": {
                    "email": "wrong11@wrong.wrong",
                    "nickname": "测试昵称5",
                    "avatar": "http://127.0.0.1:8070/media/avatar/avatar_ISMz23z.jpg"
                },
                "role": "R",
                "realname": "测试姓名5",
                "stu_id": "2017123005"
            },
            {
                "user": {
                    "email": "wrong12@wrong.wrong",
                    "nickname": "测试昵称6",
                    "avatar": "http://127.0.0.1:8070/media/avatar/avatar_VYEbS3z.jpg"
                },
                "role": "R",
                "realname": "测试姓名6",
                "stu_id": "2017123006"
            }
        ]
    },
    "tags": [
        "dalao",
        "计算几何"
    ],
    "achievements": [
        {
            "id": 1,
            "name": "自闭冠军",
            "level": 2,
            "detail": "人都要没了"
        },
        {
            "id": 2,
            "name": "500题达成",
            "level": 2,
            "detail": "vj+cf的过题数达到500"
        }
    ]
}
```

### 2.3 修改队员信息 `PATCH|PUT` `/member/member/<str:email>/`

只能修改自己的信息，可以用`self`表示自己的email

|字段名|类型|例子|备注|必填|
|-|-|-|-|-|
|user.nickname|str|bad apple|昵称||
|user.college|str|西北工业大学|学校||
|cf_id|str|tourist|codeforces账号||
|vj_id|str|tourist|vjudge账号||
|need_peer|bool|true|是否需要队友||

- 成功状态码 `200`

response结果与查询队员信息相同

### 2.4 加入某一队伍 `POST` `/member/join-team/<int:team_id>/`

- 成功状态码 `204`

### 2.5 请离当前队伍中某队员 `DELETE` `/member/leave-team/<str:email>/`

可以用`self`表示自己的email

- 成功状态码 `204`

- 状态码 `403`

```json
{
    "detail": "未加入任何队伍"
}
```

- 状态码 `403`

```json
{
    "detail": "队伍中无此人"
}
```

### 2.6 添加自己的标签 `POST` `/member/tag/<str:tag_name>/`

- 成功状态码 `204`

### 2.7 删除自己的标签 `DELETE` `/member/tag/<str:tag_name>/`

- 成功状态码 `204`

### 2.8 获取所有队伍信息 `GET` `/member/team/`

- 成功状态码 `200`

```json
[
    {
        "id": 1,
        "name_ch": "测试队伍1",
        "name_en": "test_team_1",
        "members": [
            {
                "user": {
                    "email": "wrong11@wrong.wrong",
                    "nickname": "测试昵称5",
                    "avatar": "http://127.0.0.1:8070/media/avatar/avatar_ISMz23z.jpg"
                },
                "role": "R",
                "realname": "测试姓名5",
                "stu_id": "2017123005"
            },
            {
                "user": {
                    "email": "wrong12@wrong.wrong",
                    "nickname": "测试昵称6",
                    "avatar": "http://127.0.0.1:8070/media/avatar/avatar_VYEbS3z.jpg"
                },
                "role": "R",
                "realname": "测试姓名6",
                "stu_id": "2017123006"
            }
        ]
    },
    {
        "id": 2,
        "name_ch": "测试队伍2",
        "name_en": "test_team_2",
        "members": []
    }
]
```

### 2.9 获取某一队伍信息 `GET` `/member/team/<int:team_id>/`

可以用`-1`表示自己队伍的id

- 成功状态码 `200`

```json
{
    "id": 1,
    "name_ch": "测试队伍1",
    "name_en": "test_team_1",
    "members": [
        {
            "user": {
                "email": "wrong11@wrong.wrong",
                "nickname": "测试昵称5",
                "avatar": "http://127.0.0.1:8070/media/avatar/avatar_ISMz23z.jpg"
            },
            "role": "R",
            "realname": "测试姓名5",
            "stu_id": "2017123005"
        },
        {
            "user": {
                "email": "wrong12@wrong.wrong",
                "nickname": "测试昵称6",
                "avatar": "http://127.0.0.1:8070/media/avatar/avatar_VYEbS3z.jpg"
            },
            "role": "R",
            "realname": "测试姓名6",
            "stu_id": "2017123006"
        }
    ]
}
```

### 2.10 创建并加入队伍 `POST` `/member/team/`

|字段名|类型|例子|备注|必填|
|-|-|-|-|-|
|name_ch|str|纸片人|中文队名|✅|
|name_en|str|need a leg|英文队名|✅|

- 成功状态码 `201`

response结果与查询队伍信息相同

### 2.11 修改队伍的信息 `PATCH|PUT` `/member/team/<int:team_id>/`

只能修改自己的队伍，可以用`-1`表示自己队伍的id

|字段名|类型|例子|备注|必填|
|-|-|-|-|-|
|name_ch|str|纸片人|中文队名||
|name_en|str|need a leg|英文队名||

- 成功状态码 `200`

response结果与查询队伍信息相同

### 2.12 解散队伍 `DELETE` `/member/team/<int:tead_id>/`

只能解散自己的队伍，可以用`-1`表示自己队伍的id

- 成功状态码 `204`

## 3 任务计划

### 3.1 获取所有公告 `GET` `/plan/announcement/`

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

### 3.2 获取单个公告 `GET` `/plan/announcement/<int:id>/`

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
