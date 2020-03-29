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
    "-n", "--lexname",
    help="""Name of the lexicon to be made out of the input entries if not given
    by a LEXICON line in the input file.""",
    default="")
argparser.add_argument(
    "-c", "--continuation",
    help="A default name of the continuation lexicon if the entry has none",
    default="")
argparser.add_argument(
    "-r", "--rules",
    help="Rule FST for generating base forms, default is None",
    default="")
args = argparser.parse_args()
lexicon_name = args.lexname

mch_set = set()
definition_lst = []
entry_lst = []

if args.rules:
    import generate
    import hfst
    generate.init(args.rules)

line_lst = []
for line_nl in sys.stdin:
    line, exclam, comment = line_nl.partition("!")
    line = re.sub(r"\s+", " ", line)
    line = line.strip()
    if line.startswith("LEXICON"):
        lexicon_keyword, space, lexicon_name = line.partition(" ")
        if not lexicon_name:
            exit("*** LEXICON NAME EMPTY")
        continue
    mch_lst =re.findall(r"\{[^}]+\}|\+[A-Z0-9]+", line)
    for mch in mch_lst:
        mch_set.add(mch)
    #print("line:", line) ###
    if "=" in line or line_lst:
        line_lst.append(line)
        #print("line_lst:", line_lst) ###
        if line.endswith(";"):
            line_str = " ".join(line_lst)
            line_str = line_str.strip(" \t\n;")
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

base_suffixes = {
    "/s": "",
    "/s12": "",
    "/s2": "",
    "/s3": "",
    "/a": "",
    "/acomp": "m{pm}i",
    "/r": "",
    "/rcomp": "m{pm}i",
    "/v": "{dlnrtØ}{aä}",
    "/v012": "{dlnrtØ}{aä}",
    "/v02": "{dlnrtØ}{aä}",
    "/v3": "{dlnrtØ}{aä}",
    "/p": "",
    "/pc": "",
    "/po": "",
    "/ps": ""
}

if not lexicon_name:
    exit("*** LEXICON NAME NOT GIVEN AT ALL!")
print("LEXICON", lexicon_name)
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
        # entry = entry.replace("+", "%;+", 1) ###
        if rest:
            cont, sp, wght = rest.partition(" ")
            continuation = cont if cont else args.continuation
            weight = ' "weight: ' + wght + '"' if wght else ""
        else:
            continuation = args.continuation
            weight = ''
        baseform, colon, mphon_form = entry.partition(":")
        #print("entry, continuation, weight", entry, continuation, weight)
        #print("baseform", baseform) ###
        if args.rules and not colon:
            if continuation in base_suffixes:
                base_mphon = baseform + base_suffixes[continuation]
                base_lst = generate.generate(base_mphon)
                if base_lst:
                    base_str = min(base_lst, key=len)
                else:
                    base_str = "**" + base_mphon + "**"
            else:
                base_str = baseform
            base_str = base_str.replace("Ø", "")
            entry = base_str + ":" + entry            

        #print("entry, continuation, weight", entry, continuation, weight) ###
        print(entry, continuation + weight, ";")

