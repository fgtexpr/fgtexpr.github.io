import time
import math
import random
from browser import document, html, alert
from browser import timer

class Node:
    def __init__(self, state, dxdt, neighbors):
        # type: (float, (float) -> real, dict<Node, (float) -> float>) -> None
        self.state = state
        self.neighbors = neighbors
        self.dxdt = dxdt
        self._kicks = []
        self._time = 0
        
    def add_neighbor(self, n, weight_fcn):
        # type: (Node, (float) -> float) -> None
        self.neighbors[n] = weight_fcn
    
    def add_kick(self, e):
        # type: (float) -> None
        self._kicks.append(e)
    
    def kick_neighbors(self):
        # type: () => None
        if self.state >= 1:
            for n in self.neighbors:
                n.add_kick(self.neighbors[n](self._time))
            self.state = 0
    
    def step(self, dt):
        # type: () => None
        self.state = self.state + dt*self.dxdt(self.state) + sum(self._kicks)
        self._kicks = []
        self.state = min(1, self.state)
        self._time += 1

class DynamicNetwork:
    def __init__(self, dt):
        self._time = 0
        self.dt = dt
        assert 'nodes' in self.__dict__
    
    def step(self):
        for n in self.nodes:
            n.step(self.dt)
            n.kick_neighbors()

class FixedLattice(DynamicNetwork):
    def __init__(self, dxdt, dt, n_nodes):
        self.nodes = [ Node(random.random(), dxdt, {}) for _ in range(n_nodes) ]
        for i, n in enumerate(self.nodes):
            m = math.ceil( math.sqrt(n_nodes) )
            n.position = (0.5/m + (i % m) / m, 0.5/m + math.floor(i/m) / m)
        
        for i, n in enumerate(self.nodes):
            for j, m in enumerate(self.nodes):
                dist = abs(n.position[0] - m.position[0]) + abs(n.position[1] - m.position[1])
                if m != n and dist <= 2:
                    kick_fnc = lambda x: 0.3/(dist + 1)
                    n.add_neighbor(m, kick_fnc)
        
        super(FixedLattice, self).__init__(dt)

class Renderer:
    def __init__(self, network):
        self.dx = network.dt
        self.net = network
        self.canvas = html.CANVAS(id = 'canv', width = 600, height = 600)
        self.container = html.DIV()
        self.container <= self.canvas
        self.inputs = {}
        self.params = {
            "dt": self.net.dt,
            "dxdt": "2 - x",
            "n_nodes": len(self.net.nodes),
            "network": "fixedlattice"
        }
        document <= self.container
        self._destroy_frame_interval = 100
        self._ticks = 0
    
    def draw_nodes(self):
        if 'position' not in self.net.nodes[0].__dict__:
            self.draw_nodes_grid()
            return
        for n in self.net.nodes:
            radius = self.canvas.width/(2*math.ceil(math.sqrt(len(self.net.nodes))))
            self.draw_node(n, n.position[0] * self.canvas.width, n.position[1] * self.canvas.height, radius)
        
    def draw_nodes_grid(self):
        n = len(self.net.nodes)
        
        m1 = math.ceil(math.sqrt(n))
        radius = self.canvas.width/(2*m1)
        
        index = 0
        
        for i in range(m1):
            for j in range(m1):
                if index < n:
                    self.draw_node(self.net.nodes[index], radius + i*radius*2, radius + j*radius*2, radius)
                index = index + 1
                
                
    def draw_node(self, node, x, y, r):
        ctx = self.canvas.getContext('2d')
        ctx.beginPath()
        ctx.arc(x, y, r, 0, 6.28)
        r = 255 - (255*node.state)
        b = 255*node.state
        ctx.fillStyle = 'rgb({}, 0, {})'.format(r, b)
        ctx.fill()
    
    def clear_canvas(self):
        self.canvas.getContext('2d').clearRect(0, 0, self.canvas.width, self.canvas.height)
        
    def draw_canvas(self):
        if self._ticks % self._destroy_frame_interval:
            self.canvas.width = self.canvas.width
            self.canvas.height = self.canvas.height
        self.clear_canvas()
        self.draw_nodes()
        
    def update(self):
        self.draw_canvas()
        self.net.step()
        self._ticks += 1
    
    def change_params_callback(self, ev):
        self.clear_canvas()
        exec_string = str(self.inputs['dxdt'].value)
        def dxdt(x):
            return eval(exec_string)
        self.net = FixedLattice(
            dxdt,
            float(self.inputs['dt'].value),
            int(self.inputs['n_nodes'].value)
        )
        self.canvas.width = 900
        self.canvas.height = 900
        global _timer
        timer.clear_interval(_timer)
        _timer = timer.set_interval(self.update, 10*float(self.inputs['dt'].value))
        
    def draw_param_selector(self):
        # param_name, default_value pairs
        
        for param in self.params:
            inp = html.INPUT(type = "text", name = param, value = self.params[param])
            self.inputs[param] = inp
            self.container <= html.BR()
            self.container <= param
            self.container <= html.BR()
            self.container <= inp
            self.container <= html.BR()
        
        butt = html.BUTTON("update simulation")
        butt.bind("click", self.change_params_callback)
        self.container <= butt

alert("SjgvjvjCSV")
alert(foo(2))
n = FixedLattice(lambda x : 2 - x, 0.01, 9)
r = Renderer(n)
r.draw_param_selector()
r.update()
_timer = timer.set_interval(r.update, 10)