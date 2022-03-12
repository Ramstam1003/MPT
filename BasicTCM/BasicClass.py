from threading import Thread
import numpy as np


def Cutting(x:int, dt:np.dtype, s):
    # x input dt:basic datatype s byte len of dt
    conse = []
    z = dt(1 * pow(2,s) - 1) # 255
    while x != 0:
        t = dt(np.bitwise_and(z,x))
        conse.append(t)
        x = dt(np.right_shift(x, s))
    return conse


class BasicInfoCell:
    def __init__(self, from_index, to_index, weight, time, dt:np.dtype, s):
        x = Cutting(from_index, dt, s)
        y = Cutting(to_index, dt, s)
        self.edge = (x, y)
        self.weight = Cutting(weight, dt, s)
        self.time = Cutting(time, dt, s)

    def get_edge(self):
        return self.edge

    def get_weight(self):
        return self.weight

    def get_time(self):
        return self.time


class GraphSketch(Thread):
    # hash func in the form of a tuple (hfunc,w)
    def __init__(self, sketch_id, hfunc_pair, stream, dt):
        Thread.__init__(self)
        self.id = sketch_id
        self.hfunc = hfunc_pair[0]
        self.w = hfunc_pair[1]
        self.stream = stream
        self.matrix = np.zeros((self.w, self.w), dtype=dt)

    def insert_edge(self, edge: BasicInfoCell):
        # 插入一条边，边为一个元组（from,to;time,val）
        pair = edge.get_edge()
        x = self.hfunc(int(pair[0]))
        y = self.hfunc(int(pair[1]))
        val = edge.get_weight()
        # 权重得保证不会溢出才行
        t = self.matrix[x][y]
        x = np.uint8(t + val)

        if x < t:
            print("Outflow")
        # print(type(t))
        self.matrix[x][y] += val

    def run(self):
        print('skecth start')
        self.process_stream(self.stream)

    def process_stream(self, stream: [BasicInfoCell]):
        for cell in stream:
            self.insert_edge(cell)


    def print_matrix(self):
        print(self.matrix)
        print('max:',self.matrix.max(),'avg:',self.matrix.mean(), 'min:',self.matrix.min(), "sum:",self.matrix.sum())