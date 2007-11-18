##language:zh
#format rst

.. contents::

:status: 草稿 ;HuangYi; 100%;

===================
过程控制
===================

python 向来秉承简洁的设计原则，在语法的设计上体现得尤为明显！
稍有编程经验的朋友对下面这些语法应当不会陌生。

对于许多读者来说，可能只需要注意两点，本章的内容就可以飞快得浏览过去了：
一是 python 以缩进控制作用范围并且缩进都以冒号开头；
二是所有这些过程控制语句都可以跟个 ``else`` 子句！
``if`` 语句后面跟 ``else`` 自不必说，连 ``for`` 、 ``while`` 语句也可以跟 ``else`` 子句！
不过不同 ``else`` 子句的含义自然会根据所处的环境不同而有所不同。

if 分支
=========

最基本的用法：
::
    
  if a == b:
      print 'a 等于 b'
  else:
      print 'a 不等于 b'

也许你还需要更细致地控制：
::
    
  if a == b:
      print 'a 等于 b'
  elif a < b:
      print 'a 小于 b'
  elif a > b:
      print 'a 大于 b'
  else:
      print '在本宇宙中这是不可能滴！'

``elif`` 就是 ``else if`` 的缩写。

.. topic:: 没有 switch

  python 没有 ``switch`` 语句，不过 ``if elif else`` 组合已经足以应付大部分情况。
  而对于另外的一种 ``switch`` 应用场景，python 还有更加优雅的方式来处理，请看：
  ::

    # 伪码 根据输入的不同参数选择程序的不同行为
    switch( sys.argv[1] ):
        case '-e':
            walk_cd()
        case '-d':
            search_cd()
        ...
        default:
            raise CommandException("Unknown Commend: " + sys.argv[1])

    # 使用 if 替代
    if sys.argv[1]=='-e':
        walk_cd()
    elif sys.argv[1]=='-d':
        search_cd()
    ...
    else:
        raise CommandException("Unknown Command: " + sys.argv[1])

    # 更好的做法
    commands = {
        '-e'   : walk_cd,
        '-d'   : search_cd,
    }
    try:
        commands[ sys.argv[1] ]()
    except KeyError:
        raise CommandException("Unknown Command: " + sys.argv[1])

  最后一种方式不管从可读性（这是显然的）、性能（哈希表 vs 普通查找）上都高出很多。
  另外最后一种做法将参数与行为的映射完全独立出来了，一来修改起来及其方便，
  到时候也很容易将它们分离到配置文件中去。

.. topic:: 三元运算符

  还记得上一章 python 数据类型的习题 1 吗？我们要求您用 and 和 or 操作符模拟 c 语言的 ? : 三元操作符。
  实际上在 python2.5 以前，这确实是一个还算实用的技巧，不过 python2.5 中应广大 fans 的强烈要求，
  终于加入了新的语法，从此可以用更优美的方式表达这种常用分支：
  ::
    
    >>> def get_length(s):
    ...     # 等价于:
    ...     # if(s!=None)
    ...     #     return len(s)
    ...     # else:
    ...     #     return len('None')
    ...     return len(s) if s!=None else len('None')
    ...
    >>> get_length(None)
    4

  用 and or 技巧可以写成：
  ::

    >>> def get_length(s):
    ...     return s!=None and len(s) or len('None')
    ...
    >>> get_length(None)
    4

  不过显然是第一种写法看起来顺眼一些，不是吗 ;-)

for 循环
=========
::

  for item in [1, 2, 3]:
      print item

上面的代码其实就是遍历 ``some_list`` 列表，将其中每一个元素都打印出来。

所以的循环语句（其实也就是这里的 ``for`` 和后面的 ``while`` 了）中都可以使用这么两条语句：
``break`` 和 ``continue`` 。 ``break`` 表示要退出循环， ``continue`` 是说直接进入到下一轮
的循环中去吧：
::

  >>> for item in range(10):
  ...     if item<5:         # 遇到比 5 小的
  ...         continue       # 进入下一轮循环
  ...     else:              # 否则遇到的是大于等于 5 的
  ...         print item     # 输出
  ...         break          # 并直接退出循环
  ...
  5

其实上面这个例子中的循环体也可以这么写的：::

  if item>=5:
      print item
      break


前面说过， ``for`` 语句后面可以跟 ``else`` 子句，在这里 ``else`` 子句含义是：如果 for 一直循环到了末尾
，最后正常退出循环，那么随后就会执行它的 ``else`` 子句，否则由于 ``break`` 语句或异常等原因退出循环的，
则不会执行 ``else`` 子句。

其实在程序中我们就常常就会遇到这样的场景：对某个列表中每一个元素执行某个操作，
如果成功执行则马上 ``break`` 跳出循环，如果遍历完整个列表，发现没有一个元素满足要求，
也就是意味着遍历失败，那么处理失败情况的语句就可以放在 ``else`` 子句中了，比如：
::

  >>> for item in range(10):
  ...     if item<10:
  ...         continue
  ...     else:
  ...         print item
  ...         break
  ... else:
  ...     print '没有大于等于10的数字'
  ...
  没有大于等于10的数字

.. topic:: 两种风格的 ``for`` 语句
 
  如果你熟悉 c 语言的话，便会看出 python 的 for 和 c 的 for 的不同，
  表面上的语法差异自然容易看出，但实际上他们的含义却是有根本的不同的。
  要类比 python 这种形式的 ``for`` 语句的话，大家可以想象某些语言的 ``for in`` 或者 ``foreach`` 之类的语法。
  ::

    /* c 语言 */
    for(int i=0; i<count; i++){
        ...
    }
    
    # python
    for item in a_iterable:
        ...
 
  简单地说， c 语言形式的 ``for`` 语句的工作原理是这样的：取第0个、第1个、第2个，一直取到最后一个这样子。
  而迭代器这种呢，就是对迭代器取下一个、取下一个、取下一个，一直取到迭代器自己喊停为止。
  实际上 python 的 ``for`` 语句是同时支持这两种风格的。

  我们先来解剖一下 python 的 ``for`` 语句：::

    for item in obj:
        ...

  如果 ``obj`` 对象实现了 ``__iter__`` 方法，
  也就是说它是个迭代器，那这就是迭代器风格的 ``for`` 语句，
  而上面这段代码也就等价于：::

    iterator = iter(obj) # 获取迭代器。
    # iter(obj) 等价于 obj.__iter__()
    try:
        item = iterator.next() # 取下一个
        ...
        item = iterator.next() # 取下一个
        ...
    except StopIteration:      # 迭代器喊停了（参见 异常处理_ ）
        pass

  如果上面的 ``obj`` 对象实现了 ``__getitem__`` 方法，
  也就是说它支持索引操作，这就成了 c 语言风格的那种迭代器，
  这段代码便等价于：::
    
    try:
      item = obj[0]      # 取第0个
      # obj[0] 等价于 obj.__getitem__(0)
      ...
      item = obj[1]      # 取第1个
      ...
    except StopIteration:      # 取到最后一个了（参见 异常处理_ ）
        pass

  最后再测试一把：::

    >>> class Indexable(object):
    ...     def __getitem__(self, i):
    ...         if i>10:
    ...             raise StopIteration()
    ...         print 'get object %d'%i
    ...
    >>> class Iterable(object):
    ...     def __init__(self):
    ...         self.counter = 0
    ...     def __iter__(self):
    ...         return self
    ...     def next(self):
    ...         if self.counter>10:
    ...             raise StopIteration()
    ...         print 'get next, current is %d'%self.counter
    ...         self.counter += 1
    ...
    >>> container = Indexable()
    >>> for i in container:pass
    ...
    get object 0
    get object 1
    get object 2
    get object 3
    get object 4
    get object 5
    get object 6
    get object 7
    get object 8
    get object 9
    get object 10
    >>> container = Iterable()
    >>> for i in container:pass
    ...
    get next, current is 0
    get next, current is 1
    get next, current is 2
    get next, current is 3
    get next, current is 4
    get next, current is 5
    get next, current is 6
    get next, current is 7
    get next, current is 8
    get next, current is 9
    get next, current is 10

while 循环
============

相对 for 来说 while 就简单多了：::

  while not self.accepted_by(her):
      trace(her)

只要 condition 为 True ，也就是满足该条件，就不停执行里面的代码。

用 while 写死循环还是比较方便：::

  while True:
      print 'running...'

异常处理
============

捕捉异常
---------

::
  
  try:
      code_block()
      ...
  except SomeException, e:
      do_some_thing_with_exception(e)
  except (Exception1, Exception2), e:
      do_some_thing_with_exception(e)
  except:
      do_some_thing_with_other_exceptions()
  else:
      do_some_thing_when_success()
  finally:
      do_some_thing()

抛出异常
--------

::

  raise SomeException("some reason")

自定义异常
----------

::

  class MyException(Exception):
      ...

小结
==========

#. 学习了几个流程控制的语法，体会 python 语法设计的简洁、正交。

#. 了解了所谓迭代器的概念

#. 知道了 __getitem__ 与索引的关系

#. 了解异常处理的抛出和捕获

练习
===========

#. 使用 while 语句演示两种 for 语句的过程。

.. macro:: [[PageComment2(nosmiley=1, notify=1)]]

