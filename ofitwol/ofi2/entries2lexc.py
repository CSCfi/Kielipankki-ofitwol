import re, sys, argparse

argparser = argparse.ArgumentParser(
    "python3 entries2lexc.py",
    description="""Convert a list of mphonemic entries and continuations into a lexc
    lexicon.  Each line in the input may have a comment starting with
    '!' which is discarded.  Each line may be either a regexp entry in
    angle brackets '<', '>' and a continuation, or an ordinary entry
    and a continuation plus an optional weight.  Multicharacters in
    entries must either be enclosed in curly brackets '{', '}' or be
    capital letter feature names preceded by a plus sign
    (e.g. '+GEN')""")
argparser.add_argument(
    "lexname",
    help="Name of the lexicon to be made out of the input entries.")
argparser.add_argument(
    "-c", "--continuation",
    help="A default name of the continuation lexicon if the entry has none",
    default="")
args = argparser.parse_args()


mch_set = set()
definition_lst = []
entry_lst = []

line_lst = []
for line_nl in sys.stdin:
    line, exclam, comment = line_nl.partition("!")
    line = re.sub(r"\s+", " ", line)
    line = line.strip()
    mch_lst =re.findall(r"\{[^}]+\}|\+[A-Z0-9]+", line)
    for mch in mch_lst:
        mch_set.add(mch)
    #print("line:", line) ###
    if "=" in line or line_lst:
        line_lst.append(line)
        #print("line_lst:", line_lst) ###
        if line.endswith(";"):
            line_str = " ".join(line_lst)
            line_str = line_str.strip(r" \t\n;")
            definition_lst.append(line_str)
            line_lst = []
        continue
    else:
        line = line.strip(" \t\n;")
        if not line:
            continue
        entry_lst.append(line)

if mch_set:
    print("Multichar_Symbols")
    mch_lst = sorted(list(mch_set))
    print(" ".join(mch_lst))

if definition_lst:
    print("Definitions")
for line in definition_lst:
    definition = re.sub(r"([{}])", r"%\1", line)
    print(definition, ";")

print("LEXICON", args.lexname)
for line in entry_lst:
    if line.startswith("<"):
        line = re.sub(r"([{}])", r"%\1", line)
        ent, rb, cont = line.rpartition(">")
        entry = ent + rb
        continuation = cont.strip() if cont else args.continuation
        print(entry, continuation, ";")
    else:
        entry, sp, rest = line.partition(" ")
        entry = entry.replace("_", "{§}")
        entry = entry.replace("+", "%;+", 1)
        if rest:
            cont, sp, wght = rest.partition(" ")
            continuation = cont if cont else args.continuation
            weight = ' "weight: ' + wght + '"' if wght else ""
        else:
            continuation = args.continuation
            weight = ''
        print(entry, continuation + weight, ";")

