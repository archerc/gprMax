#! python

import gprMax
from tools import plot_Ascan
import os

curdir, filename = os.path.split(__file__) 
basename, ext = os.path.splitext(filename)
in_file = ''.join([curdir, os.path.sep, basename, '.in']);
out_file = ''.join([curdir, os.path.sep, basename, '.out']);
gprMax.run(in_file)
plot_Ascan(out_file)