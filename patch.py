from abc import ABCMeta, abstractmethod
from Vector import Vector
import math

class Patch:
    __metaclass__ = ABCMeta
    
    def __init__(self):
        self._delta = 0.001
    
    @abstractmethod
    def call(self, point): raise NotImplementedError

    @classmethod
    def create(cls, fx, fy, fz):
        class DynamicPatch(Patch):
            def __init__(self):
                super().__init__()
            
            def call(self, point):
                u = point[0]
                v = point[1]
                x = fx(u, v)
                y = fy(u, v)
                z = fz(u, v)
                return Vector(x, y, z)
        return DynamicPatch()

    def uVelocity(self, point):
        return  (self.call(point + Vector(0, 1)*self._delta) - self.call(point)) * (1/self._delta) 
    def vVelocity(self, point):
        return (self.call(point + Vector(1, 0)*self._delta) - self.call(point)) * (1/self._delta)
    
    def unitNormalR(self, point):
        return self.uVelocity(point).cross(self.vVelocity(point)).normalized()
    
    def unitNormalL(self, point):
        return self.vVelocity(point).cross(self.uVelocity(point)).normalized()
    
    
    def tangentSpaceBasis(self, point):
        uVel = self.uVelocity(point)
        return [
            uVel,
            self.unitNormalR(point).cross(uVel)
        ]
    
    
    def tangentSpaceSample(self, point, n_samples):
        basis = self.tangentSpaceBasis(point)
        sample = [None for _ in range(n_samples)]
        for i in range(n_samples):
            angle = i*(math.pi*2/n_samples)
            sample[i] = basis[0]*math.sin(angle) + basis[1]*math.cos(angle)
        return sample
    
    
    def covariant(self, point, direction):
        normal = self.unitNormalR(point)
        
        cpt = self.call(point)
        
        next_pt = self.inverseOfQAroundP(point,cpt,  cpt + (direction *self._delta))
        
        return (self.unitNormalR(next_pt) - normal)* (1/self._delta)
    
    
    def shapeOperator(self, point, direction):
        return -1*self.covariant(point, direction)
    
    
    def normalCurvature(self, point, direction):
        return (direction*self.shapeOperator(point, direction) ) / (direction* direction)
    
    
    def tangentSpaceProjection(self, point, vec):
        normal = self.unitNormalR(point)
        return vec - normal * ( vec*normal )
        
    
    def inverseOfQAroundP(self, pinv, p, q):
        v =p - self.tangentSpaceProjection(pinv, q)
        
        vInv = Vector(
            self.uVelocity(pinv) * v, 
            self.vVelocity(pinv) * v
        )
        
        return pinv + vInv
        
    
    def meanCurvature(self, point):
        uVel = self.uVelocity(point)
        vVel = self.vVelocity(point)
        
        E = uVel * uVel
        G = vVel * vVel
        F = uVel * vVel
        
        shapeU = self.shapeOperator(point, uVel)
        shapeV = self.shapeOperator(point, vVel)
        
        L = shapeU * uVel
        N = shapeV * vVel
        M = shapeV * uVel
        return (G*L + E*N - 2*F*M)/ (2*(E*G - F*F));
    
    
    def gaussianCurvature(self, point):
        uVel = self.uVelocity(point)
        vVel = self.vVelocity(point)
        
        E = uVel * uVel
        G = vVel * vVel
        F = uVel * vVel
        
        shapeU = self.shapeOperator(point, uVel)
        shapeV = self.shapeOperator(point, vVel)
        
        L = shapeU * uVel
        N = shapeV * vVel
        M = shapeV * uVel
        
        return ( (L*N) - (M*M) ) / ( (E*G) - (F*F) )
