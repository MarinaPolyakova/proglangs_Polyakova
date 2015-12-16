from distutils.core import setup, Extension
import numpy.distutils.misc_util

setup(
    ext_modules=[Extension("floydwarshall", ["floyd_warshall.cpp"])],
    include_dirs=numpy.distutils.misc_util.get_numpy_include_dirs(),
)