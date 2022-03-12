# 测试一下
import Tools
import DataStructure
import numpy as np
import time


# Super Parameter：dt，w
class Attribute_Core:
    def __init__(self, stream_path, dt, w, n=1):
        # 首先初始化函数堆，然后将图流导入
        print('initialing...')
        self.hash_stack = []
        for i in range(n):
            self.hash_stack.append(Tools.GenerateIPHash(w))
        print('get hash functions')
        self.TCM = []
        self.dt = dt
        self.graph_stream, l_stream = Tools.DBLPDataProcessor(stream_path)
        self.sketch_counter = n
        print("Process Core initialization finish, len of stream:", l_stream)

    def generating_sketch(self):
        print("start generating sketches")
        for i in range(self.sketch_counter):
            self.TCM.append(DataStructure.PyramidSketch(i, self.hash_stack[i], self.graph_stream, self.dt))
        for ske in self.TCM:
            ske.start()
            ske.join()
            ske.print_M()


DataPath = '/Users/cherudim/Desktop/DBLP/DBLPdata/1424953.txt'

Core = Attribute_Core(DataPath, np.uint8, 70)
Core.generating_sketch()
