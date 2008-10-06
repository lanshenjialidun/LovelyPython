def foo(perms, x):
    i = 0
    while perms[i]**2 <= x:
        if x%perms[i] == 0:
            return perms
        else:
            i += 1
    else:
        perms.append(x)
    return perms

print reduce(foo, range(5, 100, 2), [2, 3])