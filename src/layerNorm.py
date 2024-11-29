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
        l_sqrt = c_Sqrt(6, 3, 4)

        l_adderTree0 = c_AdderTree(self.n1, l_adder)
        l_buffer0 = c_Buffer(int(self.embdDim/self.n1), l_register)
        # self.head = c_Node(l_adderTree0, l_buffer0)

        g_block0 = c_Node(c_AdderTree(self.n1, l_adder))
        g_block1 = c_Node(l_buffer0)
        # g_block0.nextNode = g_block1
        g_block2 = c_Node(c_AdderTree(int(self.embdDim)/self.n1, l_adder))
        g_block3 = c_Node(l_divider)
        g_block4 = c_Node(c_SubtractorArray(self.n2, l_subtractor))
        g_block5 = c_Node(c_MultiplierArray(self.n2, l_multiplier))
        g_block6 = c_Node(c_Buffer(self.embdDim, l_register))
        g_block7 = c_Node(c_AdderTree(self.n3, l_adder))
        g_block8 = c_Node(c_Buffer(int(self.embdDim/self.n3), l_register))
        g_block9 = c_Node(c_AdderTree(int(self.embdDim/self.n3), l_adder))
        g_block10 = c_Node(l_divider)
        g_block11 = c_Node(l_sqrt)
        g_block12 = c_Node(c_DividerArray(self.n2, l_divider))
        g_block13 = c_Node(c_MultiplierArray(self.n2, l_multiplier))
        g_block14 = c_Node(c_AdderArray(self.n2, l_adder))
        g_block15 = c_Node(c_Buffer(self.embdDim, l_register))

        self.root = g_block0
        self.generateGraph([g_block0, g_block1, g_block2, g_block3, g_block4, g_block5, g_block6, g_block7, g_block8, 
                            g_block9, g_block10, g_block11, g_block12, g_block13, g_block14, g_block15])

        l_head = self.root
        while l_head != None:
            self.resource.accumulate(l_head.component.getResource())
            self.latency += l_head.component.getLatency()
            l_head = l_head.nextNode

    def generateGraph(self, x_blocks):
        assert self.root == x_blocks[0], "self.root and blocks[0] do not match"
        for i in range(0, len(x_blocks)-2):
            x_blocks[i].nextNode = x_blocks[i+1]

    def getLatency(self):
        return self.latency
    
    def getResource(self):
        return [self.resource.lut, self.resource.dsp]
    

layer0 = c_LayerNorm(768, 32, 2, 2)
layer0.build()
print(layer0.getResource())
print(layer0.getLatency())