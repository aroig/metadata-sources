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
import unicodedata

if sys.version_info[0] >= 3:
    from urllib.parse import urlencode
else:
    from urllib import urlencode

from .latex_encoding import latex_decode
from .utils import surname, metadata_distance, strip_accents
from .bibtexparser import parse_bibtex
from .base import NetbibBase, NetbibError

class MathscinetError(NetbibError):
    pass


class Mathscinet(NetbibBase):
    def __init__(self, browser, timeout=30):
        super(Mathscinet, self).__init__()

        self.search_fields = ['title', 'authors', 'id']
        self.idkey = 'mr'

        self.timeout = timeout
        self.browser = browser
        self.sleep_time = 0.2

        self.url = "http://www.ams.org/mathscinet/search/publications.html"
        self.ans = []


    # Internals
    # ------------------------------ #

    def entry_from_bibtex(self, bib):
        d = super(Mathscinet, self).entry_from_bibtex(bib)

        if 'bibtexkey' in bib.keys():
            d['id'] = self.format_id(bib['bibtexkey'])

        # Series may be in a note.
        if not 'series' in d.keys() and bib['bibtextype'] == 'book' and 'note' in bib.keys():
            series, series_idx = self.format_series_from_note(bib['note'])
            if series:
                d['series'] = series
                if series_idx:
                    d['series_index'] = series_idx

        return d


    def get_matches(self, params):
        query_list = '%s?%s' % (self.url, urlencode(params))
        raw = self.browser.open(query_list, timeout=self.timeout).read()
        rawdata = raw.decode('utf-8', errors='replace').strip()

        m = re.search('<div class="doc">(.*?)</div>', rawdata, re.DOTALL)
        if m: rawdata = m.group(1)
        else: return []

        ans = []
        for entry in re.findall('<pre>(.*?)</pre>', rawdata, re.DOTALL):
            for bib in parse_bibtex(entry):
                ans.append(self.entry_from_bibtex(bib))
        return ans


    def get_item(self, bibid):
        params = self.format_query({'id': bibid})
        ans = self.get_matches(params)

        if len(ans) > 0:
            return ans[0]

        return None


    def get_abstract(self, bibid):
        query_abstract = "http://www.ams.org/mathscinet/search/publdoc.html?pg1=MR&s1=%s" % bibid
        raw = self.browser.open(query_abstract, timeout=self.timeout).read()
        rawdata = raw.decode('utf-8', errors='replace').strip()
        m = re.search('<div class="review">(.*?)</div>', rawdata, re.DOTALL)
        if m:
            abstract = m.group(1).strip()
            L = re.findall("(.*?)<br\s*/>\s*&nbsp;\s*&nbsp;",
                           abstract + '<br />&nbsp;&nbsp;', re.DOTALL)
            Lpar = [self.format_abstract_paragraph(par.strip()) for par in L if len(par.strip()) > 0]
            abstract = ('\n'.join(Lpar)).strip()

            if len(abstract) > 0:
                return abstract

        return None


    def append_query_token(self, params, idx, field, value):
        params['pg%d' % idx] = field
        params['s%d' % idx] = value
        params['co%d' % idx] = 'AND'


    def format_query(self, d, lax=False):
        """Formats a query suitable to send to the arxiv API"""
        for k in d.keys():
            if not k in self.search_fields:
                raise MathscinetError("Error in Mathscinet. Don't understand key: %s" % k)

        params = {}
        idx = 1
        if 'id' in d.keys():
            self.append_query_token(params, idx, 'MR', d['id'])

        elif 'authors' in d.keys() or 'title' in d.keys():
            if 'title' in d.keys():
                if lax: KEY='ALLF'
                else: KEY='TI'

                self.append_query_token(params, idx, KEY, self.clean_query(d['title']))
                idx = idx + 1

            if 'authors' in d.keys():
                words = [surname(a) for a in d['authors']]
                max = min(len(words), 3)
                for i in range(0,max):
                    self.append_query_token(params, idx, 'ICN', self.clean_query(words[i]))
                    idx = idx + 1

        else:
            raise MathscinetError("Error in Mathscinet. Insuficient metadata to construct a query")

        params['fmt'] = 'bibtex'       # Bibtex format
        params['extend'] = '1'         # All in one page

        return params




    # Utility stuff
    # ------------------------------ #

    def format_journal(self, txt):
        txt = super(Mathscinet, self).format_journal(txt)
        m = re.match("(.*)\.", txt, re.DOTALL)   # Kill what appears after the last dot.
        if m: txt = m.group(1).strip()
        return txt


    def format_id(self, bibid):
        return bibid.replace('MR', '').strip()


    def format_series_from_note(self, note):
        m = re.match("(.+?),?\s*(No|Vol|vol|volume|Volume)\.?\s*(\d*)", note)
        if m:
            return (m.group(1), m.group(3))
        else:
            return (None, None)


    def format_abstract_paragraph(self, par):
        par = re.sub('\s+', ' ', par)
        par = re.sub('<span\s+class="it">(.*?)</span>', '<i>\g<1></i>', par, re.DOTALL | re.MULTILINE)
        par = re.sub('<span\s+class="bf">(.*?)</span>', '<b>\g<1></b>', par, re.DOTALL | re.MULTILINE)
        par = re.sub('<span\s+class="it">(.*?)</span>', '<i>\g<1></i>', par, re.DOTALL | re.MULTILINE)
        par = re.sub('<span\s+class="MathTeX">(.*?)</span>', '\g<1>', par, re.DOTALL | re.MULTILINE)
        par = re.sub('<script\s+type="math/tex">(.*?)</script>', '', par, re.DOTALL | re.MULTILINE)

        return '<p>%s</p>' % par.strip()
