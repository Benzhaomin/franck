#!/bin/sh

python franck-http.py > api.log 2>&1 &
cd html/ && python -m http.server > ../web.log 2>&1 &
