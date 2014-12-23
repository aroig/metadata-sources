#!/usr/bin/env python2
# -*- coding: utf-8 -*-
#
# arxiv - arxiv plugin for calibre
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

import time
import re

from .mysource import MySource
from .netbib.arxiv import Arxiv
from .tags import arxiv_tags

from calibre.ebooks.metadata.sources.base import Option
from calibre.ebooks.metadata.book.base import Metadata


class Arxiv(MySource):
    name                    = 'Arxiv'
    description             = _('Downloads metadata from arxiv.org')
    author                  = 'Abdó Roig-Maranges'
    supported_platforms     = ['windows', 'osx', 'linux']
    version                 = (1,2,0)
    minimum_calibre_version = (0,8,0)

    capabilities = frozenset(['identify'])
    touched_fields = frozenset(['title', 'authors', 'identifier:arxiv', 'comments',
                                'publisher', 'pubdate', 'tags'])

    options = MySource.options + \
        [Option("publisher", "string", "arxiv.org",
                _("Publisher"),
                _("Sets the publisher to this value")),
         ]

    # Plugin Options
    supports_gzip_transfer_encoding = False
    has_html_comments = True

    # My Options
    idkey = 'arxiv'
    maxresults = 10
    sleep_time = 0.5
    worker_class = Arxiv
    abstract_title = "Abstract:"



    def data2mi(self, item):
        mi = super(Arxiv, self).data2mi(item)

        publisher = self.prefs['publisher'].strip()
        if publisher != "":
            mi.publisher = publisher

        if 'subject' in item.keys():
            tags = set([])
            for s in item['subject']:    tags = tags.union(arxiv_tags.get(s, []))
            mi.set('tags', tags)

        return mi


# vim: expandtab:shiftwidth=4:tabstop=4:softtabstop=4:textwidth=80
