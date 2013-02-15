#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# netbib - collect bibliographical data over the net
# Copyright 2012 Abdó Roig-Maranges <abdo.roig@gmail.com>
#
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program.  If not, see <http://www.gnu.org/licenses/>.

from __future__ import (unicode_literals, division)

import sys

if sys.version_info[0] >= 3:
    from urllib.request import build_opener
else:
    from urllib2 import build_opener


from .zentralblatt import Zentralblatt
from .mathscinet import Mathscinet
from .arxiv import Arxiv


def test():
    browser = build_opener()

    print("Arxiv")
    arxiv = Arxiv(browser)
    ans = arxiv.query_and_wait({'authors': ['Kontsevich']})
    for d in ans: print('%s - %s' % (', '.join(d['authors']), d['title']))
    print("")


    print("Zentralblatt")
    zbl = Zentralblatt(browser)
    ans = zbl.query_and_wait({'authors': ['Kontsevich']})
    for d in ans: print('%s - %s' % (', '.join(d['authors']), d['title']))
    print("")

    print("Mathscinet")
    mr = Mathscinet(browser)
    ans = mr.query_and_wait({'authors': ['Kontsevich']})
    for d in ans: print('%s - %s' % (', '.join(d['authors']), d['title']))
    print("")
