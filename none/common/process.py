# -*- Mode: Python; test-case-name: none.test.test_common_process -*-
# vi:si:et:sw=4:sts=4:ts=4

import os
import re

from none.common import log

# example:
# 1 (systemd) S 0 1 1 0 -1 4219136 39364 53335146 889 127526 53 449 2828476 602170 20 0 1 0 1 54607872 475 18446744073709551615 1 1 0 0 0 0 671173123 4096 1260 18446744073709551615 0 0 17 1 0 0 1566 0 1353199 0 0 0 0 0 0 0 0

_STAT_RE = re.compile(r"""
    ^
    (?P<pid>\d+)     # pid
    \s+
    \((?P<cmd>.*)\)  # command, between parentheses
    (?P<fields>.*)   # a bunch of integer fields
    $
    """, re.VERBOSE)

class Process(log.Loggable):
    """
    I hold information about a process with a given pid based on information in
    /proc/(pid)/stat.  See man proc for more info.

    @ivar  pid:     the PID of the process
    @type  pid:     int
    @ivar  cmdline: the command line arguments for this process
    @type  cmdline: list of str
    @ivar  vsize:   virtual memory size in bytes
    @type  vsize:   int
    @ivar  rss:     number of pages in real memory, minus 3.
    @type  rss:     int
    """

    def __init__(self, pid, line=None):
        if not line:
            handle = open('/proc/%d/stat' % pid)
            line = handle.read()

        # see man proc
        m = _STAT_RE.search(line)
        if not m:
            raise IndexError, "Cannot parse stat line %r" % (line, )

        assert pid == int(m.group('pid'))

        fields = m.group('fields').split()
        self.debug('fields for process [%05d]: %r' % (pid, fields))
        self.pid = pid
        self.cmd = m.group('cmd')
        self.ppid = int(fields[3])
        self.vsize = int(fields[22])
        self.rss = int(fields[23])

        handle = open('/proc/%d/cmdline' % pid)
        line = handle.read()
        bits = line.split('\0')
        self.cmdline = bits

    def __repr__(self):
        return '<process %d: %s>' % (self.pid, self.cmd)

# FIXME: create a way to map pid's to Process subclasses if wanted
class ProcessFactory:
    """
    I create a Process instance or subclass.
    """

    def process(self, pid):
        """
        @rtype: L{Process} instance
        """
        # this is a factory function, so suppress inconsistent return value
        # warnings
        __pychecker__ = '--no-returnvalues'

        return Process(pid)

def commandSelecterFactory(prefix):
    def selecter(p):
        return p.cmd.startswith(prefix)
    return selecter

def getProcesses(selecter=None):
    """
    Get all running processes whose command starts with the given prefix.

    Note: since we use the /proc interface, only the first 15 characters can
    actually be matched. (FIXME: this might not be the case on other OS/Linux
    versions)

    @rtype:   dict of int -> Process
    @returns: a dict of pid -> process
    """
    factory = ProcessFactory()
    procs = {}

    for entry in os.listdir('/proc'):
        try:
            pid = int(entry)
        except ValueError:
            continue

        p = factory.process(pid)
        if selecter:
            if not selecter(p):
                continue
        procs[pid] = p

    return procs

