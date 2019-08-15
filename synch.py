from browser import document, alert

class Node(object):
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
        state = self.state + dt*self.dxdt(self.state) + sum(kicks)
        self.state = min(1, state)
        self._kicks = []
        self.state = min(1, self.f(self.state))
        self.f = self._next_f
    
class Simulation(object):
    def __init__(self, dt):
        s_0 = 2
        l = 1
        self.dt = dt
        dxdt = lambda x: s_0 - l*x
        self.nodes = [Node(0.4, dxdt, {})]
        
    def update(self):
        for n in self.nodes:
            n.update(self.dt)

def render():
    s = Simulation(0.1)
    for _ in range(10):
        s.update()
        alert(s.nodes[0].state)

render()