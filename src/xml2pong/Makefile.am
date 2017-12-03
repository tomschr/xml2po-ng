SUBDIRS = modes

xml2podir = $(pythondir)/xml2po

nodist_bin_SCRIPTS = xml2po
CLEANFILES = xml2po

xml2po: xml2po.py.in
	$(AM_V_GEN)sed -e "s/^VERSION =.*/VERSION = \"@VERSION@\"/" \
	    -e "s+^#!.*python.*+#!$(PYTHON)+" \
	  < $(srcdir)/xml2po.py.in > xml2po
	$(AM_V_at)chmod +x xml2po

xml2po_PYTHON = \
	__init__.py

EXTRA_DIST = \
	xml2po.py.in
