from distutils.core import setup
from Cython.Build import cythonize

setup(name="loop_cpython", ext_modules=cythonize("./loop_cpython.pyx"))
