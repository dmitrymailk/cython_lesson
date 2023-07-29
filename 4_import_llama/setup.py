from setuptools import setup

from Cython.Build import cythonize
from distutils.extension import Extension

extensions = [Extension("llama_cy", ["llama_cy.pyx", "llama_c.c"])]
setup(
    ext_modules=extensions,
    extra_compile_args=["-O3"],
)
