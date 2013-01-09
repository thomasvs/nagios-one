dnl initialize autoconf
dnl when going to/from release please remove/add the nano (fourth number)
dnl releases only do Wall, trunk and prerelease does Werror too
AC_INIT(nagios-one, 0.0.0.1,
   ,
   nagios-one)

dnl initialize automake
AM_INIT_AUTOMAKE

dnl define PACKAGE_VERSION_* variables
AS_VERSION

AS_NANO

dnl authors
AC_SUBST_FILE(AUTHORS)
AUTHORS=$srcdir/AUTHORS

dnl AM_MAINTAINER_MODE only provides the option to configure to enable it
AM_MAINTAINER_MODE

dnl Add parameters for aclocal
AC_SUBST(ACLOCAL_AMFLAGS, "-I m4")

dnl check for python
AS_PATH_PYTHON(2.3)

dnl check for where to install our python stuff
PYVER=[`$PYTHON -c "import sys ; print sys.version[:3]"`]

dnl This is the best way of installing in an arch-independent location for now
AS_AC_EXPAND(PYTHONLIBDIR, "\${exec_prefix}/lib/python$PYVER/site-packages")

AC_MSG_NOTICE(Installing python code in $PYTHONLIBDIR)
AC_SUBST(PYTHONLIBDIR)

AS_AC_EXPAND(NAGIOSPLUGINSDIR, "\${libexecdir}/nagios/plugins")
AC_MSG_NOTICE(Installing nagios plugin in $NAGIOSPLUGINSDIR)
AC_SUBST(NAGIOSPLUGINSDIR)

dnl check for epydoc
AC_CHECK_PROG(EPYDOC, epydoc, yes, no)
AM_CONDITIONAL(HAVE_EPYDOC, test "x$EPYDOC" = "xyes")

dnl check for pychecker
AC_CHECK_PROG(PYCHECKER, pychecker, yes, no)
AM_CONDITIONAL(HAVE_PYCHECKER, test "x$PYCHECKER" = "xyes")

dnl output stuff
AC_CONFIG_FILES([bin/none], [chmod +x bin/none])

AC_OUTPUT(
Makefile
bin/Makefile
m4/Makefile
none/Makefile
none/main/Makefile
none/common/Makefile
none/extern/Makefile
nagios-one.spec
)
