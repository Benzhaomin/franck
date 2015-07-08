#!/bin/sh

python /home/ben/dev/python/franck/current/FranckCli.py "$@" | xargs /home/ben/dev/bash/wget.sh

