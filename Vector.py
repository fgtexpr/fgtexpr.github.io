import math
from operator import add, sub, mul

class Vector(object):
    def __init__(self, *args):
        if len(args)==0: 
            self.values = (0,0)
        else: 
            self.values = args
        
    def mag(self):
        """ Returns Euclidean norm of the vector """
        return math.sqrt( sum( map(lambda x: x*x, self.values) ) )

    def normalized(self):
        """ Returns a normalized unit vector """
        magnitude = self.mag()
        if magnitude == 0:
            return Vector(*self.values)
        normed = map(lambda x: x / magnitude, self.values)
        return Vector(*normed)
        
    def dot(self, other):
        """ Returns the dot product of self and other vector
        """
        return sum(map(mul, self.values, other.values))

    def scalar_multiply(self, scalar):
        scaled = map(lambda x: x*scalar, self.values)
        return Vector(*scaled)
        
    def cross(self, other):
        x = self.values[1]*other.values[2] - self.values[2]*other.values[1]
        y = self.values[0]*other.values[2] - self.values[2]*other.values[0]
        z = self.values[0]*other.values[1] - self.values[1]*other.values[0]
        return Vector(x, y, z)
        
    def __mul__(self, other):
        """ Returns the dot product of self and other if multiplied
            by another Vector.  If multiplied by an int or float,
            multiplies each component by other.
        """
        if type(other) == type(self):
            return self.dot(other)
        elif type(other) == type(1) or type(other) == type(1.0):
            return self.scalar_multiply(other)
        return ValueError
    
    def __rmul__(self, other):
        return self.__mul__(other)

    def __add__(self, other):
        """ Returns the vector addition of self and other """
        added = map(add, self.values, other.values)
        return Vector(*added)
    
    def __sub__(self, other):
        """ Returns the vector difference of self and other """
        subbed = map(sub, self.values, other.values)
        return Vector(*subbed)
    
    def __mod__(self, other):
        '''Returns self cross other'''
        return self.cross(other)

    def __iter__(self):
        return self.values.__iter__()
    
    def __len__(self):
        return len(self.values)
    
    def __getitem__(self, key):
        return self.values[key]
        
    def __repr__(self):
        return str(self.values)
