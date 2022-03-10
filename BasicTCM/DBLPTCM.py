import BasicClass as Bc
import HashList
import time


class DBLPInfoCell(Bc.BasicInfoCell):
    def __init__(self, from_index, to_index, t1):
        super(DBLPInfoCell, self).__init__(from_index, to_index, 1, t1)


class DBLP_Core:
    def __init__(self, stream_path, hash_stack):
        # 首先初始化函数堆，然后将图流导入
        self.hash_stack = hash_stack
        self.TCM = []
        f = open(stream_path, 'r')
        self.graph_stream = []  # 调度核心中存储的总图流
        l_stream = 0
        for e in f:
            e = e.split(';')
            t = e[1]
            v = (e[0].split(',')[0], e[0].split(',')[1])
            cell = DBLPInfoCell(v[0], v[1], t)
            self.graph_stream.append(cell)
            l_stream += 1
        f.close()
        print("initialization finish, len of stream:", l_stream, len(self.graph_stream))

    def start(self):
        index = 0
        self.TCM.append(Bc.GraphSketch(sketch_id=index, hfunc_pair=self.hash_stack[index], stream=self.graph_stream))
        for ske in self.TCM:
            ske.start()
            ske.join()
            ske.print_matrix()


DataPath = '/Users/cherudim/Desktop/DBLP/DBLPdata/1424953.txt'

hash_stack = []
hash_stack.append((HashList.Hashfunc1, 809))
T1 = DBLP_Core(DataPath, hash_stack)
t1 = time.time()
T1.start()
t2 = time.time()
t = t2 - t1
print(t)
