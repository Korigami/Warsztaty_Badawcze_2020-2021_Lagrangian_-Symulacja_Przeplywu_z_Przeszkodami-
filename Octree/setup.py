import setuptools
from distutils.core import Extension, setup
from Cython.Build import cythonize
import numpy

ext = Extension(name="octree", sources=["octree.pyx"])
setup(ext_modules=cythonize(ext), include_dirs=[numpy.get_include()])
