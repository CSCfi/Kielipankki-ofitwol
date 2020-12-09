import re

multichar_set = set()

def collect_mphons(expr_str):
    mch_lst = re.findall(r"\{[^}]+\}|\+[A-Z0-9]+", expr_str)
    for mch in mch_lst:
        multichar_set.add(mch)

def generated_base(mphon, cont):
    if cont in suffix_dict:
        base_mphon = mphon + suffix_dict[cont]
        base_lst = generate.generate(base_mphon)
        if base_lst:
            base_str = min(base_lst, key=len)
        else:
            base_str = "**" + base_mphon + "**"
    else:
        base_str = mphon
    base_str = base_str.replace("Ø", "")
    base_str = base_str.replace("§", "_")
    return base_str

import argparse

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
    help="""Name of the lexicon to be made out of the input
    entries if not given by a LEXICON line in the input file.""",
    default="")
argparser.add_argument(
    "-c", "--continuation",
    help="A default name of the continuation lexicon if the entry has none",
    default="")
argparser.add_argument(
    "-p", "--pattern-names",
    help="Add the pattern names of reg exp entries",
    action="store_true")
argparser.add_argument(
    "-s", "--base-suffixes",
    help="""Dict of mophophonemic suffixes for base form generation
    of each continuation clas""",
    default="base-suffixes.json")
argparser.add_argument(
    "-r", "--rules",
    help="Rule FST for generating base forms, default is None",
    default="")
args = argparser.parse_args()
lexicon_name = args.lexname

definition_lst = []
entry_lst = []

if args.rules:
    import generate
    import hfst
    generate.init(args.rules)

if args.base_suffixes:
    import json
    suffix_file = open(args.base_suffixes, "r")
    suffix_dict = json.load(suffix_file)
else:
    suffix_dict = {}

import sys

ent_pat = re.compile(
    r"""
    (?P<entry> \S +)
    (\s+ (?P<cont> [/A-ZÅÄÖŠŽa-zšžåäö] \S +))?
    (\s + (?P<weight> [0-9] +))?
    (\s*;)?
    """, re.X)
rege_pat = re.compile(
    r"""
    < (?P<re_entry> [^>]+ ) > # reg exp pattern
    \s*                       #
    (?P<cont> \S+ )           # continuation lexicon name
    (
      \s+                     #
      (?P<weight> \d+ )       # weight
      \s+
      (?P<name> [A-ZŠŽÅÄÖ]+ ) # name of the pattern
    )?
    """, re.X)
defi_pat = re.compile(r"^\s*[A-ZÅÄÖa-zåäö][A-ZÅÄÖa-zåäö0-9]+\s*=")

defi_line_lst = []
rege_line_lst = []

for line_nl in sys.stdin:
    line, exclam, comment = line_nl.partition("!")
    line = re.sub(r"\s+", " ", line)
    line = line.strip()
    if not line:
        continue
    if line.startswith("LEXICON"):
        lexicon_keyword, space, lexicon_name = line.partition(" ")
        if not lexicon_name:
            exit("*** LEXICON NAME MISSING")
        entry_lst.append(line)
        continue
    
    #print("line:", line) ###

    if defi_line_lst or " = " in line:
        # definitions may consist of several lines
        defi_line_lst.append(line)
        if line.endswith(";"):
            line_str = " ".join(defi_line_lst)
            line_str = line_str.strip(" \t\n;")
            collect_mphons(line_str)
            line_str = re.sub(r"([{}])", r"%\1", line_str)
            definition_lst.append(line_str)
            defi_line_lst = []

    elif rege_line_lst or line.startswith("<"):
        rege_line_lst.append(line)
        if line.endswith(";"):
            line_str = " ".join(rege_line_lst)
            line_str = line_str.strip(" \t\n;")
            collect_mphons(line_str)
            line_str = re.sub(r"([{}])", r"%\1", line_str)
            rege_mat = m_regent = rege_pat.fullmatch(line_str)
            r = rege_mat.group("re_entry").strip()
            c = rege_mat.group("cont")
            w = rege_mat.group("weight")
            n = rege_mat.group("name")
            n = "°" + n if n and args.pattern_names else ""
            if n:
                multichar_set.add(n)
            if w and n:
                entry_lst.append("< {} {}:0::{} > {} ;".format(r, n, w, c))
            elif w:
                entry_lst.append("< {} 0::{} > {} ;".format(r, w, c))
            elif n:
                entry_lst.append("< {} {}:0 > {} ;".format(r, n, c))
            else:
                entry_lst.append("< {} > {} ;".format(r, c))
            rege_line_lst = []

    else:
        ent_mat = ent_pat.fullmatch(line)
        if not ent_mat:
            exit("!!!!!!!!!!!!!!!!!!" + line)
        #### print(ent_mat.groups()) ####
        e = ent_mat.group("entry").replace("_", "{§}")
        collect_mphons(e)
        c = ent_mat.group("cont")
        if not c:
            c = args.continuation
            if ":" not in e and args.rules:
                e = generated_base(e, c) + ":" + e
        w = ent_mat.group("weight")
        w = ' "weight {}"'.format(w) if w else ""
        entry = "{} {}{} ;".format(e, c, w)
        entry_lst.append(entry)


if multichar_set:
    print("Multichar_Symbols")
    mch_lst = sorted(list(multichar_set))
    print(" ".join(mch_lst))

if definition_lst:
    print("Definitions")
for definition in definition_lst:
    print(definition, ";")

if not entry_lst[0].startswith("LEXICON"):
    print("LEXICON", args.lexname)

for line in entry_lst:
    print(line)

