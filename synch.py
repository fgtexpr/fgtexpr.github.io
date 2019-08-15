import time
import math
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
        
    
class Simulation:
    def __init__(self, dt):
        s_0 = 2
        l = 1
        self.dt = dt
        dxdt = lambda x: s_0 - l*x
        self.nodes = [Node(0.24, dxdt, {}), Node(0.5, dxdt, {}), Node(0.1, dxdt, {})]
        for n in self.nodes:
            for m in self.nodes:
                if m != n:
                    n.add_neighbor(m, 0.01)
        
    def update(self):
        for n in self.nodes:
            n.update(self.dt)
            n.kick_neighbors()

class Renderer:
    def __init__(self, dx):
        self.dx = dx
        self.sim = Simulation(dx)
        self.canvas = html.CANVAS(id = 'canv', width = 300, height = 300)
        document <= self.canvas
        alert("debuggg!!??!!!!!")
        self._destroy_frame_interval = 20
        self._ticks = 0
    
    def draw_nodes(self):
        n = len(self.sim.nodes)
        radius = self.canvas.width/(2*n)
        
        for i, node in enumerate(self.sim.nodes):
            self.draw_node(self.canvas, node, radius + i*radius*2, 150, radius)
        
    def draw_node(self, canv, node, x, y, r):
        ctx = canv.getContext('2d')
        ctx.beginPath()
        ctx.arc(x, y, r, 0, 6.28)
        ctx.fillStyle = 'rgba(255, 0, 0, {})'.format(node.state)
        ctx.fill()
    
    def clear(self, canv):
        canv.getContext('2d').clearRect(0, 0, canv.width, canv.height)
    
    def update(self):
        if self._ticks % self._destroy_frame_interval:
            del document['canv']
            self.canvas = html.CANVAS(id = 'canv', width = 300, height = 300)
            document <= self.canvas
        self.canvas = document['canv']
        self.sim.update()
        self.clear(self.canvas)
        self.draw_nodes()
        self._ticks += 1
        

r = Renderer(0.01)

timer.set_interval(r.update, 20)