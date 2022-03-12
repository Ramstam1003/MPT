# 测试一下
import Tools
import DataStructure
import numpy as np
import time

class Attribute_Core:
    def __init__(self, stream_path, hash_stack, dt):
        # 首先初始化函数堆，然后将图流导入
        self.hash_stack = hash_stack
        self.TCM = []
        self.dt = dt
        f = open(stream_path, 'r')
        self.graph_stream = []  # 调度核心中存储的总图流
        l_stream = 0
        for e in f:
            e = e.split(';')
            t = e[1]
            v = (e[0].split(',')[0], e[0].split(',')[1])
            cell = DataStructure.InfoCell(v[0], v[1], 1,t)
            self.graph_stream.append(cell)
            l_stream += 1
        f.close()
        print("initialization finish, len of stream:", len(self.graph_stream))

    def start(self):
        index = 0
        self.TCM.append(DataStructure.PyramidSketch(1, self.hash_stack[0], self.graph_stream, self.dt))
        for ske in self.TCM:
            ske.run()
            ske.print_M()



DataPath = '/Users/cherudim/Desktop/DBLP/DBLPdata/1424953.txt'

hash_stack1 = []
hash_stack1.append(Tools.GenerateIPHash(5))
T1 = Attribute_Core(DataPath, hash_stack1, np.uint8)
t1 = time.time()
T1.start()
t2 = time.time()
t = t2 - t1
print(t)
