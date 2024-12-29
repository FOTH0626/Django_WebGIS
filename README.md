


# Django 结构

## Root Directory

### `setting.py`:配置
当新建一个module/app后,需要添加到 `INSTALLED_APPS` 
### `urls.py`:总路由,指向开发的app应用
### `wsgi.py`: python与web交互的接口,在开发中无需关心
### `manage.py`:django的cli管理工具

## App Directory
### `admin.py` admin profile
### `models.py` 数据库模型 file
### `urls.py` url路径
### `views.py` 视图函数处理


# Django 命令
`python -m django startapp {name}` 用来新建app(module)  

