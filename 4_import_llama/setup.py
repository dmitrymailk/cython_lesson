from setuptools import setup

from Cython.Build import cythonize
from distutils.extension import Extension

extensions = [Extension("llama_cy", ["llama_cy.pyx", "llama_c.c"])]
# setup(ext_modules=cythonize("llama_cy.pyx"))
setup(ext_modules=extensions)
