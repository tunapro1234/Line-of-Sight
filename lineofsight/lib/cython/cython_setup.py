from setuptools import setup
from Cython.Build import cythonize

path = "lineofsight/lib/cython/"
setup(ext_modules=cythonize(f"{path}ray_cy.pyx", annotate=True))
