import numpy as np
import pickle

with open('tmp.pickle', mode='rb') as f:
    tmp = pickle.load(f)

import matplotlib.pyplot as p

p.imshow(tmp[47])
p.show()
