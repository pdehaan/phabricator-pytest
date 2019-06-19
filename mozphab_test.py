import imp
import os

print(os.path.join(os.path.dirname(__file__), "moz-phab"))

mozphab = imp.load_source(
    "mozphab", os.path.join(os.path.dirname(__file__), "moz-phab")
    # "mozphab", "moz-phab"
)

print(mozphab.main)


## PYTHON 3.5+?

# import importlib

# try:
#     importlib.import_module('moz-phab')
#     print("success")
# except ImportError as err:
#     print('Error:', err)



"""
import importlib
import sys
import os

# For illustrative purposes.
name = 'moz-phab'


name = os.path.join(os.path.dirname(__file__), os.path.pardir, "moz-phab")
pkg = "mozphab"

spec = importlib.import_module("/Users/pdehaan/dev/github/mozilla/phabricator/git-cinnabar/moz-phab")
if spec is None:
    print("can't find the itertools module")
else:
    # # If you chose to perform the actual import ...
    # module = importlib.util.module_from_spec(spec)
    # spec.loader.exec_module(module)
    # # Adding the module to sys.modules is optional.
    # sys.modules[name] = module

    print("OK")
"""
