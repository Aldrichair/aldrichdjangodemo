# aldrichdjangodemo

### 一个关于aldrichair的django项目练手 (前后分离 B2C商城项目)

#### 创建数据库

```mysql
CREATE DATABASE `MeiDuoB2C` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci */;
```

#### 依据apps.users.models写入数据模型

```python
class User(AbstractUser):
    mobile = models.CharField(max_length=11, unique=True)   # 手机号码为字符型

    class Meta:
        verbose_name = '用户管理'
        verbose_name_plural = verbose_name
        db_table = 'tb_user'
```

#### 终端执行

```
python manage.py makemigrations
python manage.py migrate
```

#### 创建超级管理员

```
python manage.py createsuperuser
```

#### 于前端文件front_end_pc/front_end_pc目录下启动前端服务器命令

```
python -m http.server 8080
```

#### 运行项目前,需启动redis服务

