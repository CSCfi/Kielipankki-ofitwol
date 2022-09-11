# affix2analylexc.py:
# builds a lexc file for analysis out of a csv file of affixes

copyright = """Copyright © 2017-2021, Kimmo Koskenniemi

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

multichars = set()

def collect_multichars(str):
    if len(str) < 2: return
    lst = re.findall(r"[{][^}]+[}]", str)
    for mch in lst:
        multichars.add(mch)
    return

def main():
    import argparse
    argparser = argparse.ArgumentParser(
        "python3 endings2lexc.py",
        description="""Converts an endings CSV file into a LEXC file""")
    argparser.add_argument(
        "-d", "--delimiter",
        help="CSV field delimiter (default is ',')",
        default=",")
    argparser.add_argument(
        "-z", "--zero_weights",
        help="Ignore any weights assigned to individual endings",
        action="store_true", default=False)
    argparser.add_argument(
        "-v", "--verbosity",
        help="Level of diagnostic output, (default is 0).",
        default=0, type=int)
    args = argparser.parse_args()

    #
    # First, read in all ending records and collect all multichar
    # symbols occurring in them:
    #
    feature_set = set()
    out_lst = []
    infile = sys.stdin
    rdr = csv.DictReader(infile, delimiter=args.delimiter)
    prevID = args.delimiter
    for r in rdr:
        if args.verbosity >= 10:
            print(r)
        next_lst = r["NEXT"].strip().split()
        if (not next_lst) or r["NEXT"].startswith('!'):
            continue
        ide = prevID if r["ID"] == '' else r["ID"]
        mphon_str = r["MPHON"].strip()
        collect_multichars(mphon_str)
        feature_lst = r['FEAT'].strip().split()
        for feat in feature_lst:
            feature_set.add("+" + feat)
        feature_str = (('+' + ('+'.join(feature_lst)))) if feature_lst else ""
        weight = r["WEIGHT"].strip()
        if args.zero_weights or not weight:
            weight_str = ""
        else:
            weight_str = ' "weight: {}"'.format(r["WEIGHT"])

        for nxt in next_lst:
            feat_str = feature_str
            if feature_str or mphon_str:
                lexc_str = "{}:{} {}{} ;".format(feature_str, mphon_str,
                                          nxt, weight_str)
            else:
                lexc_str = "  {}{} ;".format(nxt, weight_str)
            if prevID != ide:
                prevID = ide
                out_lst.append("LEXICON %s" % ide)
            out_lst.append(lexc_str)
    #
    # Finally, write the LEXC file with collected multichar symbol
    # definitions and the LEXC entries for individual endings.
    #
    if multichars or feature_set:
        print("Multichar_Symbols")
        multichar_lst = sorted(list(multichars))
        multichar_str = " ".join(multichar_lst)
        print(multichar_str)
        features_lst = sorted(list(feature_set))
        print(" ".join(features_lst))
    for line in out_lst:
        print(line)

if __name__ == "__main__":
    main()
