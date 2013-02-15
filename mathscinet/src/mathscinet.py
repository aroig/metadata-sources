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
from .netbib import Mathscinet

from calibre.ebooks.metadata.sources.base import Option
from calibre.ebooks.metadata.book.base import Metadata

class Mathscinet(MySource):
    name                    = 'Mathscinet'
    description             = _('Downloads metadata from Mathscinet')
    author                  = 'Abdó Roig-Maranges'
    supported_platforms     = ['windows', 'osx', 'linux']
    version                 = (1,2,0)
    minimum_calibre_version = (0,8,0)

    capabilities = frozenset(['identify'])
    touched_fields = frozenset(['title', 'authors', 'identifiers', 'comments',
                                'publisher', 'pubdate', 'series', 'series_index'])


    # Plugin Options
    has_html_comments = True
    supports_gzip_transfer_encoding = False

    # My Options
    idkey = 'mr'
    maxresults = 5
    sleep_time = 0.5
    worker_class = Mathscinet
    abstract_title = "Mathscinet Review:"


    def get_book_url(self, identifiers):
        """Produces an url for the mr identifier."""
        if 'mr' in identifiers.keys():
            mr = identifiers['mr']
            url = "http://www.ams.org/mathscinet/search/publdoc.html?pg1=MR&s1=%s" % mr
            return ("mr", mr, url)
        else:
            return None


# vim: expandtab:shiftwidth=4:tabstop=4:softtabstop=4:textwidth=80
