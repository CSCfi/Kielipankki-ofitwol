"""Reads a table which defines the symbols that are used in a two-level morphological analyser.
The table is in CSV form, and this script produces (1) a snippet for the LEXC file which contains 
the morphophonemes that will be used in the entries of the lexicon, and (2) a file which contains 
the morphophonemes and their realisations as pairs quoted with % signs as the TWOLC requires.

Copyright (C) 2016 Kimmo Koskenniemi
This is free software according to GPL 3, see <http://www.gnu.org/licenses/>"""

import sys, csv, re

rdr = csv.DictReader(sys.stdin, delimiter=',')
lexcF = open("morphophonemes.lexc", mode='w')
rulF = open("alpha.twolc", mode='w')
#exaF = open("test.m2s.pstr", mode='w')
for r in rdr:
    l = r['LEXICAL']
    print(" %s" % l, end=' ', file=lexcF)
    ex = r['EXAMPLES']
    #print(ex, file=exaF)
    for s in re.split(" +", r['SURFACE']):
        ll = re.sub(r"([{}_&-\<=>])", r"%\1", l)
        print(" %s:%s" % (ll, s),  end='', file=rulF)
    print(file=rulF)
print(file=lexcF)
