# entryharvester.py

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

argparser = argparse.ArgumentParser("python3 entryharvester.py",
                                    description="Extracts lexicon entries from corpus data")
argparser.add_argument(
    "guesser_fst",
    default="guess.fst",
    help="An optimized FST that transforms a word form into a set of guessed entries")
argparser.add_argument(
    "word_forms",
    default="words.fst",
    help="The word forms one word form per line")
argparser.add_argument(
    "-m", "--minimum_forms",
    type=int, default=8,
    help="minimum number of froms")
argparser.add_argument(
    "-v", "--verbosity",
    type=int, default=0,
    help="level of debugging info printed")
args = argparser.parse_args()

guess_fil = hfst.HfstInputStream(args.guesser_fst)
guess_fst = guess_fil.read()
map_fst = guess_fst.copy()
guess_fst.lookup_optimize()

def unique_entry(word_forms):
    remaining = set()
    first = True
    for word_form in word_forms:
        entries_and_weights = guess_fst.lookup(word_form, output="tuple")
        entries = set()
        for e,w in entries_and_weights:
            entries.add(e)
        if first:
            first = False
            remaining = entries
        else:
            remaining = remaining & entries
        if len(remaining) <= 1:
            break
    return remaining

map = {}                        # word form sets for an entry
pam = {}                        # entry sets for a word form
word_fil = open(args.word_forms)
for line_nl in word_fil:
    word = line_nl.strip()
    res_lst = guess_fst.lookup(word)
    for res in res_lst:
        entry, weight = res
        if not entry in map:
            map[entry] = set()
        map[entry].add(word)
        if not word in pam:
            pam[word] = set()
        pam[word].add(entry)

for entry in sorted(map.keys(), key=lambda x: len(map[x]), reverse=True):
    if args.verbosity > 0:
        print("--entry:", entry) ##
    word_forms = map[entry]
    if len(word_forms) < args.minimum_forms:
        continue
    entries = unique_entry(word_forms)
    if args.verbosity > 0:
        print("entries =", entries)
    if len(entries) == 1:
        if entry != list(entries)[0]:
            if args.verbosity > 0:
                print("--", entry, "--", " ".join(sorted(word_forms)))
            continue
        print(entry + "\t" + " ".join(sorted(word_forms)))
        word_form_set = map[entry]
        if args.verbosity > 0:
            print("----word_form_set:", word_form_set)
        for word in word_form_set:
            if args.verbosity > 10:
                print("------word:", word, "pam.get(word, set():", pam.get(word, set()))
            for ent in pam.get(word, set()):
                if args.verbosity > 10:
                    print("--------ent:", ent)
                if ent in map:
                    if args.verbosity > 20:
                        print("--------map[ent]:", map[ent])
                    prev = map[ent]
                    map[ent] = map[ent].difference(word_forms)
                    if prev != map[ent]:
                        if args.verbosity > 10:
                            print("--------map[", ent, "] =", sorted(prev), "!=", sorted(map[ent])) ###
    del map[entry]
    #else:
    #    print("***", entry + "\t" + " ".join(word_forms))
