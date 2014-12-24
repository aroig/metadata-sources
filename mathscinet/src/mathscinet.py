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

import time
import re

from .mysource import MySource
from .tags import msc_tags
from .netbib import Mathscinet as MathscinetWorker

from calibre.ebooks.metadata.sources.base import Option
from calibre.ebooks.metadata.book.base import Metadata

class Mathscinet(MySource):
    name                    = 'Mathscinet'
    description             = _('Downloads metadata from Mathscinet')
    author                  = 'Abdó Roig-Maranges'
    supported_platforms     = ['windows', 'osx', 'linux']
    version                 = (1,3,0)
    minimum_calibre_version = (1,0,0)

    capabilities = frozenset(['identify'])
    touched_fields = frozenset(['title', 'authors', 'identifier:mr', 'comments', 'publisher',
                                'languages', 'pubdate', 'series', 'series_index', 'tags'])


    # Plugin Options
    has_html_comments = True
    supports_gzip_transfer_encoding = False

    # My Options
    idkey = 'mr'
    maxresults = 5
    sleep_time = 0.5
    worker_class = MathscinetWorker
    abstract_title = "Mathscinet Review:"


    def get_book_url(self, identifiers):
        """Produces an url for the mr identifier."""
        if 'mr' in identifiers.keys():
            mr = identifiers['mr']
            url = "http://www.ams.org/mathscinet/search/publdoc.html?pg1=MR&s1=%s" % mr
            return ("mr", mr, url)
        else:
            return None


    def data2mi(self, item):
        mi = super(Mathscinet, self).data2mi(item)

        if 'subject' in item.keys():
            tags = set([])
            for s in item['subject']:
                tags.update(msc_tags(s))
            mi.set('tags', tags)

        return mi



# vim: expandtab:shiftwidth=4:tabstop=4:softtabstop=4:textwidth=80
