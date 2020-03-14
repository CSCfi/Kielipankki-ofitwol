import re, sys, argparse

argparser = argparse.ArgumentParser(
    "python3 good-compounds.py",
    description="""Select a set of compound entries out of an analysed corpus.""")
argparser.add_argument(
    "-m", "--minimum-frequency",
    help="The number of distinct forms required in order to accept the compound",
    type=int, default=1)
argparser.add_argument(
    "-v", "--verbosity",
    help="Level of diagnostic output",
    type=int, default=0)
args = argparser.parse_args()

freq = {}

for line_nl in sys.stdin:
    if args.verbosity > 0:
        print(line_nl)
    wrd, entry_feat, wght = line_nl.split("\t")
    if not wrd or wght == "inf\n":
        continue
    if not "§" in entry_feat:
        continue
    entry, semicol, features = entry_feat.partition(";")
    if args.verbosity > 0:
        print("«", wrd, entry, features, "«")
    freq[entry] = freq.get(entry, 0) + 1

for entry, fq in freq.items():
    if fq < args.minimum_frequency:
        continue
    print(entry, "!", fq)
