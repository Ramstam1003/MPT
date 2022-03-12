# 测试一下
import Tools
import DataStructure
import numpy as np
import time


# Super Parameter：dt，w
class Attribute_Core:
    def __init__(self, stream_path, dt, w, n=1):
        # initialize the hash functions and them import the graph stream
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
        for ske in self.TCM:
            ske.join()

    def print_all(self):
        for ske in self.TCM:
            ske.print_M()


class OperatingSystem:
    def __init__(self):
        self.op = -1
        print("choose super_para:")
        stream_path, dt, w, n = self.initial_choose()
        self.core = Attribute_Core(stream_path, dt, w, n)
        op_dic = {
            "end": self.shut_system,
            "start": self.core.generating_sketch,
            "print":self.core.print_all
        }
        while self.op != "end":
            self.op = input("input the operation code\n")
            op_dic[self.op]()

    def shut_system(self):
        print("System Closed")
        self.op = "end"
        return 0

    def initial_choose(self):
        path_dic = {
            "1": '/Users/cherudim/Desktop/DBLP/DBLPdata/1424953.txt'
        }
        dt_dic = {
            "1": np.uint8
        }
        w_dic = {
            "1": 70
        }
        state = 1
        while state:
            try:
                stream_path = path_dic[input(path_dic)]
                break
            except:
                continue
        while state:
            try:
                dt = dt_dic[input(dt_dic)]
                break
            except:
                continue
        while state:
            try:
                w = w_dic[input(w_dic)]
                break
            except:
                continue
        while state:
            try:
                n = int(input("number of pyramid"))
                break
            except:
                continue
        return stream_path, dt, w, n


op = OperatingSystem()

# switch = {"valueA":functionA,"valueB":functionB,"valueC":functionC}
# try:
# 　　switch["value"]() #执行相应的方法。
# except KeyError as e:
#       pass 或 functionX #执行default部分
