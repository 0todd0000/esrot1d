
import numpy as np
import h5py

def load_h5(fpath):
    d = dict()
    with h5py.File(fpath, 'r') as f:
        for k in f.keys():
            d[k] = np.array(f[k])
    return d

def save_h5(fpath, d):
    with h5py.File(fpath, 'w') as f:
        for key in d.keys():
            f.create_dataset( key, data=d[key], compression='gzip', compression_opts=9 )