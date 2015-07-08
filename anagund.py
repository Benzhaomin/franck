#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys

import franck.model.crawler as crawler

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("what page?")
        sys.exit(1)

    crawler.parse(sys.argv[1])
