import numpy as np
from threading import Thread


class InfoCell:
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


class brick:
    # the brick is a tree node
    def __init__(self, dt, i, dep):
        self.parent = None
        self.val = dt(0)
        self.Lflag = 0
        self.Rflag = 0
        self.id = i
        self.dep = dep
    def print1(self):
        print(self.val)


class PyramidSlice:
    # use to manage the bricks in a pyramid slice
    def __init__(self, dt):
        self.bricks = []
        self.dt = dt
        self.dep = -1

    def create_brick(self, dep, index):
        if dep > self.dep:
            print(dep, self.dep)
            print('create new layer', dep)
            self.bricks.append({})
            self.dep = self.dep + 1
            # print(self.dep)
            # print('Finish create new layer', dep)
        b = brick(self.dt, index, dep)
        self.bricks[dep].update({index: b})

        return b

    def carry_over(self, x, dep):
        # 该x为上一层中的x坐标,dep为上一层的深度
        b = self.bricks[dep][int(x / 2)]
        # print("carry_over", dep)
        # 找到需要被执行进位的节点
        t = b.val
        lr = x % 2
        # 确认进位信号来源的方向
        if lr:
            b.Rflag = 1
        else:
            b.Lflag = 1

        t = self.dt(t + 1)

        if t < b.val:

            #此时发生进位
            if b.parent:
                self.carry_over(int(x/2), dep + 1)
            else:
                p = self.create_brick(dep + 1, int(b.id/2))
                p.val = self.dt(1)
                if b.id % 2:
                    p.Lflag = 1
                else:
                    p.Rflag = 1
                b.parent = p
        b.val = self.dt(t)


    def print1(self, dep):
        print(self.bricks[dep])



class PyramidSketch(Thread):
    def __init__(self, sketch_id, hfunc_pair, stream, dt):
        # sketch_id is the index of the sketch.
        # hfunc_pair is the (hfunc,w) tuple
        # stream is the graph stream,a list of Infocell
        # dt means the basic datatype of the matrix,e.g np.uint8
        Thread.__init__(self)
        self.id = sketch_id
        self.hfunc = hfunc_pair[0]
        self.gs = stream
        self.dt = dt
        self.base_layer = np.zeros((hfunc_pair[1], hfunc_pair[1]), dtype=dt)
        print("A Pyramid base has been initialized,No.", self.id)
        self.pyramid_proj = []
        for arr in self.base_layer:
            pyramid_slice = PyramidSlice(self.dt)
            for i in range(int(len(arr) / 2)+1):
                # i = [0,w-1]
                b = pyramid_slice.create_brick(0, i)
                b.Lflag = -1
                b.Rflag = -1
                # -1 means this brick is on the base, it`s position should be calculated by the id
            self.pyramid_proj.append(pyramid_slice)
        print("The first layer of Pyramid Structure has been initialized,No.", self.id)

    def insert_edge(self, cell: InfoCell):
        # insert an edge,which is a entity of Infocell
        edge = cell.get_edge()
        x, y = int(edge[0]), int(edge[1])
        val = self.dt(cell.get_weight())
        # TODO 这个版本不具备处理图流中的权重直接溢出的情况，个人认为实际图流信息中几乎不用浪费算力处理这种事项。。
        # TODO 这个版本先不处理时间了
        # Step 0 :find the hashed position in the Base, e.g M[x][y]
        # Step 1 :let them plu,if outflow, let the outflow part go to the n-layer part
        x = self.hfunc(x)
        y = self.hfunc(y)
        old_val = self.base_layer[x][y]
        res = old_val + val
        if res < old_val:
            # print('Overflow in base')
            self.pyramid_proj[y].carry_over(x, 0)  # 此x为base中的x坐标
        self.base_layer[x][y] = res
        # end

    def run(self):
        print('skecth start')
        self.streaming(self.gs)

    def streaming(self, stream):
        for cell in stream:
            self.insert_edge(cell)

    def print_M(self):
        print('base layer\n', self.base_layer)
        print('The first brick layer')
        for s in self.pyramid_proj:
            for r in s.bricks[0].values():
                print(r.val, type(r.val), end=" ")
            print(' ')
        print('The Second brick layer')
        for s in self.pyramid_proj:
            for r in s.bricks[1].values():
                print(r.val, type(r.val), end=" ")
            print(' ')

