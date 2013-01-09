# -*- Mode: Python -*-
# vi:si:et:sw=4:sts=4:ts=4

import commands

from none.common import logcommand, formatting


class Memory(logcommand.NagiosCommand):

    summary = "check memory use of process"

    def addOptions(self):
        self.parser.add_option('-w', '--warning',
            action="store", dest="warning", default="512M",
            help="Memory to warn at (default %default)")
        self.parser.add_option('-c', '--critical',
            action="store", dest="critical", default="1024M",
            help="Memory to critical at (default %default)")


    def do(self, args):
        command = self.parentCommand.command
        if not command:
            self.unknown('Specify a command to process')

        pids = commands.getoutput("pgrep -f %s | xargs | tr ' ' ','" %
            self.parentCommand.command)

        self.debug('matching pids: %r' % pids)

        highest = commands.getoutput(
            "ps p %s eo pid=,vsz=  | sort -nrk2 | head -n 1" % pids)
        (pid, mem) = highest.split()[:2]

        self.debug('highest pid %s, mem %s KB' % (pid, mem))

        formatted = formatting.formatStorage(float(mem) * 1024)
        msg = "Memory for process %s with PID %s is %s" % (
                command, pid, formatted)

        if float(mem) * 1024 >= formatting.parseStorage(self.options.critical):
            self.critical(msg)
        if float(mem) * 1024 >= formatting.parseStorage(self.options.warning):
            self.warning(msg)
        self.ok(msg)


class Process(logcommand.LogCommand):

    summary = "process checks"

    subCommandClasses = [Memory, ]

    def addOptions(self):
        self.parser.add_option('-c', '--command',
            action="store", dest="command",
            help="command line to select process by")

    def handleOptions(self, options):
        self.command = options.command
