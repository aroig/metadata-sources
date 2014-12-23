#!/usr/bin/env python2
# -*- coding: utf-8 -*-
#
# mathscinet - mathscinet metadata plugin for calibre
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

from xml.sax.saxutils import escape

import time
import re

from .netbib.utils import metadata_distance

from calibre.utils.browser import Browser
from calibre.ebooks.metadata.sources.base import Source, Option
from calibre.ebooks.metadata.book.base import Metadata
from calibre.utils.date import parse_date
from calibre.ebooks.metadata import author_to_author_sort


class MySource(Source):
    options = [Option('clean_title', 'bool', True,
                      _('Clean title'),
                      _('Enable this option clean title metadata and make it "Title Case".'))]

    # Plugin Options
    has_html_comments = True
    supports_gzip_transfer_encoding = False

    # My Options
    idkey = None
    maxresults = 5
    sleep_time = 0.5
    worker_class = None
    abstract_title = None

    def identify(self, log, result_queue, abort, title=None, authors=None,
              identifiers={}, timeout=30):

        md = self.worker_class(self.browser, timeout)

        d = {}
        idval = identifiers.get(self.idkey, None)
        isbn = identifiers.get('isbn', None)

        if idval: d['id'] = idval
        if isbn: d['isbn'] = isbn
        if title: d['title'] = title
        if authors: d['authors'] = authors

        md.query(d, maxresults = self.maxresults)

        while not abort.is_set():
            md.join(0.2)
            if abort.is_set(): break
            if not md.is_alive(): break

        time.sleep(self.sleep_time)

        if not abort.is_set():
            for i in range(0,len(md.ans)):
                mi = self.data2mi(md.ans[i])
                mi.source_relevance = i                # Less means more relevant.

                title = mi.title
                tags = list(mi.tags)
                self.clean_downloaded_metadata(mi)
                mi.tags = tags
                if not self.prefs['clean_title']:      # Keep raw title
                    mi.title = title.strip()

                result_queue.put(mi)
        return None


    def identify_results_keygen(self, title=None, authors=None, identifiers={}):
        """ Returns a key to sort search results. Lesser value means more relevance."""

        query = dict([('title', title), ('authors', authors)] + identifiers.items())

        def mi_distance(mi):
            mifields = dict([('title', mi.title), ('authors', mi.authors)] + mi.identifiers.items())
            return metadata_distance(query, mifields, idkey = self.idkey)

        return mi_distance


    def data2mi(self, item):
        """Converts a single metadata answer in the form of a dict to a MetadataInformation object"""

        mi = Metadata(_('Unknown'))

        # Regular metadata
        mi.title = item.get('title', None)
        mi.authors = item.get('authors', [])
        mi.publisher = item.get('publisher', None)

        if 'id' in item.keys(): mi.set_identifier(self.idkey, item['id'])
        if 'doi' in item.keys(): mi.set_identifier('doi', item['doi'])
        if 'isbn' in item.keys(): mi.set_identifier('isbn', item['isbn'])

        if 'updated' in item.keys(): mi.pubdate = parse_date(item['updated'], assume_utc=True)

        if 'series' in item.keys():
            mi.series = item['series']
            mi.series_index = self.format_series_index(item.get('series_index'), None)

        if 'year' in item.keys(): mi.pubdate = parse_date(item['year'], assume_utc=True)

        if 'abstract' in item.keys(): mi.comments = self.format_abstract(item['abstract'])

        if 'language' in item.keys(): mi.language = item['language']

        if 'journal' in item.keys():
            mi.series = item['journal']
            mi.series_index = self.format_series_index(item.get('volume'), item.get('number'))

        return mi


    def format_abstract(self, abstract):
        return '<h3>%s</h3>\n %s' % (self.abstract_title, abstract)


    def format_paragraph(self, par):
        par = escape(par)
        par = re.sub(r"{\\it(.*?)}", "<i>\g<1></i>", par)
        par = re.sub("\s+", ' ', par)
        return '<p>%s</p>' % par


    def surname(self, au):
        return author_to_author_sort(au).split(',')[0]


    def format_series_index(self, volume, number):
        """Formats a series index of the form 4.03 indicating number 3 in volume 4."""
        v = 0.0
        n = 0.0

        if volume:
            try: v = float(volume)
            except ValueError: v = 0.0

        if number:
            try: n = float(number)
            except ValueError: n = 0.0

        if volume and number:     return v + n/100.
        elif volume:              return v
        elif number:              return n
        else:                     return 0.


# vim: expandtab:shiftwidth=4:tabstop=4:softtabstop=4:textwidth=80
