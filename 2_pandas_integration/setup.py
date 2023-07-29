from distutils.core import setup
from Cython.Build import cythonize

setup(name="cython_pandas", ext_modules=cythonize("./cython_pandas.pyx"))
