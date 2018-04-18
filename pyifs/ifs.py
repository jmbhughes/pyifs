import random
from . import transform


class IFS:
    ''' representation of an iterated function system, evaluated probabilistically using a list of transforms '''
    
    def __init__(self):
        self.transforms = []
        self.total_weight = 0

    def random(self, count,
               allowed_transforms=[transform.RandomAffineTransform,
                                   transform.RandomMoebiusTransform,
                                   transform.RandomInverseJuliaTransform]):
        for t in random.choices(allowed_transforms, k=count):
            self.add_transform(t)
        
    def from_dict(self, dictionary):
        ''' read in from a dictionary
        this has easy support for reading in from the json transforms section 
        '''
        for transform_type in dictionary:
            transform_class = getattr(transform, transform_type)
            for t in dictionary[transform_type]:
                self.add_transform(transform_class(**t))

    def to_dict(self):
        d = dict()
        for weight, transform in self.transforms:
            name, params = transform.__dict__()
            if name in d:
                d[name].append(params)
            else:
                d[name] = [params]
        return d
    
    def add_transform(self, transform, weight=None):
        ''' append a transform to the system, the weight is assigned randomly if not passed'''
        if not weight:
            weight = random.gauss(1, 0.15) * random.gauss(1, 0.15)
        self.total_weight += weight
        self.transforms.append((weight, transform))
    
    def _choose_transform(self):
        ''' choose a transform at random using the weighting ''' 
        w = random.random() * self.total_weight
        running_total = 0
        for weight, transform in self.transforms:
            running_total += weight
            if w <= running_total:
                return transform
    
    def _final_transform(self, px, py):
        ''' an internal helper function to convert point into proper projection for image plotting '''
        a = 0.5
        b = 0
        c = 0
        d = 1
        z = complex(px, py)
        z2 = (a * z + b) / (c * z + d)
        return z2.real, z2.imag

    def evaluate(self, image, num_points, iterations):
        ''' given an input image from the image class, 
        evaluate the iterated function system probabilistically using
        num_points for specified number of iterations
        '''
        width, height = image.width, image.height
        for i in range(num_points): 
            px = random.uniform(-1, 1)
            py = random.uniform(-1, 1)
            r, g, b = 0.0, 0.0, 0.0
    
            for j in range(iterations):
                t = self._choose_transform()
                px, py = t.transform(px, py)
                r, g, b = t.transform_colour(r, g, b)
                
                fx, fy = self._final_transform(px, py)
                x = int((fx + 1) * width / 2)
                y = int((fy + 1) * height / 2)
                image.add_radiance(x, y, [r, g, b])
        return image

    
