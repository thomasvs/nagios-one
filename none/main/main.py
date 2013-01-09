# -*- Mode: Python -*-
# vi:si:et:sw=4:sts=4:ts=4

import os
import sys

from none.extern.command import command

from none.common import logcommand, log
from none.main import process

VERSION = '0.0.1'

def main(argv):

    c = Main()
    try:
        ret = c.parse(argv)
    except SystemError, e:
        sys.stderr.write('none: error: %s\n' % e.args)
        return 255
    except ImportError, e:
        # FIXME: decide how to handle
        raise
    except command.CommandError, e:
        sys.stderr.write('none: error: %s\n' % e.output)
        return e.status

    if ret is None:
        return 0

    return ret


class Main(logcommand.LogCommand):
    usage = "%prog %command"
    description = """none or nagios-one is a unified nagios plugin.

none gives you a tree of subcommands to work with.
You can get help on subcommands by using the -h option to the subcommand.
"""

    subCommandClasses = [process.Process, ]

    def addOptions(self):
        log.init()
        log.debug("none", "This is none version %s", VERSION)
        self.parser.add_option('-v', '--version',
                          action="store_true", dest="version",
                          help="show version information")

    def handleOptions(self, options):
        if options.version:
            print "none %s" % VERSION
            sys.exit(0)

    def parse(self, argv):
        log.debug("none", "none %s" % " ".join(argv))
        ret = logcommand.LogCommand.parse(self, argv)
        log.debug("none", "main: returned %r" % ret)
        return ret
