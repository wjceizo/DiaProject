# API 文档

| 模块名 | 命名空间  |
| --- | ----- |
| 登录  | auth  |
| 用户  | user  |
| 音频  | audio |

## Auth

### 注册

/auth/register

- 方法：post

- 描述：用户注册

- 请求格式：
  
  ```json
  {
        "username": "user",
        "password_hash": "abc123",
        "email": "user@example.com",
        "name": "Zhao",
        "location": "zhangjiagang",
        "lang": "putong"
  }
  ```

### 登录

/auth/login

- 方法：post

- 描述：用户注册

- 请求格式：
  
  ```json
  {
    "username": "user",
    "password": "abc123"
  }
  ```

### 用户

/auth/users

- 方法：get

- 描述：获取用户用户名

- 请求对象：无

- 参数：
  
  - page=`0`
  
  - pageSize=`5`
  
  - order=`ASC`/`DESC`

- 响应格式：

```json
[
    "total":100
    "page": 0,
    "pageSize": 5,
    "order": "ASC",
    "orderBy":"id",
    "users":
        {
            "username": "wang",
            "id": "235"
        },
        {
            "username": "wang",
            "id": "235"
        },
        ...
] 
```

- 用例：
  
  https://127.0.0.1:5000/auth/users/pagr=1&pageSize=5

## Audio

### 添加词

/audio/words

- 方法：post

- 描述：添加新的词

- 请求对象：

```json
{
    "stem":"一",
    "meaning":"计数法中的第一个",
    "comm":"数一"   
}

```

*comm可以省略*

## User

### 录音录入

/user/word/{word_id}/record

1. 方法：post

2. 描述：用户添加录音

3. 请求对象：
   
   **格式为form**
   
   | Key     | Value      | Type |
   | ------- | ---------- | ---- |
   | record  | 录音文件       | file |
   | token   | efsdfini.. | txt  |
   | snd_abs | hello      | txt  |

### 录音更新

/user/word/{word_id}/update

1. 方法：post

2. 描述：用户跟新录音

3. 请求对象：
   
   **格式为form**
   
   | Key     | Value      | Type |
   | ------- | ---------- | ---- |
   | record  | 录音文件       | file |
   | token   | efsdfini.. | txt  |
   | snd_abs | hello      | txt  |

### 用户删除

/user/word/{word_id}/delete

1. 方法：post

2. 描述：用户删除录音

3. 请求对象：
   
   {
   
   "token": "efsdfini.."
   
   }

### 录音全部删除

/user/word/all/delete

1. 方法：post

2. 描述：用户删除全部录音

3. 请求对象：
   
   ```json
   {
       "token": "efsdfini.."
   }
   ```
