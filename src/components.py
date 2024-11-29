import math


"""Base Classes"""

class c_Component():
    def __init__(self):
        self.resource = 0
        self.latency = 0
        self.clkFreq = 100_000_000
    
    def __str__(self):
        return "Base Class for all components"


class c_Resource():
    def __init__(self, x_lut=0, x_dsp=0):
        self.lut = x_lut
        self.dsp = x_dsp

    def accumulate(self, x_resource):
        self.lut += x_resource[0]
        self.dsp += x_resource[1]

    def getResource(self):
        return [self.lut, self.dsp]
    
    def __str__(self):
        return "Resource = LUT + DSP + ..."


"""Level0 Classes"""

class c_Adder(c_Component):
    def __init__(self, x_lut, x_dsp, x_latency=0):
        super(c_Adder, self).__init__()
        self.resource = c_Resource(x_lut, x_dsp)
        self.latency = x_latency

    def getResource(self):
        return [self.resource.lut, self.resource.dsp]
    
    def getLatency(self):
        return self.latency
    
    def __str__(self):
        return "Level0: Adder"
    

class c_Multiplier(c_Component):
    def __init__(self, x_lut, x_dsp, x_latency=0):
        super(c_Multiplier, self).__init__()
        self.resource = c_Resource(x_lut, x_dsp)
        self.latency = x_latency

    def getResource(self):
        return [self.resource.lut, self.resource.dsp]
    
    def getLatency(self):
        return self.latency
    
    def __str__(self):
        return "Level0: Multiplier"
    

class c_Divider(c_Component):
    def __init__(self, x_lut, x_dsp, x_latency=0):
        super(c_Divider, self).__init__()
        self.resource = c_Resource(x_lut, x_dsp)
        self.latency = x_latency

    def getResource(self):
        return [self.resource.lut, self.resource.dsp]
    
    def getLatency(self):
        return self.latency
    
    def __str__(self):
        return "Level0: Divider"
    
class c_Subtractor(c_Component):
    def __init__(self, x_lut, x_dsp, x_latency=0):
        super(c_Subtractor, self).__init__()
        self.resource = c_Resource(x_lut, x_dsp)
        self.latency = x_latency

    def getResource(self):
        return [self.resource.lut, self.resource.dsp]
    
    def getLatency(self):
        return self.latency
    
    def __str__(self):
        return "Level0: Subtractor"
    
class c_Register(c_Component):
    def __init__(self, x_lut, x_dsp):
        super(c_Register, self).__init__()
        self.resource = c_Resource(x_lut, x_dsp)
        self.latency = 1

    def getResource(self):
        return [self.resource.lut, self.resource.dsp]
    
    def getLatency(self):
        return self.latency
    
    def __str__(self):
        return "Level0: Register"
    
class c_Sqrt(c_Component):
    def __init__(self, x_lut, x_dsp, x_latency=0):
        super(c_Sqrt, self).__init__()
        self.resource = c_Resource(x_lut, x_dsp)
        self.latency = x_latency

    def getResource(self):
        return [self.resource.lut, self.resource.dsp]
    
    def getLatency(self):
        return self.latency
    
    def __str__(self):
        return "Level0: Sqrt"
    

"""Level1 Classes"""

class c_AdderTree(c_Component):
    def __init__(self, x_height, x_adder):
        assert (x_height).is_integer(), "The height of the tree is not an integer"
        super(c_AdderTree, self).__init__()
        self.height = x_height
        l_numAdders, self.depth = self.getNumAdders(self.height)
        self.resource = c_Resource(l_numAdders * x_adder.getResource()[0], l_numAdders * x_adder.getResource()[1])

        self.latency = self.depth * x_adder.getLatency()

    def getNumAdders(self, x_height):
        l_height = x_height
        l_numAdders = 0
        l_depth = 0
        while l_height > 1:
            l_numAdders += int(l_height/2)
            l_height = math.ceil(l_height/2)
            l_depth += 1

        return l_numAdders, l_depth

    def getResource(self):
        return [self.resource.lut, self.resource.dsp]
    
    def getLatency(self):
        return self.latency
    
    def getHeight(self):
        return self.height
    
    def __str__(self):
        return "Level1: AdderTree"
    

class c_Buffer(c_Component):
    def __init__(self, x_width, x_register):
        super(c_Buffer, self).__init__()
        self.width = x_width
        self.resource = c_Resource(self.width * x_register.getResource()[0], self.width * x_register.getResource()[1])
        self.latency = x_register.getLatency()

    def getResource(self):
        return [self.resource.lut, self.resource.dsp]
    
    def getLatency(self):
        return self.latency
    
    def getWidth(self):
        return self.width
    
    def __str__(self):
        return "Level1: Buffer"
    
class c_AdderArray(c_Component):
    def __init__(self, x_width, x_adder):
        super(c_AdderArray, self).__init__()
        self.width = x_width
        self.resource = c_Resource(self.width * x_adder.getResource()[0], self.width * x_adder.getResource()[1])
        self.latency = x_adder.getLatency()

    def getResource(self):
        return [self.resource.lut, self.resource.dsp]
    
    def getLatency(self):
        return self.latency
    
    def getWidth(self):
        return self.width
    
    def __str__(self):
        return "Level1: AdderArray"
    
class c_MultiplierArray(c_Component):
    def __init__(self, x_width, x_multiplier):
        super(c_MultiplierArray, self).__init__()
        self.width = x_width
        self.resource = c_Resource(self.width * x_multiplier.getResource()[0], self.width * x_multiplier.getResource()[1])
        self.latency = x_multiplier.getLatency()

    def getResource(self):
        return [self.resource.lut, self.resource.dsp]
    
    def getLatency(self):
        return self.latency
    
    def getWidth(self):
        return self.width
    
    def __str__(self):
        return "Level1: MultiplierArray"
    
class c_DividerArray(c_Component):
    def __init__(self, x_width, x_divider):
        super(c_DividerArray, self).__init__()
        self.width = x_width
        self.resource = c_Resource(self.width * x_divider.getResource()[0], self.width * x_divider.getResource()[1])
        self.latency = x_divider.getLatency()

    def getResource(self):
        return [self.resource.lut, self.resource.dsp]
    
    def getLatency(self):
        return self.latency
    
    def getWidth(self):
        return self.width
    
    def __str__(self):
        return "Level1: DividerArray"
    
class c_SubtractorArray(c_Component):
    def __init__(self, x_width, x_adder):
        super(c_SubtractorArray, self).__init__()
        self.width = x_width
        self.resource = c_Resource(self.width * x_adder.getResource()[0], self.width * x_adder.getResource()[1])
        self.latency = x_adder.getLatency()

    def getResource(self):
        return [self.resource.lut, self.resource.dsp]
    
    def getLatency(self):
        return self.latency
    
    def getWidth(self):
        return self.width
    
    def __str__(self):
        return "Level1: SubtractorArray"
    
"""Level2 Classes"""

class c_MAC(c_Component):
    def __init__(self, x_height, x_multiplier, x_adder):
        assert (x_height).is_integer(), "The height of the tree is not an integer"
        super(c_MAC, self).__init__()
        l_adderTree = c_AdderTree(x_height, x_adder)
        l_multResource = [x_height * x_multiplier.getResource[0], x_height * x_multiplier.getResource[1]]

        self.resource = c_Resource(l_multResource[0] + l_adderTree.getResource()[0], l_multResource[1] + l_adderTree.getResource()[1])
        self.latency = x_multiplier.getLatency() + l_adderTree.getLatency()

    def getResource(self):
        return [self.resource.lut, self.resource.dsp]
    
    def getLatency(self):
        return self.latency
    
    def __str__(self):
        return "Level2: MAC"
    
class c_AdderTreeArray(c_Component):
    def __init__(self, x_height, x_width, x_adder):
        assert math.log2(x_height).is_integer(), "The height of the tree is not a power of 2"
        super(c_AdderTreeArray, self).__init__()
        self.height = x_height
        self.width = x_width

        l_adderTree = c_AdderTree(self.height, x_adder)
        self.resource = c_Resource(self.width * l_adderTree.getResource([0]), self.width * l_adderTree.getResource()[1])
        self.latency = l_adderTree.getLatency()

    def getResource(self):
        return [self.resource.lut, self.resource.dsp]
    
    def getLatency(self):
        return self.latency
    
    def getWidth(self):
        return self.width
    
    def getHeight(self):
        return self.height
    
    def __str__(self):
        return "Level2: AdderTreeArray"
    
"""Level3 Classes"""

class c_MACArray(c_Component):
    def __init__(self, x_height, x_width, x_multiplier, x_adder):
        assert math.log2(x_height).is_integer(), "The height of the tree is not a power of 2"
        super(c_MACArray, self).__init__()
        self.height = x_height
        self.width = x_width

        l_MAC = c_MAC(self.height, x_multiplier, x_adder)
        self.resource = c_Resource(self.width * l_MAC.getResource()[0], self.width * l_MAC.getResource()[1])
        self.latency = l_MAC.getLatency()
    
    def getResource(self):
        return [self.resource.lut, self.resource.dsp]
    
    def getLatency(self):
        return self.latency
    
    def getWidth(self):
        return self.width
    
    def getHeight(self):
        return self.height
    
    def __str__(self):
        return "Level3: MAC_ARRAY"
    

"""Miscellaneous classes"""

class c_Node():
    def __init__(self, x_component, x_nextNode=None):
        self.component = x_component
        self.nextNode = x_nextNode

    def getResource(self):
        return self.component.getResource()
    
    # The getLatency function is to be modified. Latency equations go here
    def getLatency(self):
        return self.component.getLatency()
    
    def __str__(self):
        return f'Component: {self.component.__str__()}, Next Node: {self.nextComponent.__str__()}'