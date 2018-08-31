#! python

import gprMax
import os

curdir, filename = os.path.split(__file__) 
basename, ext = os.path.splitext(filename)
in_file = ''.join([curdir, os.path.sep, basename, '.in']);
out_file = ''.join([curdir, os.path.sep, basename, '.out']);
try:
	gprMax.run(in_file)
except Exception as e:
	raise e
