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

def Cutting(x:int, dt:np.dtype, s):
    conse = []
    flag = 1
    z = dt(1 * pow(2,s) - 1) # 255

    while x != 0:
        t = dt(np.bitwise_and(z,x))
        conse.append(t)
        x = np.right_shift(x, s)
    return conse


def shutdown(a):
    print("shutdown",a)

def start(a):
    print("start",a)
# switch = {"valueA":functionA,"valueB":functionB,"valueC":functionC}
# try:
#　　switch["value"]() #执行相应的方法。
# except KeyError as e:
#       pass 或 functionX #执行default部分

op_dic = {
    "end" : shutdown,
    "start":start
}

op = input()
op_dic[op](10)