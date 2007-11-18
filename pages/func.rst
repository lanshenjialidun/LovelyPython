##language:zh
#format rst

.. contents::

:status: 草稿 ;HuangYi; 99%;

===================
函数
===================

函数定义
==========

函数定义很简单：::

  >>> def add(a, b):
  ...     '返回 a 和 b 的和'
  ...     return a+b
  ...

这样就定义了函数 ``add`` ，接受两个参数： ``a`` 和 ``b`` 。
试验一下：::

  >>> add(1, 2)
  3

python 中万物皆对象，函数也不例外：::

  >>> add
  <function add at 0x00C30CF0>
  >>> id(add)
  12782832
  >>> type(add)
  <type 'function'>

函数定义中第一个行的字符串就是它的文档字符串，
可以通过函数对象的 ``__doc__`` 属性访问：::

  >>> print add.__doc__
  返回 a 和 b 的和

使用 ``help`` 可以获得更多关于如何使用函数 ``add`` 的信息：::

  >>> help(add)
  Help on function add in module __main__:

  add(a, b)
      返回 a 和 b 的和

OK，现在大家对函数对象有了一个基本的认识，我们来对 ``add`` 进行一点升级。
考虑到我们做加法时经常进行加一操作，我们可以让参数 ``b`` 默认为 ``1`` ：::

  >>> def add(a, b=1):
  ...     '返回 a 和 b 的和, b 默认为 1'
  ...     return a+b
  ...

这样便使得参数 ``b`` 成为可选参数，python 中我们叫它关键字参数，前面的 ``a`` 叫做位置参数，因为它是通过所处的位置来进行参数匹配的。
继续试验：::

  >>> add(1)
  2
  >>> add(1, 1)
  2
  >>> add(1, b=1)
  2

传递关键字参数时是不需要考虑顺序的，而位置参数，则需要传参数的时候按照参数定义的位置一一对应，
所以才叫做位置参数的嘛。另外位置参数与关键字参数之间也并非格格不入，你可以以关键字参数的形式
传递位置参数，也可以以位置参数的形式传递关键字参数（其实大部分时候并不推荐这么做，显然这很容易导致混乱），唯一的规则就是关键字参数一定要在位置参数的后面，否则会引起歧义。::

  >>> def function(a, b, c=1, d=2):print a, b, c, d
  ...
  >>> function(1, 2, c=3, d=4)
  1 2 3 4
  >>> function(1, 2, 3, 4)
  1 2 3 4
  >>> function(a=1, b=2, c=3, d=4)
  1 2 3 4
  >>> function(1, b=2, c=3, d=4)
  1 2 3 4
  >>> function(a=1, 2, c=3, d=4)
  SyntaxError: non-keyword arg after keyword arg

神奇的星号
============

传递实参和定义形参（所谓实参就是调用函数时传入的参数，形参则是定义函数是定义的参数）的时候，
你还可以使用两个特殊的语法：``*`` ``**`` 。

* 调用函数时使用 ``*`` ``**`` ::
    
    test(*args)

  ``*`` 的作用其实就是把序列 ``args`` 中的每个元素，当作位置参数传进去。比如上面这个代码，如果 ``args`` 等于 ``(1,2,3)`` ，那么这个代码就等价于 ``test(1, 2, 3)`` 。 ::

    test(**kwargs)

  ``**`` 的作用则是把字典 kwargs 变成关键字参数传递。比如上面这个代码，如果 ``kwargs`` 等于 ``{'a':1,'b':2,'c':3}`` ，那这个代码就等价于 ``test(a=1,b=2,c=3)`` 。

* 定义函数参数时使用 ``*`` ``**`` ::

    def test(*args):
        ...
  
  定义函数参数时 ``*`` 的含义又要有所不同，在这里 ``*args`` 表示把传进来的位置参数都装在元组 ``args`` 里面。比如说上面这个函数，调用 ``test(1, 2, 3)`` 的话， ``args`` 的值就是 ``(1, 2, 3)`` 。::

    def test(**kwargs):
        ...

  类似的， ``**`` 就是针对关键字参数和字典的了。 调用 ``test(a=1,b=2,c=3)`` 的话， ``kwargs`` 的值就是 ``{'a':1,'b':2,'c':3}`` 了。

普通的参数定义和传递方式和 ``*`` 们都可以和平共处，不过显然 ``*`` 必须放在所有位置参数的最后，而 ``**`` 则必须放在所有关键字参数的最后，否则就要产生歧义了。

lambda
==========

一般来说，所谓的 ``lambda`` 其实就是匿名函数的意思，用来定义没有名字的函数对象，python 的也不例外。
不过 python 的 ``lambda`` 却是被阉割过的，python 的 ``lambda`` 中其实只能包含表达式！
这也是 python 为了保持代码的可读性而作的一点方便性的牺牲了。
所以为了保持代码的整洁，请您给函数起个名字。

既然是阉割过的，python 的 ``lambda`` 语法也就不会复杂到哪去了：::

  lambda arg1, arg2 ... : expression

``lambda`` 关键字后就是逗号分隔的形参列表，冒号后面是一个表达式，表达式求值的结果作为 ``lambda`` 的返回值。

虽然 ``lambda`` 的滥用会严重影响代码可读性，不过在适当的时候使用一下 ``lambda`` 来减少几下键盘的敲击还是有其实际意义的，
比如做排序的时候，用 ``data.sort(key=lambda o:o.year)`` 显然就比：::

  def get_year(o):
      return o.year
  data.sort(key=func)

要方便许多！

只能包含表达式的规定基本上就将 ``lambda`` 的应用场景限制在这种小场合了，所以当其函数内容增多，还是尽量给它起个合适的名字吧 ;-)

闭包(closure)
================

python 支持函数的嵌套，也就是传说中的闭包！::

  >>> def make_adder(n):
  ...     def add(n1):
  ...         return n+n1
  ...     return add
  ...
  >>> adder3 = make_adder(3)
  >>> adder3(5)
  8
  >>> adder5 = make_adder(5)
  >>> adder5(5)
  10

所谓闭包，就是在嵌套函数中内部函数对象本身包含了外部函数对象的名字空间。
就像上面代码中的 ``add`` 函数，它本身就拥有外部函数 ``make_adder`` 的名字空间，
也就可以访问 ``make_adder`` 函数中的名字 ``n`` 了。

TODO 闭包的主要用途

装饰器(decorator)
===================
::
  
  @log
  def test(a, b):
      pass

其中 ``log`` 就是个别人写好的装饰器，作用就是在调用 ``test`` 的前后分别输出个
``enter test`` 和 ``exit test`` ，使用符号 ``@`` 来应用这个装饰器。

用最容易理解的方式来说，装饰器其实很简单，我们给您看上面这段代码的另一种写法，就很清楚了：
::

  def test(a, b):
      pass
  test = log(test)

是的，上面两段代码完全等价！实际上在 python2.4 加上 ``@``
语法之前，大家也一直都是用后面这种方法在做的。

是不是很简单？但其实又不是那么简单。要从复杂的来讲，它和所谓 AOP
之类的神秘概念都扯得上关系。但 python 就是这样，你总是能够以最简单的方式完成
一些看似复杂的工作 ;-)

那么这个 ``log`` 应该如何来写呢？
其实有经验的读者从后面这段代码中应该已经能够看出端倪。
``log`` 无非就是接受一个函数作为参数同时返回一个新函数的函数，说起来像绕口令，
不如看代码：
::
  
  def log(func):
      def wrapper(*args, **kw):
          print 'enter', func.__name__
          func(*args, **kw)
          print 'exit', func.__name__
      wrapper.__name__ = func.__name__
      wrapper.__globals__ = func.__globals__
      return wrapper

``log`` 里面定义另一个叫 ``wrapper`` 的嵌套函数，它把所有接受到的参数简单地全部传给
``func`` ，并在调用前后输出一些信息。
最后对 ``wrapper`` 的一些属性进行偷梁换柱之后，就将它返回了，
于是这个 ``wrapper`` 就变成了一个被包装过的如假包换的 ``func`` 了！

现在我们的 ``log`` 只是简单地将信息输出到了标准输出，
要是可以随意指定 ``log`` 输出到的文件该多好啊，
也就是说，我们希望 ``log`` 变成这样：
::
  
  @log(open('default.log', 'w')) # 这里 open 函数是以写方式打开一个文件，并返回这个文件对象
  def test(a, b):
      pass

那么这个 ``log`` 应该怎么实现呢？我们先来看一下上面这个代码的等价版本：
::

  def test(a, b):
      pass
  test = log(open('default.log'))(test)

貌似这里括号有点多，但仔细分析一下就看得出来， ``log`` 还是一个函数，它接受一个文件对象做参数，
并返回一个新函数，而这个新函数就是上面说过的装饰器（也就是绕口令：接受一个函数作为参数并返回另一个函数的函数）。
ok，我们还是看代码吧：
::
  
  def log(fileobj):
      def logger(func):
          def wrapper(*args, **kw):
              print >> fileobj, 'enter', func.__name__
              func(*args, **kw)
              print >> fileobj, 'exit', func.__name__
          wrapper.__name__ = func.__name__
          return wrapper
      return logger

理清思路了吗？ ``open('default.log')`` 返回一个文件对象，然后我们把它传给了 ``log`` ，
``log`` 返回了这个 ``logger`` 函数，然后我们调用这个 ``logger`` 函数，把 ``test`` 函数传给了它，
它再返回一个 ``wrapper`` 函数，而这个 ``wrapper`` 函数正是一个包装过了的“新” ``test`` 函数。

其实我们还是感觉这个 ``log`` 的功能有点弱，它只能记录下 enter、exit 和函数名，
作为一个有用的 ``log`` ，怎么说也应该能够记录下函数调用所用的参数和函数的返回值的吧，没问题：
::
  
  def log(fileobj):
      def logger(func):
          def wrapper(*args, **kw):
              print >> fileobj, 'calling function', func.__name__,\
                          'with position arguments', ', '.join(map(str, args)),\
                          'and keyword arguments',\
                          ', '.join('%s=%s'%key_value for key_value in kw.items())
              result = func(*args, **kw)
              print >> fileobj, 'function', func.__name__, 'returns', result
          wrapper.__name__ = func.__name__
          return wrapper
      return logger

从上面这个例子中你应该温习到了不少熟悉的内容了吧 ;-) 里面用到了字符串模板、字符串的 ``join`` 方法、
``map`` 函数，Generator expressions、字典，不错，真是个好例子！

现在让我们打开 python shell，试试这个 log 的强大威力吧！
先把上面的代码拷进 python shell（你应该可以从光盘中找到代码），
然后：
::

  >>> import sys
  >>> @log(sys.stdout) # sys.stdout 就是标准输出，也就是 print 默认输出的地方
  ... def plus(a, b):
  ...     return int(a) + int(b)
  ...
  >>> plus(1, b=2)
  call function plus with position arguments 1 and keyword arguments b=2
  function plus returns 3
  >>>
  >>> logfile = open('func.log', 'w')
  >>> @log(logfile)
  ... def plus(a, b):
  ...     return int(a) + int(b)
  ...
  >>> plus(1, b=2)
  >>> logfile.flush()
  >>> print open('func.log').read()
  call function plus with position arguments 1 and keyword arguments b=2
  function plus returns 3

江湖上还流传一个叫 decorator 的库（http://www.phyast.pitt.edu/~micheles/python/documentation.html），可以帮助你简化 decorator 的编写。

生成器(generator)
=====================
::

  >>> def number_generator():
  ...     i = 0
  ...     while True:
  ...         yield i
  ...         i += 1
  ...
  >>> for item in number_generator():
  ...     print item
  ...
  0
  1
  2
  # 省略后面输出的无穷个数字

是不是很神奇？哈哈。啥？停不下来了？按一下 Ctrl+C 吧。

python 的生成器其实也可以有两种讲法，
从简单的来讲，它就是方便的实现迭代器的方法而已，就像上面用的那样。
从复杂的来讲呢，python 的生成器其实正是神秘的 continuation ！

实际上大部分时候我们都只需要把 ``yield`` 当成是快速实现迭代器的工具来用就行了。
神秘的 continuation 已经超出了本身的范畴。

小结
=======

和许多语言不同，在 python 中，函数是一等公民，函数也是对象，这也是在 python 中进行函数式编程的基础，理解这一点非常重要。当你越深入学习 python，越能感受到函数在 python 中的重要地位。

练习
=======

.. macro:: [[PageComment2(nosmiley=1, notify=1)]]

