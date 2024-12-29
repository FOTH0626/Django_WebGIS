# Django 架构
MVT架构
## MVC架构
MVC是软件工程中的经典架构，分离为`Model`,`View`,`Controller`三部分。
- `Model`充当着数据库存储数据的接口。它维护Web应用程序的数据并处理逻辑数据结构
- `View`是一个用户界面，负责向用户显示模型数据，并从用户那获取数据。
- `Controller`代表着应用程序的逻辑部分。用户与`View`交互并发送请求，由`Controller`处理并返回响应。

## MVT架构
Django对传统的MVC架构进行了修改。并称为MVT架构，即`Model`,`View`,`Template`。  
- `Model` 与传统的MVC架构类似，`Model`担任了与数据库交互的任务。
```python
# import the models class from Django
from django.db import models

# creating a model class below
class Movie(models.Model):
    title = models.CharField(max_length=25)
    director = models.CharField(max_length=25)
    release_date = models.DateField()

    def __str__(self):
        return self.title
```
通过创建一个继承models.Model 子类的 Python 类来定义它。  
这意味着我们刚刚创建的类“Movie”是一个 Django 模型，现在可以使用 Django 的所有内置 ORM 功能。
Django不鼓励使用`__init__`方法,Django内部会自动实例化作为代替,所以Django官方推荐直接定义字段。
```python
# field definition examples
title = models.CharField(max_length=25)
director = models.CharField(max_length=25)
release_date = models.DateField()
```
>对于CharField属性，虽然不是必须的，但建议设置最大长度。

- `View`  与MVC架构不同，`View`充当着`Model data` 和 `Template` 的桥梁。它根据用户请求，从数据库检索数据并将模板和数据一起呈现
```python
from django.shortcuts import render
from .models import Movie

def movie_list(request):
    # my view request
    movies = Movie.objects.all()

    # render to the specific template
    return render(request, 'movies/movie_list.html', {'movies': movies})
```
在这个示例中，我们导入Movie模型和Django渲染函数， `movie_list`函数接受request，这是Django的HTTPRequest对象。代表了客户端向服务器发送的请求。
- `Template` 和MVC的`View`类似，`Template`负责用户界面，它处理静态组件，包括`HTML`.  
Django 中的模板充当 Web 应用程序的蓝图或布局。它们有助于创建 HTML 页面，这些页面可以使用通过视图函数从模型查询的数据来显示动态内容。
Django模板主要是HTML，模板获取查询的函数并按设计实现它。如下。
```html
<!-- example of a Django template -->

<!DOCTYPE html>
<html>
<head>
    <title>Movie List</title>
</head>
<body>
    <h1>List of Movies</h1>
    {% if movies %}
        <ul>
            {% for movie in movies %}
                <li>{{ movie.title }} - {{ movie.director }} - {{ movie.release_date }}</li>
            {% endfor %}
        </ul>
    {% else %}
        <p>No movies available.</p>
    {% endif %}
</body>
</html>
```

---
MVT中没有单独的`Controller`  
![img.png](img/img.png)

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

