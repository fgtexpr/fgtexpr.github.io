from browser import document, alert
from browser import html

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

def draw_node(canv, node, x, y, r):
    ctx = canv.getContext('2d')
    ctx.arc(x, y, r, 0, 6.28, True)
    ctx.fillStyle = 'rgba(0, 0, 0, {})'.format(node.state)
    ctx.fill()

def clear(canv):
    canv.getContext('2d').clearRect(0, 0, canv.width, canv.height)

def render():
    s = Simulation(0.01)
    canvas = html.CANVAS(width = 300, height = 300)
    document <= canvas
    for _ in range(100):
        s.update()
        clear(canvas)
        draw_node(canvas, s.nodes[0], 150, 150, 50)
        

render()