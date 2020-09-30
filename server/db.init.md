### 数据库初始化步骤
1、安装好mysql（版本要求5.7.8+）
2、在mysql上创建名为aishare的数据库：
![](https://cdn.nlark.com/yuque/0/2020/png/662957/1600528877511-d6d7ed74-e5c4-435e-99ef-d718c9622f2b.png)
3、在项目的server/server/settings.py文件中，将DATABASE部分改为：
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'aishare',
        'USER': 'root',
        'PASSWORD': '123456',
        'HOST': '127.0.0.1',
        'PORT': '3306',
    }
}
```
这里请注意，USER和PASSWORD因人而异，由自己安装数据库时的设置而定。
4、在pycharm的terminal中输入：
`python manage.py makemigrations system`
接下来再运行命令：
`python manage.py migrate`
接着，创建超级用户：
`python manage.py createsuperuser`
这里用户名，邮箱，密码可以自己设置。
5、成功运行，在页面输入自己超级用户的账户和密码即可登录，如果想要增删改一些数据，可在界面上提供的django后台进行操作。