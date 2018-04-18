from __future__ import print_function
import random, json, argparse, sys
from math import cos, sin, pi, atan2, sqrt
from image import Image
from abc import ABCMeta, abstractmethod

def random_complex_number():
    return complex(random.uniform(-1, 1), random.uniform(-1, 1))

class IFS:
    ''' representation of an iterated function system, evaluated probabilistically using a list of transforms '''
    
    def __init__(self):
        self.transforms = []
        self.total_weight = 0
    
    def add_transform(self, transform, weight=None):
        ''' append a transform to the system, the weight is assigned randomly if not passed'''
        if not weight:
            weight = random.gauss(1, 0.15) * random.gauss(1, 0.15)
        self.total_weight += weight
        self.transforms.append((weight, transform))
    
    def choose_transform(self):
        ''' choose a transform at random using the weighting ''' 
        w = random.random() * self.total_weight
        running_total = 0
        for weight, transform in self.transforms:
            running_total += weight
            if w <= running_total:
                return transform
    
    def final_transform(self, px, py):
        a = 0.5
        b = 0
        c = 0
        d = 1
        z = complex(px, py)
        z2 = (a * z + b) / (c * z + d)
        return z2.real, z2.imag

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

class LinearTransform(Transform):
    ''' a linear transformation as described by a matrix [[a,b],[c,d]] '''
    def __init__(self,matrix):
        super(LinearTransform, self).__init__()
        (self.a, self.b), (self.c, self.d) = matrix
            
    def transform(self, px, py):
        return (self.a * px + self.b * py, self.c * px + self.d * py)

    def __str__(self):
        return "Linear:[[{:+0.5f},{:+0.5f}],[{:+0.5f},{:+0.5f}]]".format(self.a, self.b, self.c, self.d)
    
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
    def __init__(self):
        super(MoebiusTransform, self).__init__()
        self.pre_a = random_complex_number()
        self.pre_b = random_complex_number()
        self.pre_c = random_complex_number()
        self.pre_d = random_complex_number()
    
    def f(self, z):
        ''' function defining the transformation '''
        return (self.pre_a * z + self.pre_b) / (self.pre_c * z + self.pre_d)

    def __str__(self):
        return "Moebius:(({0.real:.5f}+{0.imag:.5f}i)z+({1.real:.5f}+{1.imag:.5f}i))/(({2.real:.5f}+{2.imag:.5f}i)z+({3.real:.5f}+{3.imag:.5f}i))".format(self.pre_a, self.pre_b, self.pre_c, self.pre_d)

class MoebiusBase(ComplexTransform):
    def __init__(self):
        super(MoebiusBase, self).__init__()
        self.pre_a = random_complex_number()
        self.pre_b = random_complex_number()
        self.pre_c = random_complex_number()
        self.pre_d = random_complex_number()
        self.post_a = random_complex_number()
        self.post_b = random_complex_number()
        self.post_c = random_complex_number()
        self.post_d = random_complex_number()
    
    def f(self, z):
        z2 = (self.pre_a * z + self.pre_b) / (self.pre_c * z + self.pre_d)
        z = self.f2(z2)
        z2 = (self.post_a * z + self.post_b) / (self.post_c * z + self.post_d)

class InverseJulia(ComplexTransform):    
    def __init__(self):
        super(InverseJulia, self).__init__()
        self.r = sqrt(random.random()) * 0.4 + 0.8
        self.theta = 2 * pi * random.random()
        self.c = complex(self.r * cos(self.theta), self.r * sin(self.theta))
    
    def f(self, z):
        z2 = self.c - z
        theta = atan2(z2.imag, z2.real) * 0.5
        sqrt_r = random.choice([1, -1]) * ((z2.imag * z2.imag + z2.real * z2.real) ** 0.25)
        return complex(sqrt_r * cos(theta), sqrt_r * sin(theta))

    def __str__(self):
        return "Inverse Julia: r={}, theta={}".format(self.r, self.theta)
    
def get_args():
    ap = argparse.ArgumentParser()
    ap.add_argument("configuration")
    args = ap.parse_args()
    return vars(args)

if __name__ == "__main__":
    args = get_args()
    with open(args['configuration']) as f:
        config = json.load(f)

    # read configuration
    WIDTH = config['image_settings']['width']
    HEIGHT = config['image_settings']['height']
    ITERATIONS = config['evaluation_settings']['iterations']
    NUM_POINTS = config['evaluation_settings']['num_points']
    NUM_TRANSFORMS = 7

    # initialize system
    h = Image(WIDTH, HEIGHT)
    ifs = IFS()

    f = open("system.txt", "w")
    # initialize transforms
    for transform_type in config['transforms']:
        transform = getattr(sys.modules[__name__], transform_type)
        for t in config['transforms'][transform_type]:
            tt = transform(**t)
            f.write(str(tt) + "\n")
            ifs.add_transform(tt)

    f.close()
    # run!
    for i in range(NUM_POINTS):
        px = random.uniform(-1, 1)
        py = random.uniform(-1, 1)
        r, g, b = 0.0, 0.0, 0.0
    
        for j in range(ITERATIONS):
            t = ifs.choose_transform()
            px, py = t.transform(px, py)
            r, g, b = t.transform_colour(r, g, b)
        
            fx, fy = ifs.final_transform(px, py)
            x = int((fx + 1) * WIDTH / 2)
            y = int((fy + 1) * HEIGHT / 2)
            h.add_radiance(x, y, [r, g, b])

    # save image
    h.save(config['image_settings']['path'],
           max(1, (NUM_POINTS * ITERATIONS) / (HEIGHT * WIDTH)))
                   
