from __future__ import print_function
import random, json, argparse, sys

from image import Image
from abc import ABCMeta, abstractmethod
from math import cos, sin, pi, atan2, sqrt

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
                   
