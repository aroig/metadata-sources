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

from difflib import SequenceMatcher
from math import log, exp

import unicodedata
import sys
import re

def ratio(stra, strb):
    return SequenceMatcher(None, stra, strb).ratio()


def metadata_distance(dquery, dresult, idkey=None):
    """Computes the distance between two metadata registers coded as a dictionary.
       Takes into account the fields: title, author and idkey. Returns a float between 0 and 1.
       0 means perfect match, 1 means maximally distinct."""

    # If idkeys match, we got it. If they are different, we don't.
    if idkey:
        if idkey in dquery.keys() and idkey in dresult.keys():
            if dquery[idkey] == dresult[idkey]: return 0.
            else: return 1.

    L = []

    if 'authors' in dquery.keys() and 'authors' in dresult.keys():
        if dquery['authors'] and dresult['authors']:
            L.append(authors_distance(dquery['authors'], dresult['authors']))

    if 'title' in dquery.keys() and 'title' in dresult.keys():
        if dquery['title'] and dresult['title']:
            L.append(title_distance(dquery['title'], dresult['title']))

    return combine_distances(L)



def authors_distance(authorsa, authorsb):
    """Computes the distance between lists of authors. Only surnames are taken into account."""

    lmax = max(len(authorsa), len(authorsb))
    ratios = [ratio(surname(a), surname(b)) for a, b in zip(authorsa, authorsb)]
    return 1 - sum(ratios)/lmax



def title_distance(titlea, titleb):
    """Computes the distance between two titles. Takes into account the possibility of having
       the subtitle after a colon."""

    rt = ratio(titlea.strip(), titleb.strip())

    if len(titlea) > len(titleb):
        tmax = titlea; tmin = titleb
    else:
        tmax = titleb; tmin = titlea

    m = re.match("(.*):", tmax)
    if m: rt2 = ratio(m.group(1).strip(), tmin.strip())
    else: rt2 = 0.

    return 1 - max(rt, rt2)


def combine_distances(l):
    if len(l) == 0: return 1.
    if 1. in l: return 1.

    ltrans = [-log(1-r) for r in l]
    val = sum(ltrans) / len(ltrans)
    return 1 - exp(-val)



def surname(fullname):
    """Returns the surname of an author, which is assumed to be the last word."""
    if ',' in fullname: return fullname.split(',')[0]
    else:               return fullname.split(' ')[-1]


def strip_accents(s):
    if sys.version_info[0] >= 3:     su = s
    else:                            su = unicode(s)

    nkfd_form = unicodedata.normalize('NFKD', su)
    return "".join([c for c in nkfd_form if not unicodedata.combining(c)])
