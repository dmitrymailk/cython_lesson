from distutils.core import setup
from setuptools import Extension
from Cython.Build import cythonize

setup(
    name="cpython_glue",
    ext_modules=cythonize(
        [
            Extension(
                "*",
                ["*.pyx"],
                extra_compile_args=["-O3"],
            )
        ],
        compiler_directives={"language_level": "3"},
    ),
)
