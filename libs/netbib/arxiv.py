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

import time
import sys
import re
import xml.etree.ElementTree

if sys.version_info[0] >= 3:
    from urllib.parse import urlencode
else:
    from urllib import urlencode

import unicodedata

from .utils import surname, strip_accents
from .base import NetbibBase, NetbibError



class ArxivError(NetbibError):
    pass


class Arxiv(NetbibBase):
    def __init__(self, browser, timeout=30):
        super(Arxiv, self).__init__()

        self.query_maxresults = 100

        self.search_fields = ['title', 'authors', 'arxiv']
        self.idkey = 'arxiv'

        self.timeout = timeout
        self.browser = browser
        self.sleep_time = 0.2

        self.arxiv_url = "http://export.arxiv.org/api/query"
        self.ans = []



    def run(self):
        # First formulate a query with the exact match for the title
        # The maxresults in the query are different from the maxresults expected from the plugin.
        params = self.format_query(self.query, self.query_maxresults, split_title = False)
        id_query = ('isbn' in self.query.keys()) or ('arxiv' in self.query.keys())

        ans = self.query_arxiv(params)

        # If no luck, let's try splitting the title by words.
        if len(ans) == 0 and not id_query:
            time.sleep(self.sleep_time)
            params = self.format_query(self.query, self.query_maxresults, split_title = True)
            ans = self.query_arxiv(params)

        if len(ans) > 0:
            self.ans = self.sort_and_trim(ans)
        else:
            self.ans = []



    def query_arxiv(self, params):
        at = "{http://www.w3.org/2005/Atom}"
        query_url = '%s?%s' % (self.arxiv_url, urlencode(params))
        raw = self.browser.open(query_url, timeout=self.timeout).read().strip()
        rawdata = raw.decode('utf-8', errors='replace')
        xmldata = xml.etree.ElementTree.fromstring(rawdata)
        entries = xmldata.findall(at+"entry")

        ans = []
        for result in entries:
            d = {}
            d['arxiv'] = self.format_arxiv_id(result.find(at+'id').text)
            d['title'] = self.format_title(result.find(at+'title').text)
            d['authors'] = [self.format_text(e.text) for e in result.findall(at+'author/'+at+'name')]
            d['subject'] = [self.format_text(e.get('term')) for e in result.findall(at+'category')]
            d['updated'] = self.format_text(result.find(at+'updated').text)
            d['abstract'] = self.format_abstract(result.find(at+'summary').text)
            d['updated'] = self.format_text(result.find(at+'updated').text)
            d['url'] = self.format_url(result.find(at+'link').get('href'))

            ans.append(d)

        return ans



    def format_query(self, d, maxresults, split_title=False):
        """Formats a query suitable to send to the arxiv API"""
        for k in d.keys():
            if not k in self.search_fields:
                raise ArxivError("Error in Arxiv. Don't understand keys")

        if 'arxiv' in d.keys():
            params = {'id_list': d['arxiv'], 'start': '0', 'max_results': '1'}
            return params

        elif 'title' in d.keys() or 'authors' in d.keys():
            items = []
            if 'title' in d.keys():
                if split_title:
                    words = d['title'].split(' ')
                    for b in words: items.append('ti:' + self.format_query_text(b))
                else:
                    items.append('ti:' + ('"%s"' % self.format_query_text(d['title'])))

            if 'authors' in d.keys():
                words = [surname(a) for a in d['authors']]
                for b in words: items.append('au:' + self.format_query_text(b))

            params = {'search_query': " AND ".join(items), 'start': 0, 'max_results': str(maxresults)}
            return params

        else:
            raise ArxivError("Error in Arxiv. Insuficient metadata to construct a query")
            return None


    def format_url(self, url):
        return url


    def format_arxiv_id(self, url):
        m = re.match("http://arxiv.org/abs/(.*)", url)
        return m.group(1).strip()


    def format_abstract(self, abs):
        return self.format_text(abs)


    def format_query_text(self, txt):
        # The wildcard does not work inside "".
        # txt = re.sub('[^\x00-\x7F]', '*', txt)
        # But arxiv does not like non-ascii characters. So I strip accents.
        return strip_accents(txt).strip()
