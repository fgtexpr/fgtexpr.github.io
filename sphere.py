from patch import Patch
from Vector import Vector
import math
class Sphere(Patch):
    def __init__(self):
        super().__init__()
    
    def call(self, point):
        u = point[0]
        v = point[1]
        x = v
        y = math.cosh(v) * math.sin(u)
        z = math.cosh(v) * math.cos(u)
        return Vector(x, y, z)
