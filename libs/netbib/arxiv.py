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

        self.search_fields = ['title', 'authors', 'id']
        self.idkey = 'arxiv'

        self.timeout = timeout
        self.browser = browser
        self.sleep_time = 0.2

        self.arxiv_url = "http://export.arxiv.org/api/query"
        self.ans = []



    # Internals
    # ------------------------------ #

    def get_matches(self, params):
        at = "{http://www.w3.org/2005/Atom}"
        query_url = '%s?%s' % (self.arxiv_url, urlencode(params))
        raw = self.browser.open(query_url, timeout=self.timeout).read().strip()
        rawdata = raw.decode('utf-8', errors='replace')
        xmldata = xml.etree.ElementTree.fromstring(rawdata)
        entries = xmldata.findall(at+"entry")

        ans = []
        for result in entries:
            d = {}
            d['id'] = self.format_id(result.find(at+'id').text)
            d['title'] = self.format_title(result.find(at+'title').text)
            d['authors'] = [self.format_text(e.text) for e in result.findall(at+'author/'+at+'name')]
            d['subject'] = [self.format_text(e.get('term')) for e in result.findall(at+'category')]
            d['updated'] = self.format_text(result.find(at+'updated').text)
            d['abstract'] = self.format_text(result.find(at+'summary').text)
            d['updated'] = self.format_text(result.find(at+'updated').text)
            d['url'] = self.format_url(result.find(at+'link').get('href'))

            ans.append(d)

        return ans


    def get_item(self, bibid):
        params = self.format_query({'id': bibid})
        ans = self.get_matches(params)

        if len(ans) > 0:
            return ans[0]

        return None


    def get_abstract(self, bibid):
        ans = self.get_item(bibid)

        if 'abstract' in ans:
            return ans['abstract']

        return None


    def format_query(self, d, lax=False):
        """Formats a query suitable to send to the arxiv API"""
        for k in d.keys():
            if not k in self.search_fields:
                raise ArxivError("Error in Arxiv. Don't understand key: %s" % k)

        if 'id' in d.keys():
            params = {'id_list': d['id'], 'start': '0', 'max_results': '1'}
            return params

        elif 'title' in d.keys() or 'authors' in d.keys():
            items = []
            if 'title' in d.keys():
                if lax:
                    words = d['title'].split(' ')
                    for b in words: items.append('ti:' + self.clean_query(b))
                else:
                    items.append('ti:' + ('"%s"' % self.clean_query(d['title'])))

            if 'authors' in d.keys():
                words = [surname(a) for a in d['authors']]
                for b in words: items.append('au:' + self.clean_query(b))

            params = {'search_query': " AND ".join(items),
                      'start': 0,
                      'max_results': str(self.query_maxresults)}
            return params

        else:
            raise ArxivError("Error in Arxiv. Insuficient metadata to construct a query")
            return None



    # Utility stuff
    # ------------------------------ #

    def format_id(self, url):
        m = re.match("http://arxiv.org/abs/(.*)", url)
        return m.group(1).strip()
