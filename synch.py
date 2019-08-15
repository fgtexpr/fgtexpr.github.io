import time
from browser import document, html, alert
from browser import timer


class Node:
    def __init__(self, state, dxdt, neighbors):
        # type: (real, (real) -> real, dict<Node, real>) -> None
        self.state = state
        self.neighbors = neighbors
        self.dxdt = dxdt
        self._kicks = []
    
    def add_kick(self, e):
        # type: (real) -> None
        self._kicks.append(e)
    
    def kick_neighbors(self):
        # type: () => None
        if self.state >= 1:
            for n in neighbors:
                n.add_kick(neighbors[n])
    
    def update(self, dt):
        # type: () => None
        state = self.state + dt*self.dxdt(self.state) + sum(self._kicks)
        self.state = min(1, state)
        self._kicks = []
        if self.state >= 1:
            self.state = 0
    
class Simulation:
    def __init__(self, dt):
        s_0 = 2
        l = 1
        self.dt = dt
        dxdt = lambda x: s_0 - l*x
        self.nodes = [Node(0.4, dxdt, {})]
        
    def update(self):
        for n in self.nodes:
            n.update(self.dt)

class Renderer:
    def __init__(self, dx):
        self.dx = dx
        self.sim = Simulation(dx)
        self.canvas = html.CANVAS(id = 'canv', width = 300, height = 300)
        document <= self.canvas
        self.draw_node(self.canvas, self.sim.nodes[0], 150, 150, 50)
        alert("F")

    def draw_node(self, canv, node, x, y, r):
        ctx = canv.getContext('2d')
        ctx.arc(x, y, r, 0, 6.28, True)
        ctx.fillStyle = 'rgba(255, 0, 0, {})'.format(node.state)
        ctx.fill()
    
    def clear(self, canv):
        canv.getContext('2d').clearRect(0, 0, canv.width, canv.height)
    
    def update(self):
        self.canvas = document['canv']
        self.sim.update()
        self.clear(self.canvas)
        self.draw_node(self.canvas, self.sim.nodes[0], 150, 150, 50)
        

r = Renderer(0.05)

#timer.set_interval(r.update, 50)