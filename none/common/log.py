# -*- Mode: Python -*-
# vi:si:et:sw=4:sts=4:ts=4

# Copyright (C) 2013 Thomas Vander Stichele

# This file is part of none.
#
# none is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# none is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with none.  If not, see <http://www.gnu.org/licenses/>.

"""
Logging
"""

from none.extern.log import log as externlog
from none.extern.log.log import *


def init():
    externlog.init('NONE_DEBUG')
    externlog.setPackageScrubList('none')
