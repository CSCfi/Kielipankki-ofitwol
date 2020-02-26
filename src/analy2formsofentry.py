import sys
d = {}
for line_nl in sys.stdin:
    lst = line_nl.strip().split("\t")
    if len(lst) == 3:
        [word, analysis, weight_str] = lst
        if weight_str == "inf":
            continue
        weight = float(weight_str.replace(",", "."))
    elif len(lst) == 2:
        [word, analysis] = lst
        weight = 0.0
    else:
        continue
    if weight > 10:
        continue
    entry = analysis.split(sep="+", maxsplit=1)[0]
    if entry in d:
        d[entry].append(word)
    else:
        d[entry] = [word]

for entry in sorted(d.keys()):
    print("{}\t{}".format(entry, " ".join(d[entry])))
