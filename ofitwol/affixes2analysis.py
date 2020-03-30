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
import argparse
argparser = argparse.ArgumentParser(
    "python3 affies2analysis.py",
    description="""Converts an affix CSV file into a LEXC file according to the mode
    that is selected.

    In 'guess' mode continuation class names containing '/' are
    included in the input string and all features are omitted.

    In 'base' mode features are present but the continuation names are
    omitted.  This mode assumes that the lexicon entries already have
    a base form given for each entry.  Compounding and derivation is
    restrected in this mode because the base form of complex analyses
    is just a concatenation of those base forms.

    In 'mphon' mode the continuation names are also omitted and the
    features are present but some additional derivations and loops and
    continuations can be allowed because inverted rules will still
    produce the desired base forms.""")
argparser.add_argument(
    "infile",
    help="input CSV file which is a table of the affix data")
argparser.add_argument(
    "outfile",
    help="output LEXC file of the affix data")
argparser.add_argument(
    "-d", "--delimiter", default=",",
    help="CSV field delimiter (default is ',')")
argparser.add_argument(
    "-mode", "--mode", choices=["BASE", "MPHON", "GUESS"],
    help="""Whether the lexicon produces base forms, morphophonemic form or
    guessed entries""",
    default="base")
argparser.add_argument(
    "-v", "--verbosity",
    default=0, type=int,
    help="level of diagnostic output")
args = argparser.parse_args()

features = set()
multichars = set()

def collect_multichars(str):
    if len(str) < 2: return
    lst = re.findall(r"[{][^}]+[}]", str)
    for mch in lst:
        multichars.add(mch)
    return

out_lst = []
features = set()
nexts = set()
infile = open(args.infile, "r")
rdr = csv.DictReader(infile, delimiter=args.delimiter)
prevID = ",,"
for r in rdr:
    if args.verbosity >= 10:
        print(r)
    if r["NEXT"] == '' or r["NEXT"].startswith('!'):
        continue
    ide = prevID if r["ID"] == '' else r["ID"]
    if r["MODE"] and not args.mode in r["MODE"]:
        continue
    if prevID != ide:
        prevID = ide
        out_lst.append("LEXICON %s" % ide)
    collect_multichars(r["MPHON"])
    if r['FEAT'] == '' and r['BASEF'] == '':
        r['BASEF'] = r['MPHON']
    if r['BASEF'] == "!":
        r['BASEF'] = ""
    if r['FEAT'] and args.mode != "GUESS":
        featlist = re.split(" +", r['FEAT'])
        feat_str = '+' + '+'.join(featlist)
        for feat in featlist:
            features.add("+" + feat)
    else:
        feat_str = ''
    weight = r["WEIGHT"].strip()
    if weight:
        weight = '"weight: {}"'.format(weight)
    if "/" in ide and args.mode == "GUESS" and r['NEXT'] != "SecondPart":
        feat_str = "% " + ide + "%;" + feat_str
        features.add("% " + ide + "%;")
    elif "/" in ide and args.mode == "MPHON" and r['NEXT'] != "SecondPart":
        feat_str = "{§}" + feat_str
    for next in re.split(" +", r["NEXT"]):
        if next:
            if r['BASEF'] + feat_str == r['MPHON']:
                out_lst.append("{}{} {} {};".format(r['BASEF'],
                                                    feat_str,
                                                    next,
                                                    weight))
            else:
                out_lst.append("{}{}:{} {} {};".format(r['BASEF'],
                                                       feat_str,
                                                       r['MPHON'],
                                                       next,
                                                       weight))
outfile = open(args.outfile, "w")
if multichars or features:
    print("Multichar_Symbols", file=outfile)
    multichar_lst = sorted(list(multichars))
    multichar_str = " ".join(multichar_lst)
    print(multichar_str, file=outfile)
    features_lst = sorted(list(features))
    print(" ".join(features_lst), file=outfile)
for line in out_lst:
    print(line, file=outfile)
outfile.close()
