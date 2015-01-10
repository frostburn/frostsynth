def powers(x, n0, n1=None):
    if n1 is None:
        n1 = n0
        n0 = 1
    if n0 == 0:
        r = 1
    elif n0 == 1:
        r = x
    else:
        r = x ** n0
    rs = [r]
    for _ in range(n1 - n0):
        r *= x
        rs.append(r)
    return rs
