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

        self.search_fields = ['title', 'authors', 'mr']
        self.idkey = 'mr'

        self.timeout = timeout
        self.browser = browser
        self.sleep_time = 0.2

        self.url = "http://www.ams.org/mathscinet/search/publications.html"
        self.ans = []



    def run(self):
        # First run with authors as authors.
        params = self.format_query(self.query, title_all=False)
        ans = self.query_mathscinet(params)

        # If no luck, try something else. Split the title ?
        if len(ans) == 0:
            time.sleep(self.sleep_time)
            params = self.format_query(self.query, title_all=True)
            ans = self.query_mathscinet(params)

        if len(ans) > 0:
            ans = self.sort_and_trim(ans)

            # Download abstracts.
            for d in ans:
                time.sleep(self.sleep_time)
                abstract = self.get_abstract(d['mr'])
                if abstract:
                    d['abstract'] = abstract

            self.ans = ans
        else:
            self.ans = []



    def query_mathscinet(self, params):
        query_list = '%s?%s' % (self.url, urlencode(params))
        raw = self.browser.open(query_list, timeout=self.timeout).read()
        rawdata = raw.decode('utf-8', errors='replace').strip()

        m = re.search('<div class="doc">(.*?)</div>', rawdata, re.DOTALL)
        if m: rawdata = m.group(1)
        else: return []

        bibentries = re.findall('<pre>(.*?)</pre>', rawdata, re.DOTALL)
        entries = parse_bibtex('\n'.join(bibentries))

        ans = []
        for bib in entries:
            d = {}
            if 'bibtexkey' in bib.keys():
                d['mr'] = self.format_MR(bib['bibtexkey'])

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

#      Seems no language on mathscinet
#      if 'language' in bib.keys():
#        d['language'] = bib['language'].lower().strip()

            if 'doi' in bib.keys():
                d['doi'] = bib['doi'].strip()

            if 'isbn' in bib.keys():
                d['isbn'] = self.clean_isbn(bib['isbn'])

#      if 'isbn' in bib.keys() and 'mr' in bib.keys():
#        self.cache_isbn_to_identifier(d['isbn'], d['mr'])

            if 'publisher' in bib.keys():
                d['publisher'] = self.format_text(bib['publisher'])

            if 'series' in bib.keys():
                d['series'] = self.format_text(bib['series'])
                if 'volume' in bib.keys():
                    d['series_index'] = bib['volume'].strip()

            # Series may be in a note.
            elif bib['bibtextype'] == 'book' and 'note' in bib.keys():
                series, series_idx = self.format_series_from_note(bib['note'])
                if series:
                    d['series'] = series
                    if series_idx:
                        d['series_index'] = series_idx

            if 'fjournal' in bib.keys():
                d['journal'] = self.format_fjournal(bib['fjournal'])
            elif 'journal' in bib.keys():
                d['journal'] = self.format_text(bib['journal'])

            if 'volume' in bib.keys():
                d['volume'] = bib['volume'].strip()

            if 'number' in bib.keys():
                d['number'] = bib['number'].strip()

            if 'year' in bib.keys():
                year = self.format_year(bib['year'].strip())
                if year: d['year'] = year

            ans.append(d)

        return ans



    def append_query_token(self, params, idx, field, value):
        params['pg%d' % idx] = field
        params['s%d' % idx] = value
        params['co%d' % idx] = 'AND'



    def format_query(self, d, title_all=False):
        """Formats a query suitable to send to the arxiv API"""
        for k in d.keys():
            if not k in self.search_fields:
                raise MathscinetError("Error in Mathscinet. Don't understand keys")

        params = {}
        idx = 1
        if 'mr' in d.keys():
            self.append_query_token(params, idx, 'MR', d['mr'])

        elif 'authors' in d.keys() or 'title' in d.keys():
            if 'title' in d.keys():
                if title_all: KEY='ALLF'
                else: KEY='TI'

                self.append_query_token(params, idx, KEY, self.format_query_text(d['title']))
                idx = idx + 1

            if 'authors' in d.keys():
                words = [surname(a) for a in d['authors']]
                max = min(len(words), 3)
                for i in range(0,max):
                    self.append_query_token(params, idx, 'ICN', self.format_query_text(words[i]))
                    idx = idx + 1

        else:
            raise MathscinetError("Error in Mathscinet. Insuficient metadata to construct a query")

        params['fmt'] = 'bibtex'       # Bibtex format
        params['extend'] = '1'         # All in one page

        return params



    def format_fjournal(self, fj):

        txt = self.format_text(fj)

        m = re.match("(.*)\.", txt, re.DOTALL)   # Kill what appears after the last dot.
        if m: txt = m.group(1).strip()

        m = re.match("(.*?)\(", txt, re.DOTALL)   # Kill what appears after the first parenthesis.
        if m: txt = m.group(1).strip()

        return txt



    def format_MR(self, mr):
        return mr.replace('MR', '').strip()



    def format_series_from_note(self, note):
        m = re.match("(.+?),?\s*(No|Vol|vol|volume|Volume)\.?\s*(\d*)", note)
        if m:
            return (m.group(1), m.group(3))
        else:
            return (None, None)



    def get_abstract(self, mr):
        query_abstract = "http://www.ams.org/mathscinet/search/publdoc.html?pg1=MR&s1=%s" % mr
        raw = self.browser.open(query_abstract, timeout=self.timeout).read()
        rawdata = raw.decode('utf-8', errors='replace').strip()
        m = re.search('<div class="review">(.*?)</div>', rawdata, re.DOTALL)
        if m:
            abs = m.group(1).strip()
            L = re.findall("(.*?)<br\s*/>\s*&nbsp;\s*&nbsp;", abs + '<br />&nbsp;&nbsp;', re.DOTALL)
            Lpar = [self.format_abstract_paragraph(par.strip()) for par in L]
            formated_abstract = ('\n'.join(Lpar)).strip()
            if formated_abstract == "":
                return None
            else:
                return formated_abstract
        else:
            return None



    def format_abstract_paragraph(self, par):
        par = re.sub('\s+', ' ', par)
        par = re.sub('<span\s+class="it">(.*?)</span>', '<i>\g<1></i>', par, re.DOTALL | re.MULTILINE)
        par = re.sub('<span\s+class="bf">(.*?)</span>', '<b>\g<1></b>', par, re.DOTALL | re.MULTILINE)
        par = re.sub('<span\s+class="it">(.*?)</span>', '<i>\g<1></i>', par, re.DOTALL | re.MULTILINE)
        par = re.sub('<span\s+class="MathTeX">(.*?)</span>', '\g<1>', par, re.DOTALL | re.MULTILINE)
        par = re.sub('<script\s+type="math/tex">(.*?)</script>', '', par, re.DOTALL | re.MULTILINE)

        return '<p>%s</p>' % par



    def clean_isbn(self, isbn):
        return isbn.replace('-', '').strip()



    def format_query_text(self, txt):
        # The wildcard does not work inside "".
        # txt = re.sub('[^\x00-\x7F]', '*', txt)
        # But arxiv does not like non-ascii characters. So I strip accents.
        return strip_accents(txt).strip()
