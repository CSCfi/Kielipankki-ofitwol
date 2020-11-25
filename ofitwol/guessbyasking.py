# guessbyasking.py

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

import hfst
import sys
import re
import argparse

argparser = argparse.ArgumentParser(
    "python3 gyessbyasking.py",
    description="Guess lexicon entries by asking forms from the user")
argparser.add_argument(
    "guesser", help="Guesser file FST", default="finv-guess.fst")
argparser.add_argument(
    "-r", "--reject", default=1000000, type=int,
    help="reject candidates which are worse than the best by REJECTION or more")
argparser.add_argument(
    "-v", "--verbosity", default=0, type=int,
    help="level of diagnostic output")
args = argparser.parse_args()

guesser_fil = hfst.HfstInputStream(args.guesser)
guesser_fst = guesser_fil.read()
guesser_fil.close()

print("\nENTER FORMS OF A WORD:\n")
while True:
    remaining_set = set()
    weights = {}                 # weights[entry] == weight
    first = True
    while True:
        linenl = sys.stdin.readline()
        if not linenl: exit()
        line = linenl.strip()
        if line in {"", "0"} :
            print("GIVING UP THIS WORD\n\n")
            break
        if re.match("[1-9][0-9]*", line):
            e = remaining_lst[int(line)-1]
            print("\n" + "="*len(e))
            print(e)
            print("="*len(e) + "\n")
            break
        if line[0] == '-':
            res = guesser_fst.lookup(line[1:], output="tuple")
        else:
            res = guesser_fst.lookup(line, output="tuple")
        if args.verbosity >= 10:
            print("lookup result =", res)
        if len(res) == 0:
            print("FITS NO PATTERN! INGORED.")
            continue
        entries = set()
        for entry_and_feats, w in res:
            entry, semicol, feats = entry_and_feats.partition(";")
            entries.add(entry)
            if entry in weights:
                weights[entry] = min(w, weights[entry])
            else:
                weights[entry] = w
        if first:
            first = False
            new_remaining_set = entries
        elif line[0] == '-':
            new_remaining_set = remaining_set - entries
        else:
            new_remaining_set = remaining_set & entries
        best_weight = min([weights[e] for e in new_remaining_set], default=0)
        remaining_lst = []
        for e in new_remaining_set:
            if weights[e] <= best_weight + args.reject:
                remaining_lst.append(e)
        remaining_lst.sort(key = lambda e : weights[e])
        if len(remaining_lst) == 1:
            e = remaining_lst[0]
            print("\n" + "="*len(e))
            print(e)
            print("="*len(e) + "\n")
            break
        elif not remaining_lst:
            print("DOES NOT FIT! IGNORED.")
        else:
            i = 0
            for entry in remaining_lst:
                i += 1
                w = weights[entry]
                print("    ({}) {}  {}".format(i, entry, w))
            remaining_set = set(remaining_lst)



