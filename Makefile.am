# version first -- they are parsed LTR and later options depend on automake 1.8
AUTOMAKE_OPTIONS = 1.8 dist-bzip2 no-dist-gzip

ACLOCAL_AMFLAGS = -I m4

SUBDIRS = none bin m4

EXTRA_DIST = nagios-one.spec RELEASE README HACKING

SOURCES = $(top_srcdir)/none/*.py $(top_srcdir)/none/*/*.py

check: pychecker check-python

check-python:
	PYTHONPATH=$(PYTHONPATH):$(top_srcdir) trial none.test

_trial_temp/coverage: $(top_srcdir)/none/*.py $(top_srcdir)/none/*/*.py
	trial --coverage none.test

coverage: _trial_temp/coverage
	python misc/show-coverage.py `ls _trial_temp/coverage/none* | grep -v none.test | grep -v none.extern`

pep8:
	for file in $(SOURCES); do python misc/pep8.py --repeat $$file; done

clean-local:
	@rm -rf _trial_temp

PYCHECKER_WHITELIST = \
	none/*.py \
	none/*/*.py

PYCHECKER_BLACKLIST = \
	none/extern/command/command.py \
	none/extern/log/log.py

release: dist
	make $(PACKAGE)-$(VERSION).tar.bz2.md5

# generate md5 sum files
%.md5: %
	md5sum $< > $@

include $(top_srcdir)/m4/pychecker.mk
