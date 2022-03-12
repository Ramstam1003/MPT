import numpy as np
from threading import Thread


class InfoCell:
    # InfoCell is the basic structure of a flow in GraphStream
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
    # the brick is a tree node,an array of bricks is a layer,several layers come to be a Slice and a pyramid is
    # consists of layers,pyramid projects in the y-axis is several slices.
    def __init__(self, dt, i, dep):
        self.parent = None
        self.val = dt(0)
        self.Lflag = 0
        self.Rflag = 0
        self.id = i
        self.dep = dep


class PyramidSlice:
    # use to manage the bricks in a pyramid slice
    def __init__(self, dt):
        # dt means the basic datatype of the whole Slice,bricks is a list consisted of several dict,they are used to
        # map bricks with their index,each dict means a layer of the pyramid-slice.
        self.bricks = []
        self.dt = dt
        self.height = -1
        # height = 0 means it is the first layer upper the basic layer

    def create_brick(self, dep, index):
        # Step 0:if the Slice now have the enough height,initialize a new brick and add it to the right height-dict with
        # it`s index.
        # Step 1:if the Slice now don`t have enough height,add a new dict and the height,then go Step 0.
        # return the pointer to the new brick.
        if dep > self.height:
            self.bricks.append({})
            self.height = self.height + 1
        b = brick(self.dt, index, dep)
        self.bricks[dep].update({index: b})
        return b

    def carry_over(self, x, dep):
        # the x is the position index of pre-layer,the dep is also the pre-layer`s depth
        # this function use to encounter the situation that some layer happens Overflow.
        # Step 0:Find the mapped brick in the next layer,calculate the plus and turn the flag situation by the odd/even
        # of the x position of the pre-bricks.
        # Step 1:If the plus process happens a overflow as well,if the brick has already have a parent,then carry_over
        # to its parent.Or initialize a new brick as its parent and add the link between them,the another Child of the
        # new bricks should be linked as well.
        b = self.bricks[dep][int(x / 2)]
        t = b.val
        lr = x % 2
        if lr:
            b.Rflag = 1
        else:
            b.Lflag = 1
        t = self.dt(t + 1)
        if t < b.val:
            if b.parent:
                self.carry_over(int(x / 2), dep + 1)
            else:
                p = self.create_brick(dep + 1, int(b.id / 2))
                p.val = self.dt(1)
                if b.id % 2:
                    p.Rflag = 1
                    if self.bricks[dep][int(x / 2)-1]:
                        self.bricks[dep][int(x / 2) - 1].parent = p
                else:
                    p.Lflag = 1
                    if self.bricks[dep][int(x/2)+1]:
                        self.bricks[dep][int(x / 2) + 1].parent = p
                b.parent = p
        b.val = t


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
        # At first we initialize the base-layer and the first-layer.
        self.pyramid_proj = []
        for arr in self.base_layer:
            pyramid_slice = PyramidSlice(self.dt)
            for i in range(int(len(arr) / 2) + 1):
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
        # TODO we recommend to process the weight to non-overflow state in the dataset rather than doing it in the
        #  system,in the actual situation it almost never happens
        # TODO Thinking about using a time manage module to map time and edge
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

    def delete_edge(self, delete_cell: InfoCell):
        # TODO how to delete a edge
        return 0

    def query(self):
        # TODO how to make a query of an vertex or an edge
        return 0

    def run(self):
        # Inheritance from threading.Thread
        print('sketch start processing')
        self.streaming(self.gs)

    def streaming(self, stream):
        # to process the graph stream from the dataset
        for cell in stream:
            self.insert_edge(cell)

    def print_M(self):
        # Use to print the matrix form data of the pyramid
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