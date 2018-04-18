from __future__ import print_function
import pyifs
import random, json, argparse, sys

def get_args():
    ap = argparse.ArgumentParser()
    ap.add_argument("configuration")
    args = ap.parse_args()
    return vars(args)

# Since complex numbers are not natively json serializable here is an encoder and decoder to handle them
class ComplexEncoder(json.JSONEncoder):
    def default(self, z):
        if isinstance(z, complex):
            return {"__complex__":True,"real":z.real,"imag":z.imag}
        else:
            super().default(self, z)

def decode_complex(dct):
    if '__complex__' in dct:
        return complex(dct['real'], dct['imag'])
    return dct

if __name__ == "__main__":
    # get arguments
    args = get_args()
    with open(args['configuration']) as f:
        config = json.load(f, object_hook=decode_complex)

    # read configuration
    width, height = config['image_settings']['width'], config['image_settings']['height']
    iterations = config['evaluation_settings']['iterations']
    num_points = config['evaluation_settings']['num_points']

    # initialize system
    image = pyifs.image.Image(width, height)
    ifs = pyifs.ifs.IFS()
    ifs.from_dict(config['transforms'])


    # run!
    image = ifs.evaluate(image, num_points, iterations)

    #save image
    image.save(config['image_settings']['path'],
               max(1, (num_points * iterations) / (height * width)))

    # save system, important if randomized
    out_json = {"image_settings":config['image_settings'],
                'evaluation_settings':config['evaluation_settings'],
                "transforms":ifs.to_dict()}
    out_json_path = "{}.json".format(config['image_settings']['path'].split(".png")[0])
    with open(out_json_path, "w") as f:
        f.write(json.dumps(out_json, cls=ComplexEncoder))
    



