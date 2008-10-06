def foo(x, y):
    return x**y

print map(foo, range(10), range(10))