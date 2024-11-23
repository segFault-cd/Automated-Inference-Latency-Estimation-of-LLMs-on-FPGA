import math
from components import *

class c_LayerNorm(c_Component):
    def __init__(self, x_embdDim, x_n1, x_n2, x_n3):
        assert (x_embdDim % x_n1 == 0), "x_n1 is not a divisor of x_embdDim"
        super(c_LayerNorm, self).__init__()
        self.embdDim = x_embdDim
        self.n1 = x_n1
        self.n2 = x_n2
        self.n3 = x_n3
        self.root = None
        self.resource = c_Resource()

    def build(self):
        l_adder = c_Adder(4, 0, 2)
        l_register = c_Register(1, 0)
        l_subtractor = c_Subtractor(4, 0, 2)
        l_divider = c_Divider(2, 4, 4)
        l_multiplier = c_Multiplier(2, 2, 3)

        l_adderTree0 = c_AdderTree(self.n1, l_adder)
        l_buffer0 = c_Buffer(int(self.embdDim/self.n1), l_register)
        # self.head = c_Node(l_adderTree0, l_buffer0)

        g_block0 = c_Node(l_adderTree0)
        g_block1 = c_Node(l_buffer0)
        g_block0.nextNode = g_block1

        self.root = g_block0

        l_head = self.root
        while l_head != None:
            self.resource.accumulate(l_head.component.getResource())
            self.latency += l_head.component.getLatency()
            l_head = l_head.nextNode

    def getLatency(self):
        return self.latency
    
    def getResource(self):
        return [self.resource.lut, self.resource.dsp]
    

layer0 = c_LayerNorm(768, 32, 2, 2)
layer0.build()
print(layer0.getResource())
print(layer0.getLatency())