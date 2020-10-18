from setuptools import setup
from Cython.Build import cythonize

# setup(ext_modules=cythonize("test_cy.pyx", annotate=True))
setup(ext_modules=cythonize("test.pyx", annotate=True))
