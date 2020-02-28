import os
import sys
import json


''' Operations on files. 
    Reading and writing files to/from and manipulate the file 
    Extract various information out of that file
'''
with open('/home/anand/quantela_projects/datascience/modelv2/scheduler/config.json') as config:
    properties = json.load(config)
    print(properties)
