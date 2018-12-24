from patch import Patch
from Vector import Vector
import math
class Sphere(Patch):
    def __init__(self):
        super().__init__()
    
    def call(self, point):
        theta = point[0]
        phi = point[1]
        x = math.cos(theta) * math.sin(phi)
        y = math.sin(phi) * math.sin(theta)
        z = math.cos(phi)
        return Vector(x, y, z)
