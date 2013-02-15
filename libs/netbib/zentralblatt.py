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

        self.search_fields = ['title', 'authors', 'zbl']
        self.idkey = 'zbl'

        self.timeout = timeout
        self.browser = browser
        self.sleep_time = 0.2

        self.url_bibtex = "http://www.zentralblatt-math.org/zmath/en/search/zmath.bibtex"
        self.url_xml = "http://www.zentralblatt-math.org/zmath/en/search/zmath.xml"
        self.ans = []

        self.lang_map = {'English': 'eng',
                         'German': 'deu',
                         'French': 'fra',
                         'Spanish': 'spa'}



    def run(self):
        params = self.format_query(self.query, type='bibtex')
#    params = self.format_query(self.query, type='xml')
        ans = self.query_zentralblatt(params)

        # If no luck, relax the query
        if len(ans) == 0:
            # TODO
            pass

        if len(ans) > 0:
            ans = self.sort_and_trim(ans)
            self.ans = ans
        else:
            self.ans = []



    def query_zentralblatt(self, params):
        query = '%s?%s' % (self.url_bibtex, urlencode(params))
        raw_bibtex = self.browser.open(query, timeout=self.timeout).read()
        if sys.version_info[0] >= 3: raw_bibtex = raw_bibtex.decode('utf-8')
        raw_bibtex = raw_bibtex.strip()
        entries = parse_bibtex(raw_bibtex)

        ans = []
        for bib in entries:
            d = {}
            if 'bibtexkey' in bib.keys():
                d['zbl'] = self.format_text(bib['bibtexkey'])

            if 'bibtextype' in bib.keys():
                d['type'] = bib['bibtextype'].strip().lower()

            if 'title' in bib.keys():
                d['title'] = self.format_title(bib['title'])

            if 'author' in bib.keys():
                d['authors'] = [self.format_author(e)
                                for e in bib['author'].split('and')]
            elif 'editor' in bib.keys():
                d['authors'] = [self.format_author(e)
                                for e in bib['editor'].split('and')]

            if 'language' in bib.keys():
                lang = self.language_code(bib['language'].strip())
                if lang:
                    d['language'] = lang

            if 'doi' in bib.keys():
                d['doi'] = bib['doi'].strip()

            if 'isbn' in bib.keys():
                d['isbn'] = bib['isbn'].strip()

            if 'publisher' in bib.keys():
                d['publisher'] = self.format_text(bib['publisher'])

            if 'journal' in bib.keys():
                d['journal'] = self.format_text(bib['journal'])

            if 'volume' in bib.keys():
                d['volume'] = bib['volume'].strip()

            if 'number' in bib.keys():
                d['number'] = bib['number'].strip()

            if 'year' in bib.keys():
                year = self.format_year(bib['year'].strip())
                if year: d['year'] = year

            if 'abstract' in bib.keys():
                d['abstract'] = latex_decode(bib['abstract'].strip())

            ans.append(d)

        return ans



    def format_query(self, d, type):
        """Formats a query suitable to send to the arxiv API"""
        for k in d.keys():
            if not k in self.search_fields:
                raise ZentralblattError("Error in Zentralblatt. Don't understand keys")

        items = []
        if 'zbl' in d.keys():
            items.append('an:%s' % d['zbl'])

        elif 'authors' in d.keys() or 'title' in d.keys():
            if 'title' in d.keys():
                items.append('ti:' + ('"%s"' % d['title']))

            if 'authors' in d.keys():
                words = [surname(a) for a in d['authors']]
                for b in words:
                    items.append('au:%s' % b.strip())

        else:
            raise ZentralblattError("Error in Zentralblatt. Insuficient metadata to construct a query")

        params = {'q': ' '.join(items), 'format': 'complete', 'type': type}
        return params



    def language_code(self, lang):
        return self.lang_map.get(lang, None)
