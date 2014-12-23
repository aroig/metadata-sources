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
import time
from .utils import metadata_distance, strip_accents
from .latex_encoding import latex_decode



class NetbibError(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)



class NetbibBase(threading.Thread):
    def __init__(self):
        super(NetbibBase, self).__init__()

        self.lang_map = {
            'english': 'eng',
            'german': 'deu',
            'french': 'fra',
            'spanish': 'spa',
            'italian': 'ita',
        }



    # Public interface
    # ------------------------------ #

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




    # Internals
    # ------------------------------ #

    def run(self):
        """Runs the query thread"""
        ans = []

        # check if querying by id
        if 'id' in self.query:
            item = self.get_item(self.query['id'])
            if item:
                # get abstract
                if not 'abstract' in item:
                    abstract = self.get_abstract(item['id'])
                    if abstract:
                        time.sleep(self.sleep_time)
                        item['abstract'] = abstract

                ans.append(item)

        else:
            # First run with authors as authors.
            params = self.format_query(self.query, lax=False)
            ans = self.get_matches(params)

            # If no luck, try searching for the title words anywhere
            if len(ans) == 0:
                time.sleep(self.sleep_time)
                params = self.format_query(self.query, lax=True)
                ans = self.get_matches(params)

            # TODO: do more attempts?

        if len(ans) > 0:
            ans = self.sort_and_trim(ans)

        self.ans = ans


    def format_query(self, query, lax=False):
        """Formats the parameters for a query"""
        raise NotImplementedError


    def get_matches(self, params):
        """Returns the answer to a query"""
        raise NotImplementedError


    def get_item(self, bibid):
        """Returns an item by id"""
        raise NotImplementedError


    def get_abstract(self, bibid):
        """Returns the answer to a query"""
        raise NotImplementedError



    # Utility stuff
    # ------------------------------ #

    def format_url(self, url):
        return url.strip()


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


    def format_type(self, txt):
        return txt.strip().lower()


    def format_journal(self, txt):
        """Strip stuff in parenthesis"""
        txt = self.format_text(txt)
        txt = re.sub("{([^{}]*?)}", "\g<1>", txt, re.DOTALL)  # Removes more {}
        txt = re.sub("\(.*$", "", txt, re.DOTALL)             # Kill after first parenthesis.
        return txt.strip()


    def format_publisher(self, txt):
        txt = self.format_text(txt)
        txt = re.sub("{([^{}]*?)}", "\g<1>", txt, re.DOTALL)  # Removes more {}
        txt = re.sub("(\(|,|\.).*$", "", txt, re.DOTALL)      # Kill after first comma or parenthesis.
        return txt.strip()


    def format_number(self, vol):
        """Format volume number"""
        return vol.strip()


    def format_language(self, lang):
        """Format language string"""
        lang = lang.lower().strip()
        if lang in self.lang_map:
            return self.lang_map[lang]
        else:
            return None


    def format_doi(self, doi):
        """Format doi"""
        return doi.strip()


    def format_isbn(self, isbn):
        """Format an isbn"""
        return isbn.replace('-', '').strip()


    def format_id(self, bibid):
        """Format the id"""
        return self.format_text(bibid)


    def clean_query(self, txt):
        """Strip accents and such, to make a query"""
        return strip_accents(txt).strip()


    def sort_and_trim(self, ans):
        """Sort results according to relevance and trim to max results."""

        def sort_key(d):
            return metadata_distance(d, self.query, self.idkey)

        ans.sort(key = sort_key)
        return ans[:self.maxresults]


    def entry_from_bibtex(self, bib):
        """Extract information from a bibtex entry"""

        d = {}

        if 'bibtextype' in bib.keys():
            d['type'] = self.format_type(bib['bibtextype'])

        if 'title' in bib.keys():
            d['title'] = self.format_title(bib['title'])

        if 'author' in bib.keys():
            d['authors'] = [self.format_author(e)
                            for e in bib['author'].split('and')]
        elif 'editor' in bib.keys():
            d['authors'] = [self.format_author(e)
                            for e in bib['editor'].split('and')]

        if 'language' in bib.keys():
            lang =  self.format_language(bib['language'])
            if lang: d['language'] = lang

        if 'doi' in bib.keys():
            d['doi'] = self.format_doi(bib['doi'])

        if 'isbn' in bib.keys():
            d['isbn'] = self.format_isbn(bib['isbn'])

        if 'publisher' in bib.keys():
            d['publisher'] = self.format_publisher(bib['publisher'])

        if 'series' in bib.keys():
            d['series'] = self.format_text(bib['series'])
            if 'volume' in bib.keys():
                d['series_index'] = self.format_number(bib['volume'])

        if 'fjournal' in bib.keys():
            d['journal'] = self.format_journal(bib['fjournal'])
        elif 'journal' in bib.keys():
            d['journal'] = self.format_text(bib['journal'])

        if 'volume' in bib.keys():
            d['volume'] = self.format_number(bib['volume'])

        if 'number' in bib.keys():
            d['number'] = self.format_number(bib['number'])

        if 'year' in bib.keys():
            year = self.format_year(bib['year'])
            if year: d['year'] = year

        if 'abstract' in bib.keys():
            d['abstract'] = latex_decode(bib['abstract'].strip())

        return d
