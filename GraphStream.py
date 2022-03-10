import numpy as np
from bidict import bidict

EDGEPATH = './DBLPdata/coll%3.txt'
VERTEXPATH = './DBLPdata/author.txt'


class InfoCell:
    def __init__(self, from_index, to_index, t, weight):
        self.from_index = from_index
        self.to_index = to_index
        self.t = t
        self.weight = weight

    def get_pairs(self):
        return self.from_index, self.to_index

    def get_time(self):
        return self.t

    def get_weight(self):
        return self.weight


class SketchGraph:
    def __init__(self, size, hash_func):
        # 创建一个大小为 w x w的矩阵,指定当前矩阵所用的哈希函数
        # 后续需要考虑如何保证哈希出来的值在[0,size-1]范围中
        try:

            self.matrix = np.shape((size, size))
            self.hash_func = hash_func

        except:
            print('initial matrix error')
        else:
            print('initial sketch success')

    def insert_edge(self, edge: InfoCell):
        # 插入一条边，边为一个元组（from,to;time,val）
        pair = edge.get_pairs()
        x = self.hash_func(pair[0])
        y = self.hash_func(pair[1])
        # TODO 这里有一个问题 如何存储时间,或许可以给每条边编号然后用bidict存，但是这样没有对于时间特性做出处理，后续考虑优化
        val = edge.get_weight()
        self.matrix[x][y] += val

    def delete_edge(self, edge: InfoCell):
        pair = edge.get_pairs()
        x = self.hash_func(pair[0])
        y = self.hash_func(pair[1])
        # TODO 处理时间记录的删除
        val = edge.get_weight()
        self.matrix[x][y] -= val


class TCM:
    def __init__(self, hash_funcs, n, w):
        # n 用于指定使用多少个哈希函数 w为大小
        # TODO 将w集成到哈希函数的属性中
        n = hash_funcs[0:n - 1]
        self.sketches = [None]
        # TODO 这里可以改用多线程加快速度
        k = 0
        for sketch in self.sketches:
            self.sketches[k] = SketchGraph(w, hash_funcs[k])
            k += 1


def HashFuncMod100(a):
    b = a % 100
    return b


def main():
    f = open(EDGEPATH, 'r')
    graph_stream = []
    for e in f:
        e = e.split(';')
        t = e[1]
        v = (e[0].split(',')[0],e[0].split(',')[1])
        cell = InfoCell(v[0], v[1], t, 1)
        graph_stream.append(cell)
    f.close()

    T1 =TCM([HashFuncMod100], 1, 100)

main()
