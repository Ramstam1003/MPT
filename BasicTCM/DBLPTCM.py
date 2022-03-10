import BasicClass as Bc
import HashList
import time

class DBLPInfoCell(Bc.BasicInfoCell):
    def __init__(self, from_index, to_index, time):
        super(DBLPInfoCell, self).__init__(from_index, to_index, 1, time)


class DBLP_Core:
    def __init__(self, stream_path):
        # 首先初始化函数池，然后将图流导入
        self.hash_pool = Bc.HashPool()
        self.hash_pool.add_func(Bc.HashFunction(809, HashList.Mod809))
        self.TCM = []
        f = open(stream_path, 'r')
        self.graph_stream = []  # 调度核心中存储的总图流
        for e in f:
            e = e.split(';')
            t = e[1]
            v = (e[0].split(',')[0], e[0].split(',')[1])
            cell = DBLPInfoCell(v[0], v[1], t)
            self.graph_stream.append(cell)
        f.close()

    def start(self):
        self.TCM.append(Bc.GraphSketch(1, 0, self.hash_pool))
        for ske in self.TCM:
            ske.process_stream(self.graph_stream)
            ske.print_matrix()

T1 = DBLP_Core('../DBLPdata/collaboration.txt')
t1 = time.time()
T1.start()
t2 = time.time()
t = t2-t1
print(t)