import sys
import os

path = "lineofsight/lib/cython/"
if sys.platform.startswith("win"):
    os.system(f"python {path}cython_setup.py build_ext --inplace")

    name = "ray_cy.cp38-win_amd64.pyd"
    path = path[:-7]
    os.replace(name, path + name)

elif sys.platform.startswith("linux"):
    os.system(f"python3 {path}cython_setup.py build_ext --inplace")

else:
    raise Exception("Unknown system")
