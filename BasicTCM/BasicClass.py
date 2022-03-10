from threading import Thread
import numpy as np


class BasicInfoCell:
    def __init__(self, from_index, to_index, weight, time):
        self.edge = (from_index, to_index)
        self.weight = weight
        self.time = time

    def get_edge(self):
        return self.edge

    def get_weight(self):
        return self.weight

    def get_time(self):
        return self.time


class GraphSketch(Thread):
    # 每个摘要图的初始化只需要分到哈希函数即可，这个哈希函数从此和这个摘要图绑定，避免后续出现重复的摘要图,哈希函数以tuple(hfunc,w)传入
    def __init__(self, sketch_id, hfunc_pair, stream):
        Thread.__init__(self)
        self.id = sketch_id
        self.hfunc = hfunc_pair[0]
        self.w = hfunc_pair[1]
        self.stream = stream
        self.matrix = np.zeros((self.w, self.w), dtype=np.uint8)
        print(self.matrix.dtype)

    def insert_edge(self, edge: BasicInfoCell):
        # 插入一条边，边为一个元组（from,to;time,val）
        pair = edge.get_edge()
        x = self.hfunc(int(pair[0]))
        y = self.hfunc(int(pair[1]))
        # TODO 这里有一个问题 如何存储时间,或许可以给每条边编号然后用bidict存，但是这样没有对于时间特性做出处理，后续考虑优化
        val = edge.get_weight()
        # 权重得保证不会溢出才行
        # TODO 这里不能用简单的＋，需要判断是否有溢出，用一个带有异常接受机制的plus函数来代替加法
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