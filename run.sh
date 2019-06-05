#!/usr/bin/env sh

FILE=${1:-test_plan.py}

pytest $FILE -sv
