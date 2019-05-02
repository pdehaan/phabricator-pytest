#!/usr/bin/env sh

FILE=${1:-test_plan.py}

autopep8 $FILE --in-place
pylint $FILE
