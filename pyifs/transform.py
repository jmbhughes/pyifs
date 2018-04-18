from abc import ABCMeta, abstractmethod
from math import cos, sin, pi, atan2, sqrt
import random

def random_complex_number():
    return complex(random.uniform(-1, 1), random.uniform(-1, 1))


class Transform(object):
    ''' a generic representation of a transform '''
    __metaclass__ = ABCMeta
    def __init__(self, name="blank"):
        self.r = random.random()
        self.g = random.random()
        self.b = random.random()
    
    def transform_colour(self, r, g, b):
        ''' modify the color of the points iteratively in the drawing'''
        r = (self.r + r) / 2
        g = (self.g + g) / 2
        b = (self.b + b) / 2
        return r, g, b

    @abstractmethod
    def transform(self, px, py):
        ''' perform the transform function '''
        pass

    @abstractmethod
    def __dict__(self):
        ''' convert to a dictionary of required parameters '''
        pass
    
class LinearTransform(Transform):
    ''' a linear transformation as described by a matrix [[a,b],[c,d]] '''
    def __init__(self,matrix):
        super(LinearTransform, self).__init__()
        (self.a, self.b), (self.c, self.d) = matrix
            
    def transform(self, px, py):
        return (self.a * px + self.b * py, self.c * px + self.d * py)

    def __str__(self):
        return "Linear:[[{:+0.5f},{:+0.5f}],[{:+0.5f},{:+0.5f}]]".format(self.a, self.b, self.c, self.d)

    def __dict__(self):
        return "Linear", {"matrix":[[self.a, self.b], [self.c, self.d]]}
    
class RandomLinearTransform(LinearTransform):
    ''' an extension of a linear transformation that randomly is generated '''
    def __init__(self, bounds=(-1,1)):
        a = random.uniform(*bounds)
        b = random.uniform(*bounds)
        c = random.uniform(*bounds)
        d = random.uniform(*bounds)
        m = [[a,b],[c,d]]
        super(RandomLinearTransform, self).__init__(m)

class AffineTransform(Transform):
    ''' an affine transfromation, combination of linear transform and translation'''
    def __init__(self, matrix, translation):
        super(AffineTransform, self).__init__()
        (self.a, self.b), (self.c, self.d) = matrix
        self.xshift, self.yshift = translation
            
    def transform(self, px, py):
        return ((self.a * px + self.b * py) + self.xshift,
                (self.c * px + self.d * py) + self.yshift)

    def __str__(self):
        return "Affine:[[{:+0.5f},{:+0.5f}],[{:+0.5f},{:+0.5f}]]+[{:+0.5f},{:+0.5f}]".format(self.a, self.b, self.c, self.d, self.xshift, self.yshift)

    def __dict__(self):
        return "AffineTransform", {"matrix":[[self.a, self.b],[self.c, self.d]],
                                   'translation':[self.xshift, self.yshift]}

class RandomAffineTransform(AffineTransform):
    ''' an affine transfromation, combination of linear transform and translation'''
    def __init__(self, bounds=(-1,1), shift=(-2,2)):
        a = random.uniform(*bounds)
        b = random.uniform(*bounds)
        c = random.uniform(*bounds)
        d = random.uniform(*bounds)
        m = [[a,b],[c,d]]
        x = random.uniform(*shift)
        y = random.uniform(*shift)
        s = [x,y]
        super(RandomAffineTransform, self).__init__(m,s)
        
class ComplexTransform(Transform):
    ''' base class for a complex transformation ''' 
    def transform(self, px, py):
        z = complex(px, py)
        z2 = self.f(z)
        return z2.real, z2.imag

class MoebiusTransform(ComplexTransform):
    def __init__(self, a, b, c, d):
        self.pre_a = a
        self.pre_b = b
        self.pre_c = c
        self.pre_d = d
        
    def f(self, z):
        ''' function defining the transformation '''
        return (self.pre_a * z + self.pre_b) / (self.pre_c * z + self.pre_d)

    def __str__(self):
        return "Moebius:(({0.real:.5f}+{0.imag:.5f}i)z+({1.real:.5f}+{1.imag:.5f}i))/(({2.real:.5f}+{2.imag:.5f}i)z+({3.real:.5f}+{3.imag:.5f}i))".format(self.pre_a, self.pre_b, self.pre_c, self.pre_d)
        self.pre_d = d

    def __dict__(self):
        return "MoebiusTransform", {"a":self.pre_a,
                                    "b":self.pre_b,
                                    "c":self.pre_c,
                                    "d":self.pre_d}
        
class RandomMoebiusTransform(MoebiusTransform):
    def __init__(self):
        a = random_complex_number()
        b = random_complex_number()
        c = random_complex_number()
        d = random_complex_number()
        super(RandomMoebiusTransform, self).__init__(a,b,c,d)
    

# class MoebiusBase(ComplexTransform):
#     def __init__(self):
#         super(MoebiusBase, self).__init__()
#         self.pre_a = random_complex_number()
#         self.pre_b = random_complex_number()
#         self.pre_c = random_complex_number()
#         self.pre_d = random_complex_number()
#         self.post_a = random_complex_number()
#         self.post_b = random_complex_number()
#         self.post_c = random_complex_number()
#         self.post_d = random_complex_number()
    
#     def f(self, z):
#         z2 = (self.pre_a * z + self.pre_b) / (self.pre_c * z + self.pre_d)
#         z = self.f2(z2)
#         z2 = (self.post_a * z + self.post_b) / (self.post_c * z + self.post_d)

class InverseJuliaTransform(ComplexTransform):    
    def __init__(self, r, theta):
        super(InverseJulia, self).__init__()
        self.r = r
        self.theta = theta
        self.c = complex(self.r * cos(self.theta), self.r * sin(self.theta))
    
    def f(self, z):
        z2 = self.c - z
        theta = atan2(z2.imag, z2.real) * 0.5
        sqrt_r = random.choice([1, -1]) * ((z2.imag * z2.imag + z2.real * z2.real) ** 0.25)
        return complex(sqrt_r * cos(theta), sqrt_r * sin(theta))

    def __str__(self):
        return "Inverse Julia: r={}, theta={}".format(self.r, self.theta)

    def __dict__(self):
        return "InverseJuliaTransform", {"r": self.r,
                                         "theta": self.theta}

class RandomInverseJuliaTransform(InverseJuliaTransform):
    def __init__(self):
        r = sqrt(random.random()) * 0.4 + 0.8
        theta = 2 * pi * random.random()
        super(RandomInverseJuliaTransform, self).__init__(r,theta)
        
