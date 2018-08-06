
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import json
from  collections import OrderedDict

filename = './../ControlPanel_Plugins/menu.json'

#with open(filename,'r') as f:
#    e = json.load(f)
with open(filename, 'r') as fp:
    e = json.load(fp, object_pairs_hook=OrderedDict)

for key,val in e.iteritems():
    print("%s" % key)
    print(val['Sub'])