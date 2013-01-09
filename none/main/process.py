# -*- Mode: Python -*-
# vi:si:et:sw=4:sts=4:ts=4

from none.common import logcommand


class Memory(logcommand.LogCommand):

    summary = "check memory use of process"


class Process(logcommand.LogCommand):

    summary = "process checks"

    subCommandClasses = [Memory, ]
