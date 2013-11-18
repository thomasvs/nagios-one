# -*- Mode: Python -*-
# vi:si:et:sw=4:sts=4:ts=4

import os

from none.common import logcommand, formatting, process


class _Memory(logcommand.NagiosCommand):

    processAttr = None
    label = None

    def addOptions(self):
        self.parser.add_option('-w', '--warning',
            action="store", dest="warning", default="512M",
            help="Memory to warn at (default %default)")
        self.parser.add_option('-c', '--critical',
            action="store", dest="critical", default="1024M",
            help="Memory to critical at (default %default)")

        self.parser.add_option('-M', '--maximum',
            action="store", dest="maximum", default="4G",
            help="Maximum memory for performance data (default %default)")

    def do(self, args):
        command = self.parentCommand.command
        selecter = process.commandSelecterFactory(prefix=command)
        pidDict = process.getProcesses(selecter=selecter)

        self.debug('matching pids: %r' % pidDict.keys())

        vsizes = pidDict.items()
        vsizes.sort(cmp=lambda x, y:
            getattr(x[1], self.processAttr) < getattr(y[1], self.processAttr))

        if not vsizes:
            self.critical("No processes found with command %s" % command)
        highest = vsizes[-1]
        (pid, proc) = highest
        mem = self.toBytes(getattr(proc, self.processAttr))

        self.info('Highest pid is %s, memory %s bytes' % (pid, mem))

        formatted = formatting.formatStorage(float(mem))
        msg = "Memory for process %s with PID %s is %s" % (
                command, pid, formatted)

        msg += '|' + "%s=%d;%d;%d;0;%d" % (
            self.label,
            int(mem),
            formatting.parseStorage(self.options.warning),
            formatting.parseStorage(self.options.critical),
            formatting.parseStorage(self.options.maximum))

        if float(mem) >= formatting.parseStorage(self.options.critical):
            self.critical(msg)
        if float(mem) >= formatting.parseStorage(self.options.warning):
            self.warning(msg)
        self.ok(msg)

    def toBytes(self, value):
        return value

class VSize(_Memory):

    processAttr = 'vsize'
    label = 'memory'

# temporary compatibility
Memory = VSize

class RSS(_Memory):

    """
    Checks the matching process with the highest RSS memory.
    """

    processAttr = 'rss'
    label = 'rss'

    def toBytes(self, value):
        # in pages
        return value * os.sysconf('SC_PAGESIZE')


class Process(logcommand.LogCommand):

    summary = "process checks"

    subCommandClasses = [Memory, RSS, VSize]

    def addOptions(self):
        self.parser.add_option('-c', '--command',
            action="store", dest="command",
            help="command line to select process by")

    def handleOptions(self, options):
        self.command = options.command

        if not self.command:
            self.unknown('Specify a command to check process status of')
