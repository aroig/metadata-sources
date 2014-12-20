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
import threading
from .utils import metadata_distance
from .latex_encoding import latex_decode



class NetbibError(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)



class NetbibBase(threading.Thread):
    def __init__(self):
        super(NetbibBase, self).__init__()


    def query(self, d, maxresults=20):
        """Performs a query with the data in the dictionary d. Starts the job and returns
           When the job is finished, the answer is in self.ans"""

        self.maxresults = maxresults
        self.query = d
        self.start()


    def query_and_wait(self, d, maxresults=20):
        """Performs a query and waits until the job is done. Returns the answer."""
        self.query(d, maxresults)

        while self.is_alive():
            self.join(0.2)

        return self.ans


    def format_text(self, tx):
        tx2 = re.sub("\s+", ' ', latex_decode(tx.strip()))
        tx2 = re.sub("{(\w*?)}", "\g<1>", tx2, re.DOTALL)    # Removes silly {}
        return tx2


    def format_title(self, ti):
        tx = self.format_text(ti)
        tx = re.sub("\$(.*?)\$", '\g<1>', tx, re.DOTALL)     # Remove dollars
        tx = re.sub("{([^{}]*?)}", "\g<1>", tx, re.DOTALL)   # Removes more {}
        m = re.match("(.*)\.", tx)                           # Removes dot at the end.
        if m: tx = m.group(1)
        return tx


    def format_author(self, au):
        au = re.sub("{([^{}]*?)}", "\g<1>", au, re.DOTALL)   # Removes more {}
        L = self.format_text(au).split(',')
        if len(L) != 2: return au
        else:           return L[1].strip() + " " + L[0].strip()


    def format_year(self, yr):
        m = re.search('(\d+)', yr)
        if m: return m.group(1)
        else: return None


    def sort_and_trim(self, ans):
        """Sort results according to relevance and trim to max results."""
        def sort_key(d):
            return metadata_distance(d, self.query, self.idkey)

        ans.sort(key = sort_key)
        return ans[:self.maxresults]
