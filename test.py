import numpy as np
def main():
    f = open('DBLPdata/collaboration.txt', 'r')
    l = 0
    t = []
    z = 0
    ft = open('DBLPdata/coll%1000.txt', 'w')
    for row in f:
        l = l + 1
        if not l % 1000:
            z += 1
            ft.write(row)
    print(l,z)
    f.close()
    ft.close()

def test():
    dt = np.dtype(np.int8)
    a = np.array([257], dtype=dt)
    print(a)
test()