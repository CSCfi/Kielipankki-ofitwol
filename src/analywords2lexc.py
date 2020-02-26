import sys
import re

mch_set = set()

d = {}
for line_nl in sys.stdin:
    entry, semicol, feats = line_nl.partition(";")
    mch_lst = re.findall(r"{[^}]+}", entry)
    for mch in mch_lst:
        mch_set.add(mch)
    if not entry in d:
        d[entry] = 0
    d[entry] = d[entry] + 1

if mch_set:
    print("Multichar_Symbols")
    mch_lst = sorted(list(mch_set))
    print(" ".join(mch_lst))

print("LEXICON Compounds")

for entry in sorted(d.keys()):
    freq = d[entry]
    weight = 10 / freq
    if freq >= 3:
        print('{} "weight: {:.3f}" ;'.format(entry, weight))
