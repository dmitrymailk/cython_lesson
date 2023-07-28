from distutils.core import setup
from Cython.Build import cythonize

import numpy

setup(
    name="spacy_cython",
    ext_modules=cythonize("./spacy_cython.pyx"),
    include_dirs=[numpy.get_include()],
)
