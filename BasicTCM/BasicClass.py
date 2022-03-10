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


class HashFunction:
    def __init__(self, w, hash_func):
        self.hfunc = hash_func
        self.w = w
        self.index = 0

    def set_index(self, index):
        self.index = index

    def get_w(self):
        return self.w

    def run(self, x):
        return self.hfunc(x)


class HashPool:
    def __init__(self):
        self.count = 0
        self.lock = False
        self.pool = []

    def add_func(self, hfunc: HashFunction):
        self.pool.append(hfunc)
        hfunc.set_index(self.count)
        self.count += 1

    def show_len(self):
        return self.count

    def search_hfunc(self, index):
        return self.pool[index]


class GraphSketch(Thread):
    # 这里计划在总系统中外置哈希函数pool，每个实际运行的线程去一个个取，好过细化到每个线程中的管理
    def __init__(self, sketch_id, hash_index, hash_pool: HashPool):
        Thread.__init__(self)
        self.id = sketch_id
        self.hfunc = hash_pool.search_hfunc(hash_index)
        self.w = self.hfunc.get_w()
        self.matrix = np.zeros((self.w, self.w))

    def insert_edge(self, edge: BasicInfoCell):
        # 插入一条边，边为一个元组（from,to;time,val）
        pair = edge.get_edge()
        x = self.hfunc.run(int(pair[0]))
        y = self.hfunc.run(int(pair[1]))
        # TODO 这里有一个问题 如何存储时间,或许可以给每条边编号然后用bidict存，但是这样没有对于时间特性做出处理，后续考虑优化
        val = edge.get_weight()
        self.matrix[x][y] += val

    def run(self):
        self.matrix = np.zeros((self.w, self.w), dtype =np.uint8)

    def process_stream(self, stream: [BasicInfoCell]):
        for cell in stream:
            self.insert_edge(cell)

    def print_matrix(self):
        print(self.matrix)
        print('max:',self.matrix.max(),'avg:',self.matrix.mean(), 'min:',self.matrix.min())