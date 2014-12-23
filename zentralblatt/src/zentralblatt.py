#!/usr/bin/env python2
# -*- coding: utf-8 -*-
#
# zentralblatt - zentralblatt metadata plugin for calibre
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
from .netbib import Zentralblatt

from calibre.ebooks.metadata.sources.base import Option
from calibre.ebooks.metadata.book.base import Metadata


class Zentralblatt(MySource):
    name                    = 'Zentralblatt'
    description             = _('Downloads metadata from Zentralblatt')
    author                  = 'Abdó Roig-Maranges'
    supported_platforms     = ['windows', 'osx', 'linux']
    version                 = (1,3,0)
    minimum_calibre_version = (0,8,0)

    capabilities = frozenset(['identify'])
    touched_fields = frozenset(['title', 'authors', 'identifier:zbl', 'comments', 'publisher',
                                'pubdate', 'languages', 'series', 'series_index', 'tags'])

    # Plugin Options
    has_html_comments = True
    supports_gzip_transfer_encoding = False

    # My Options
    idkey = 'zbl'
    maxresults = 5
    sleep_time = 0.5
    worker_class = Zentralblatt
    abstract_title = "Zentralblatt Review:"


    def get_book_url(self, identifiers):
        """Produces an url for the zbl identifier. The others are known."""
        if 'zbl' in identifiers.keys():
            zbl = identifiers['zbl']
            url = "https://zbmath.org?q=an:%s" % zbl
            return ("zbl", zbl, url)
        else:
            return None



# vim: expandtab:shiftwidth=4:tabstop=4:softtabstop=4:textwidth=80
