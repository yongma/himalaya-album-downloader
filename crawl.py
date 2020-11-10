#!/usr/bin/env python
# -*- coding: utf-8 -*-
# himalaya
# crawl
# 2020-11-10

from __future__ import print_function
import sys
from scrapy.cmdline import execute

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("usage: [python] {} ALBUM_URL".format(sys.argv[0]))
        sys.exit(0)
    album_url = sys.argv[1]
    execute(['scrapy', 'crawl', 'album', "-a", "album_url={}".format(album_url)])
