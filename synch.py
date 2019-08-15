import time
import math
import random
from browser import document, html, alert
from browser import timer


class Node:
    def __init__(self, state, dxdt, neighbors):
        # type: (real, (real) -> real, dict<Node, real>) -> None
        self.state = state
        self.neighbors = neighbors
        self.dxdt = dxdt
        self._kicks = []
        
    def add_neighbor(self, n, e):
        self.neighbors[n] = e
        
    def add_kick(self, e):
        # type: (real) -> None
        self._kicks.append(e)
    
    def kick_neighbors(self):
        # type: () => None
        if self.state >= 1:
            for n in self.neighbors:
                n.add_kick(self.neighbors[n])
            self.state = 0
    def update(self, dt):
        # type: () => None
        self.state = self.state + dt*self.dxdt(self.state) + sum(self._kicks)
        self._kicks = []
        self.state = min(1, self.state)
    
class Simulation:
    def __init__(self, dt, n_nodes, s0, lamb, eps):
        self.S0 = s0
        self.lamb = lamb
        self.dt = dt
        self.eps = eps
        dxdt = lambda x: s0 - lamb*x
        self.nodes = [ Node(random.random(), dxdt, {}) for _ in range(n_nodes) ]
        for i, n in enumerate(self.nodes):
            for j, m in enumerate(self.nodes):
                if m != n:
                    n.add_neighbor(m, eps/( (i*j)+1  ) )
        
    def update(self):
        for n in self.nodes:
            n.update(self.dt)
            n.kick_neighbors()
    
class Renderer:
    def __init__(self, sim):
        self.dx = sim.dt
        self.sim = sim
        self.canvas = html.CANVAS(id = 'canv', width = 600, height = 300)
        self.container = html.DIV()
        self.container <= self.canvas
        self.inputs = {}
        self.params = {
            "dt": self.sim.dt,
            "n_nodes": len(sim.nodes),
            "S0": sim.S0,
            "lamb": sim.lamb,
            "kick_eps": sim.eps,
        }
        document <= self.container
        alert("debuggg???")
        self._destroy_frame_interval = 100
        self._ticks = 0
    
    def draw_nodes_line(self):
        n = len(self.sim.nodes)
        radius = self.canvas.width/(2*n)
        
        for i, node in enumerate(self.sim.nodes):
            self.draw_node(node, radius + i*radius*2, self.canvas.height/2, radius)
    
    def draw_nodes_grid(self):
        n = len(self.sim.nodes)
        
        radius = self.canvas.width/(n)
        
        m1 = math.floor(math.sqrt(n))
        
        index = 0
        
        for i in range(m1):
            for j in range(m1):
                if index < n:
                    self.draw_node(self.sim.nodes[index], radius + i*radius*2, radius + j*radius*2, radius)
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
        self.draw_nodes_grid()
        
    def update(self):
        self.draw_canvas()
        self.sim.update()
        self._ticks += 1
    
    def change_params_callback(self, ev):
        self.clear_canvas()
        self.sim = Simulation(
            float(self.inputs['dt'].value), 
            int(self.inputs["n_nodes"].value), 
            float(self.inputs["S0"].value), 
            float(self.inputs["lamb"].value), 
            float(self.inputs["kick_eps"].value),
            )
        self.canvas.width = self.inputs['n_nodes'] * 40
        self.canvas.height = self.canvas.width
        global _timer
        timer.clear_interval(_timer)
        _timer = timer.set_interval(self.update, 20*float(self.inputs['dt'].value))
        
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

s = Simulation(0.01, 10, 2, 1, 0.1)
r = Renderer(s)
r.draw_param_selector()
# r.update()
_timer = timer.set_interval(r.update, 10)