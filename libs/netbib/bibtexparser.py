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

import re

def parse_bibtex(bibtex):
    """Parses a bibtex file and returns a list of dictionaries."""
    L = [parse_bibtex_entry(e) for e in chop_bibtex(bibtex)]
    return [e for e in L if e != None]


def chop_bibtex(s):
    """Chops a bibtex string into individual entries."""
    L = []
    par = 0
    opened = False
    for i in range(0,len(s)):
        if s[i] == '{':
            par = par+1
        elif s[i] == '}':
            par = par-1
            if par == 0 and opened:
                b = i+1
                opened = False
                L.append(s[a:b])
        elif s[i] == '@' and par == 0:
            a = i
            opened = True
    return L


def parse_bibtex_entry(s):
    """Parses a bibtex entry producing a dictionary."""
    bib = {}
    m = re.match("\s*@(.*?)\s*{(.*?),\s*(.*)}", s, re.DOTALL)

    if m == None:
        return None

    bib['bibtextype'] = m.group(1).strip()
    bib['bibtexkey'] = m.group(2).strip()
    raw = m.group(3).strip()
    L1 = re.findall("^\s*([^\n]*?)\s*=\s*{(.*?)}\s*,?\s*$", raw, re.DOTALL | re.MULTILINE)
    L2 = re.findall('^\s*([^\n]*?)\s*=\s*"{?(.*?)}?"\s*,?\s*$', raw, re.DOTALL | re.MULTILINE)
    for it in L1 + L2:
        bib[it[0].strip().lower()] = it[1].strip()
    return bib
