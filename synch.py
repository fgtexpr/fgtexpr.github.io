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
        if len(self._kicks) == 0:
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
        self.state = min(1, self.state)
    
class Simulation:
    def __init__(self, dt, n_nodes, s0, lamb, eps):
        self.S0 = s0
        self.lamb = lamb
        self.dt = dt
        self.eps = eps
        dxdt = lambda x: s0 - lamb*x
        self.nodes = [ Node(random.random(), dxdt, {}) for _ in range(n_nodes) ]
        for n in self.nodes:
            for m in self.nodes:
                if m != n:
                    n.add_neighbor(m, eps)
        
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
            "canvas_width": self.canvas.width,
        }
        document <= self.container
        alert("debuggg!!??")
        self._destroy_frame_interval = 100
        self._ticks = 0
    
    def draw_nodes(self):
        n = len(self.sim.nodes)
        radius = self.canvas.width/(2*n)
        
        for i, node in enumerate(self.sim.nodes):
            self.draw_node(node, radius + i*radius*2, self.canvas.height/2, radius)
        
    def draw_node(self, node, x, y, r):
        ctx = self.canvas.getContext('2d')
        ctx.beginPath()
        ctx.arc(x, y, r, 0, 6.28)
        ctx.fillStyle = 'rgba(255, 0, 0, {})'.format(node.state)
        ctx.fill()
    
    def clear_canvas(self):
        self.canvas.getContext('2d').clearRect(0, 0, canv.width, canv.height)
        
    def draw_canvas(self):
        if self._ticks % self._destroy_frame_interval:
            canvas.width = canvas.width
        self.clear_canvas()
        self.draw_nodes()
        
    def update(self):
        draw_canvas()
        self.sim.update()
        self._ticks += 1
    
    def change_params_callback(self):
        clear_canvas()
        self.sim = Simulation(self.inputs['dt'], 
            self.inputs["n_nodes"], 
            self.inputs["S0"], 
            self.input["lambda"], 
            self.input["kick_eps"],
            )
        self.canvas.width = self.inputs['n_nodes'] * 30
        
    def draw_param_selector(self):
        # param_name, default_value pairs
        
        for param in params:
            inp = html.INPUT(type = "text", name = param, value = params[param])
            self.inputs[param] = inp
            self.container <= inp
        
        butt = html.BUTTON("update simulation")
        butt.bind("click", self.change_params_callback)

s = Simulation(0.01, 10, 2, 1, 0.1)
r = Renderer(s)
r.draw_param_selector()
timer.set_interval(r.update, 10)