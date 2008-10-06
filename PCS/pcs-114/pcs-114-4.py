def foo(x):
    return x%2==0

print filter(foo, range(100))