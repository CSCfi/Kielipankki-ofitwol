# guessbygenerating.py

copyright = """Copyright © 2017, Kimmo Koskenniemi

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or (at
your option) any later version.

This program is distributed in the hope that it will be useful, but
WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

import hfst, sys, argparse

argparser = argparse.ArgumentParser(
    "python3 gyessbygenerating.py",
    description="Guess lexicon entries from generated forms of them")
argparser.add_argument(
    "-g", "--guesser",
    help="Guesser file FST", ### default="ofi-guess-n.fst",
    default="guess/guess-analy.ofst")
argparser.add_argument(
    "-r", "--rules", 
    help="name of the two-level rule file",
    default="ofi-rules.fst")
argparser.add_argument(
    "-v", "--verbosity", default=0, type=int,
    help="level of diagnostic output")
args = argparser.parse_args()

guesser_fil = hfst.HfstInputStream(args.guesser)
guesser_fst = guesser_fil.read()
guesser_fil.close()

import sys, re
import generate

generate.init(args.rules)

suf = {
    "/s": ["", "n", "{nrs}{aä}", "{ij}{Øt}{aä}"],
    "/v": ["{dlnrtØ}{aä}", "n", "{i}{VØ}", "isi",
           "{C}", "{nlrs}{uy}{tØthn}{ØeØØØ}"],
    "/a": ["", "n", "{nrs}{aä}", "{ij}{Øt}{aä}", "m{pm}i"]
}

print()
for line_nl in sys.stdin:
    line = line_nl.strip()
    res_str = guesser_fst.lookup(line, output="text")
    if args.verbosity >= 10:
        print("lookup res_str =", res_str)
    res_lst = res_str.split("\n")
    stem_cont_weight_lst = []
    entry_set = set()
    for res in res_lst:
        if not res.strip():
            continue
        if args.verbosity >= 10:
            print("res =", res)
        entry_feat, weight_str = res.split("\t")
        entry, semicolon, feat = entry_feat.partition(";")
        if entry in entry_set:
            continue
        else:
            entry_set.add(entry)
        stem, space, cont = entry.partition(" ")
        weight = float(weight_str.strip())
        stem_cont_weight_lst.append((stem.strip(), cont.strip(), weight))
    if not stem_cont_weight_lst:
        print("** NO GUESSES")
        continue
    if args.verbosity >= 10:
        print("lookup stem_cont_weight_lst =", stem_cont_weight_lst)
    best_w = min([weight for stem, cont, weight in stem_cont_weight_lst])

    i = 0
    for [stem, cont, weight] in stem_cont_weight_lst:
        i += 1
        suffix_lst = suf.get(cont, "")
        word_lst = []
        for suffix in suffix_lst:
            generated_words = generate.generate(stem+suffix)
            for word in generated_words:
                word = word.replace("Ø", "")
                word_lst.append(word)
        print("{}:".format(i), " ".join(word_lst))
        print("            {} {} ; {:6.2f}".format(stem, cont, weight))
    print()
