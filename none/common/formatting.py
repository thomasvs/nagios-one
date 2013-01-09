# -*- Mode: Python -*-
# vi:si:et:sw=4:sts=4:ts=4

# This file may be distributed and/or modified under the terms of
# the GNU Lesser General Public License version 2.1 as published by
# the Free Software Foundation.
# This file is distributed without any warranty; without even the implied
# warranty of merchantability or fitness for a particular purpose.
# See "LICENSE.LGPL" in the source distribution for more information.
#
# Headers in this file shall remain intact.

# selected from flumotion.common.formatting and flumotion.monitor.nagios.process

"""formatting functions for storage, time, etc
"""

import gettext
import locale
import sys
import time

def formatStorage(units, precision=2):
    """
    Nicely formats a storage size using SI units.
    See Wikipedia and other sources for rationale.
    Prefixes are k, M, G, ...
    Sizes are powers of 10.
    Actual result should be suffixed with bit or byte, not b or B.

    @param units:     the unit size to format
    @type  units:     int or float
    @param precision: the number of floating point digits to use
    @type  precision: int

    @rtype: string
    @returns: value of units, formatted using SI scale and the given precision
    """

    # XXX: We might end up calling float(), which breaks
    #      when using LC_NUMERIC when it is not C -- only in python
    #      2.3 though, no prob in 2.4. See PEP 331
    if sys.version_info < (2, 4):
        locale.setlocale(locale.LC_NUMERIC, "C")

    prefixes = ['E', 'P', 'T', 'G', 'M', 'k', '']

    value = float(units)
    prefix = prefixes.pop()
    while prefixes and value >= 1000:
        prefix = prefixes.pop()
        value /= 1000

    formatString = "%%.%df %%s" % precision
    return formatString % (value, prefix)


def parseStorage(size):
    """
    Given a size string, convert to an int in base unit.
    suffixes are interpreted in SI, as multiples of 1000, not 1024.
    Opposite of L{formatStorage}

    @rtype: int
    """
    if len(size) == 0:
        return 0

    suffixes = ['E', 'P', 'T', 'G', 'M', 'k']

    suffix = size[-1]

    if suffix not in suffixes:
        raise KeyError(
            'suffix %c not in accepted list of suffixes %r' % (
            suffix, suffixes))

    i = suffixes.index(suffix)
    power = (len(suffixes) - i) * 3
    multiplier = 10 ** power

    return int(float(size[:-1]) * multiplier)
