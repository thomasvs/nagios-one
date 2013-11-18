# -*- Mode: Python; test-case-name: none.test.test_common_process -*-
# vi:si:et:sw=4:sts=4:ts=4

from twisted.trial import unittest

from none.common import process


class ProcessTestCase(unittest.TestCase):

    def test_systemd(self):
        LINE = '1 (systemd) S 0 1 1 0 -1 4219136 39367 53337166 889 127551 53 449 2828478 602173 20 0 1 0 1 54607872 475 18446744073709551615 1 1 0 0 0 0 671173123 4096 1260 18446744073709551615 0 0 17 1 0 0 1566 0 1353199 0 0 0 0 0 0 0 0\n'

        p = process.Process(1, LINE)
        self.assertEquals(p.cmd, 'systemd')
        self.assertEquals(p.rss, 1)

    def test_with_space(self):
        LINE = '1443 (Plex Media Serv) S 1 1443 1443 0 -1 1077960960 21447 41160 1519 2782 1054 1049 15211 3124 20 0 14 0 3065 1704644608 1420 18446744073709551615 1 1 0 0 0 0 0 0 87279 18446744073709551615 0 0 17 2 0 0 20 0 0 0 0 0 0 0 0 0 0'

        p = process.Process(1443, LINE)
        self.assertEquals(p.cmd, 'Plex Media Serv')
        self.assertEquals(p.rss, 1)
