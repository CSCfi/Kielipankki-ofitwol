# affix2analylexc.py:
# builds a lexc file for analysis out of a csv file of affixes

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

import re, csv, sys

import argparse
argparser = argparse.ArgumentParser(
    "python3 affies2analysis.py",
    description="""
    Converts an affix CSV file into a LEXC file according to the mode
    that is selected.

    The "MPHON" mode produces LEXC entries suitable for constructing
    an analyser where one can produce the base form of the lexeme by
    generating from the upper string according to the rules.

    The "GUESS" mode produces LEXC entries suitable for guessing LEXC
    entries for lexemes out of inflected forms of that lexeme.  In
    guessing, the inflection features are not needed, so they are
    omitted from the upper string of the LEXC entries.  Instead, the
    name of the continuation class is included in entries whose
    continuation class contains a slash "/".

    The "ENTRY" mode produces LEXC entries suitable for e.g. creating
    new lexcial entries with a special analysator with more liberal
    compounding or derivational mechanism.  The mode is similar to the
    GUESS mode but the inflectional features are included in the upper
    string of the LEXC entries.

    The "BASE" mode assumes that the base forms of the word entries
    already have a base form as their upper LEXC string.  No
    morphophonemes of the affixes are included in the upper LEXC
    string.  Compounding and derivation is restrected in this mode
    because the base form of complex analyses is just a concatenation
    of those base forms.

""")
argparser.add_argument(
    "-m", "--mode", choices=["MPHON", "GUESS", "ENTRY", "BASE"],
    help="""Whether the lexicon produces base forms, morphophonemic form or
    guessed entries""",
    default="base")
argparser.add_argument(
    "-d", "--delimiter", default=",",
    help="CSV field delimiter (default is ',')")
argparser.add_argument(
    "-v", "--verbosity",
    default=0, type=int,
    help="level of diagnostic output")
args = argparser.parse_args()

mode = args.mode

feature_set = set()
multichars = set()

def collect_multichars(str):
    if len(str) < 2: return
    lst = re.findall(r"[{][^}]+[}]", str)
    for mch in lst:
        multichars.add(mch)
    return

out_lst = []

infile = sys.stdin
rdr = csv.DictReader(infile, delimiter=args.delimiter)
prevID = args.delimiter
for r in rdr:
    if args.verbosity >= 10:
        print(r)
    next_lst = r["NEXT"].split()
    if (not next_lst) or r["NEXT"].startswith('!'):
        continue
    ide = prevID if r["ID"] == '' else r["ID"]
    ok = (not r["MODE"]) or (mode in r["MODE"])
    if not ok:
        continue
    mphon_str = r["MPHON"].strip()
    collect_multichars(mphon_str)
    feature_lst = r['FEAT'].split()
    feature_str = (('+' + ('+'.join(feature_lst)))) if feature_lst else ""
    for feat in feature_lst:
        feature_set.add("+" + feat)
    basef_str = r["BASEF"].strip()
    if (not feature_lst) and (not basef_str):
        basef_str = mphon_str
    weight_str = (' "weight: {}"'.format(r["WEIGHT"])
                  if r["WEIGHT"] else "" )
    for nxt in next_lst:
        if mode == "MPHON":
            if ("/" in ide) and nxt != "SecondPart":
                feat_str = "{§}" + feature_str
            else:
                feat_str = feature_str
        elif mode == "GUESS":
            feat_str = ""
            if "/" in ide and nxt != "SecondPart":
                feat_str = "% " + ide + "%;" + feat_str
        elif mode == "ENTRY":
            if "/" in ide and nxt != "SecondPart":
                feat_str = "% " + ide + "%;" + feature_str
            else:
                feat_str = feature_str
        elif  mode == "BASE":
            basef_str = ""
            feat_str = feature_str
        basefeat_str = basef_str + feat_str
        if basefeat_str == mphon_str:
            lexc_str = "{} {}{} ;".format(basefeat_str,
                                          nxt, weight_str)
        else:
            lexc_str = "{}:{} {}{} ;".format(basefeat_str, mphon_str,
                                               nxt, weight_str)
        if prevID != ide:
            prevID = ide
            out_lst.append("LEXICON %s" % ide)
        out_lst.append(lexc_str)

outfile = sys.stdout
if multichars or feature_set:
    print("Multichar_Symbols", file=outfile)
    multichar_lst = sorted(list(multichars))
    multichar_str = " ".join(multichar_lst)
    print(multichar_str, file=outfile)
    features_lst = sorted(list(feature_set))
    print(" ".join(features_lst), file=outfile)
for line in out_lst:
    print(line, file=outfile)
outfile.close()
