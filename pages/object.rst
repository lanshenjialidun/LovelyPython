##language:zh
##OBP项目图书reST通用文章模板
#format rst
:status: 草稿|校对|正式;HuangYi;完成度60%;

.. contents::
  :depth: 3

========
类与实例
========

通常大家说的是"类与对象"，不过 python 中万物皆"对象"，对象这个词语的含义太宽泛。
实际上我们这里要讨论的只是用户自定义的类和这些类的实例而已，类及其实例都只是对象这个大家族中的一员。

定义类
------

::
  
  >>> class Klass(object):
  ...     ' docstring... '
  ...     def __init__(self, a):
  ...         self.attr_a = a
  ...
  >>> Klass.__doc__
  ' docstring... '
  >>> obj = Klass(1)
  >>> obj.attr_a
  1

关键字 ``class`` 定义一个类， ``Klass`` 是类的名字，括号中 ``object`` 是它的基类，
python 中所有的 ``class`` 都是从 ``object`` 继承而来
（虽然在目前的 python 版本中还存在一类所谓的 old-style class ，他们是不从 ``object`` 继承而来的，不过这只是为了保持向后兼容性并且很快就要在 python3.0 中彻底退出历史舞台，所以我们这里直接忽略它了）。

和许多语言不同的是，python 中构造函数叫做 ``__init__`` ，第一个参数传递的就是将要初始化的实例对象本身，类似许多语言中的 ``this`` 。

和函数一样，class 也可以定义文档字符串，同样是通过 ``__doc__`` 访问。

创建实例对象并不需要学习新的语法，创建实例和函数调用一摸一样。传给 ``Klass`` 的参数最终传给构造函数 ``__init__`` ，而返回值便是新创建的实例对象。

属性
----

在构造函数中的 ``self.attr_a = a`` 便给 ``self`` 这个对象增加了一个名为 ``attr_a`` 的属性，其绑定的对象就是传入的参数 ``a`` 所绑定的对象。

对象的 ``__dict__`` 属性可以让你以字典的方式查看对象的所有属性：::

  >>> obj.__dict__
  {'attr_a': 1}

不光在构造函数中，其实在任何时候你都可以给对象增加属性，你只需要给不存在的属性绑定对象即可，python 会自动创建不存在的属性：::

  >>> obj.attr_b = 1
  >>> obj.attr_b
  1
  >>> obj.__dict__
  {'attr_b': 1, 'attr_a': 1}

讲到属性，需要明确的一个概念就是不光实例对象有属性，类也是对象，类自然也有属性！::

  >>> class Klass1(object):
  ...     ' docstrign... '
  ...     class_attr1 = 'hello'
  ...     def __init__(self, a):
  ...         self.attr_a = a
  ...
  >>> Klass1.class_attr1
  'hello'

我们也可以使用 ``__dict__`` 来查看类对象的所有属性：

  >>> from pprint import pprint
  >>> pprint(dict(Klass1.__dict__))
  {'__dict__': <attribute '__dict__' of 'Klass1' objects>,
   '__doc__': ' docstrign... ',
   '__init__': <function __init__ at 0x00FBAEF0>,
   '__module__': '__main__',
   '__weakref__': <attribute '__weakref__' of 'Klass1' objects>,
   'class_attr1': 'hello'}

class 的属性比较多，为了方便查看我们使用了 ``pprint`` 模块中的 ``pprint`` 方法，其功能是以更可读的方式输出一些复杂数据结构，
具体用法可以查看 python 自带手册。

当访问实例对象的属性时，如果属性不存在，将自动查找其对应的类对象的属性：::

  >>> obj1 = Klass1(1)
  >>> obj1.class_attr1
  'hello'

类属性是和类对象的属性，同一个类对象的所有实例都共享同一份类属性：::

  >>> obj2 = Klass1(2)
  >>> Klass1.class_attr1 = 'changed'
  >>> obj1.class_attr1
  'changed'
  >>> obj2.class_attr1
  'changed'

方法
----

::

  >>> class Klass(object):
  ...     def __init__(self, name):
  ...         self.name = name
  ...     def greet_to(self, name):
  ...         print self.name, 'say hello to', name
  ...
  >>> obj = Klass('HuangYi')
  >>> obj.greet_to('you')
  HuangYi say hello to you
  >>> pprint(dict(Klass.__dict__))
  {'__dict__': <attribute '__dict__' of 'Klass' objects>,
   '__doc__': None,
   '__init__': <function __init__ at 0x010122B0>,
   '__module__': '__main__',
   '__weakref__': <attribute '__weakref__' of 'Klass' objects>,
   'greet_to': <function greet_to at 0x010122F0>}

方法其实也是属性！准确地说还是属于类对象的属性。在 ``Klass`` 中我们定义了两个方法： 构造函数 ``__init__`` 和普通方法 ``greet_to`` 。

方法本质上说其实是对函数的一层简单包装，这层包装的作用就是将调用方法的这个对象当做第一个参数传进去，
所以在定义方法的时候千万别忘了声明第一个参数，按照约定，这个参数我们叫它 ``self`` 。::

  >>> obj.greet_to
  <bound method Klass.greet_to of <__main__.Klass object at 0x0101C550>>
  >>> Klass.__dict__['greet_to']
  <function greet_to at 0x010122F0>

直接通过实例对象 ``obj`` 访问属性 ``greet_to`` 时得到的其实是对这个函数包装后产生的"方法"。
直接通过 ``Klass.__dict__`` 取 ``greet_to`` 属性实际绑定的对象时，你得到的才是这个还没有经过包装的"纯净"的函数！

  >>> func = Klass.__dict__['greet_to']
  >>> func(obj, 'you')
  HuangYi say hello to you

如果你要问这个包装是何时以及如何产生的，这其实又涉及到 python 中另一个相对高级的概念： Descriptors。
如果有兴趣可以查看 Raymond 写的精彩教程（http://users.rcn.com/python/download/Descriptor.htm），本书将不做更多介绍。

不过当我们认识到方法与函数的这一层关系后，我们已经可以利用它来实现一些有意思的功能了，比如在运行时给类添加方法：::

  >>> class Klass(object):
  ...     pass
  ...
  >>> obj = Klass()
  >>> def print_id(obj):
  ...     print id(obj)
  ...
  >>> Klass.print_id = print_id # 等价于 Klass.__dict__['print_id'] = print_id
  >>> obj.print_id() # 等价于 print_id(obj) 
  16892848

特殊属性
--------

所谓特殊属性就是那些名字前后都是两个下划线的属性。这种属性往往都会被 python 特殊处理，用来实现一些特定功能用的。
所以定义你自己的属性时千万记得不要定义这种"风格"的属性。

构造析构函数
============

构造函数我们前面已经见识过了 ``__init__`` 便是，而析构函数叫做 ``__del__`` 。

TODO 介绍析构函数

操作符重载
==========

TODO

自定义属性访问
==============

TODO

继承
----

小结
-----


练习
-----

.. macro:: [[PageComment2(nosmiley=1, notify=1)]]


.. macro:: -- HuangYi [[[DateTime(2007-06-26T05:39:25Z)]]]

