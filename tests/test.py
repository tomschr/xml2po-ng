#!/usr/bin/env python
import sys, os, time

SIMPLETESTS = { 'deep-finals.xml' : {},
                'deep-nonfinals.xml': {},
                'attribute-entities.xml': {},
                'docbook.xml' : {},
                'mallard.xml' : {'options': '-m mallard' },
                'utf8-original.xml': {},
                'footnotes.xml': {},
                'keepents.xml': { "options" : "-k" },
                'adjacent-ents.xml': { "options" : "-k" },
                'ubuntu-mode.xml': { "options" : "-m ubuntu -k -l sr" },
                'xhtml.xml': { "options" : "-m xhtml" },
                }

OTHERTESTS = [ ('relnotes', 'test.sh') ]

if len(sys.argv) > 1:
    input = sys.argv[1]
    pot = input.replace(".xml", ".pot")
    po = input.replace(".xml", ".po")
    myopts = ""
    if len(sys.argv) > 2:
        for opt in sys.argv[2:]:
            myopts += " " + opt
    output = input.replace(".xml", ".xml.out")
    fullcommand = "../xml2po/xml2po %s %s | sed 's/\"POT-Creation-Date: .*$/\"POT-Creation-Date: \\\\n\"/' | diff -u %s -" % (myopts, input, pot)
    #print >>sys.stderr, fullcommand
    ret = os.system(fullcommand)
    if ret:
        print "Problem: extraction from '%s'" % (input)
    fullcommand = "../xml2po/xml2po -p %s %s %s | diff -u %s -" % (po, myopts, input, output)
    #print >>sys.stderr, fullcommand
    ret = os.system(fullcommand)
    if ret:
        print "Problem: merging translation into '%s'" % (input)
else:
    time_start = time.time()
    for t in SIMPLETESTS:
        myopts = SIMPLETESTS[t].get("options", "")
        if os.system("%s %s %s" % (sys.argv[0], t, myopts)):
            print "WARNING: Test %s failed." % (t)

    for t in OTHERTESTS:
        if os.system("cd %s && ./%s" % (t[0], t[1])):
            print "WARNING: Test %s failed." % (t[0])
    time_end = time.time()
    print "%d tests executed in %2.2f secs" % (len(SIMPLETESTS)+len(OTHERTESTS), time_end-time_start)
