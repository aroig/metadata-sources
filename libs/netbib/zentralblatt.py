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

import copy
import time
import sys
import re

if sys.version_info[0] >= 3:
    from urllib.parse import urlencode
else:
    from urllib import urlencode

from .latex_encoding import latex_decode
from .utils import surname, metadata_distance
from .bibtexparser import parse_bibtex
from .base import NetbibBase, NetbibError

class ZentralblattError(NetbibError):
    pass


class Zentralblatt(NetbibBase):
    def __init__(self, browser, timeout=30):
        super(Zentralblatt, self).__init__()

        self.search_fields = ['title', 'authors', 'id']
        self.idkey = 'zbl'

        self.timeout = timeout
        self.browser = browser
        self.sleep_time = 0.2

        self.url_bibtex = "https://zbmath.org/bibtex"
        self.url_query = "https://zbmath.org"
        self.ans = []



    # Internals
    # ------------------------------ #

    def entry_from_bibtex(self, bib):
        d = super(Zentralblatt, self).entry_from_bibtex(bib)

        if 'zbl' in bib.keys():
            d['id'] = self.format_id(bib['zbl'])

        if 'msc2010' in bib.keys():
            d['subject'] = self.format_subject(bib['msc2010'])

        return d


    def get_item(self, bibid):
        query = '%s/%s.bib' % (self.url_bibtex, bibid)
        raw = self.browser.open(query, timeout=self.timeout).read()
        rawdata=raw.decode('utf-8', errors='replace').strip()

        ans = parse_bibtex(rawdata)

        if len(ans) > 0:
            return self.entry_from_bibtex(ans[0])

        return None


    def get_abstract(self, bibid):
        """Returns the answer to a query"""
        params = self.format_query({'id': bibid})
        query = '%s?%s' % (self.url_query, urlencode(params))
        raw = self.browser.open(query, timeout=self.timeout).read()
        rawdata=raw.decode('utf-8', errors='replace').strip()
        m = re.search('<div class="abstract">(.*?)</div>', rawdata, re.DOTALL)
        if m:
            abstract = m.group(1).strip()

            # The abstract section might contain crap
            if '<div class="scan">' in abstract: return None

            L = re.findall("(.*?)\n\s*?\n", abstract + "\n\n", re.DOTALL | re.MULTILINE)
            Lpar = [self.format_abstract_paragraph(par.strip()) for par in L if len(par.strip()) > 0]
            abstract = ('\n'.join(Lpar)).strip()

            if len(abstract) > 0:
                return abstract

        return None


    def get_matches(self, params):
        query = '%s?%s' % (self.url_query, urlencode(params))
        raw = self.browser.open(query, timeout=self.timeout).read()
        rawdata=raw.decode('utf-8', errors='replace').strip()

        ans = []
        # note, we are not catching the id's, just some wat to retrieve the bibtex!
        for bibid in re.findall('"bibtex/(.*).bib"', rawdata):
            item = self.get_item(bibid)
            if item: ans.append(item)

        return ans


    def format_query(self, d, lax=False):
        """Formats a query suitable to send to Zentralblatt API"""
        for k in d.keys():
            if not k in self.search_fields:
                raise ZentralblattError("Error in Zentralblatt. Don't understand key: %s" % k)

        items = []
        if 'id' in d.keys():
            items.append('an:%s' % d['id'])

        elif 'authors' in d.keys() or 'title' in d.keys():
            if 'title' in d.keys():
                if lax: items.append('any:' + ('"%s"' % d['title']))
                else:   items.append('ti:' + ('"%s"' % d['title']))

            if 'authors' in d.keys():
                words = [surname(a) for a in d['authors']]
                for b in words:
                    items.append('au:%s' % b.strip())

        else:
            raise ZentralblattError("Error in Zentralblatt. Insuficient metadata to construct a query")

        params = {'q': ' '.join(items)}
        return params


    # Utility stuff
    # ------------------------------ #

    def format_abstract_paragraph(self, par):
        par = re.sub('\s+', ' ', par)

        return '<p>%s</p>' % par.strip()
