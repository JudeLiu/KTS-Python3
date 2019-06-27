# from distutils.core import setup
# from Cython.Build import cythonize

# setup(name='cpd_nonlin', ext_modules=cythonize('cpd_nonlin.pyx'))

from distutils.core import setup, Extension
from Cython.Build import cythonize
import numpy

setup(
    ext_modules=cythonize("cython_functions.pyx"),
    include_dirs=[numpy.get_include()]
)  