def isSymmetry(it):
    if it < 10:
        return True
    s = str(it)
    mpoint = len(s)/2 + 1
    for idx in range(1, mpoint):
        if s[idx-1] != s[-idx]:
            return False
    else:
        return True

print [x for x in range(1000) if isSymmetry(x)]