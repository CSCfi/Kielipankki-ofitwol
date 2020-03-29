import generate
import sys
import re

generate.init("ofi-rules.fst")

for line_nl in sys.stdin:
    line, exclam, comment = line_nl.partition("!")
    line = re.sub(r" +", " ", line)
    entry, space, cont = line.partition(" ")
    entry = entry.replace("_", "{§}")
    if cont.strip() != "/s":
        continue
    if entry.endswith("{ns}{eeØØ}{nØØØ}"):
        stem = entry[:-16] + "s"
    else:
        stem = entry
    nom_set = generate.generate(stem)
    for nom_str in nom_set:
        print(nom_str)
    gen_set = generate.generate(entry + "n")
    for gen_str in gen_set:
        print(gen_str)
