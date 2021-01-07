
def main():
    import argparse

    argparser = argparse.ArgumentParser(
        "python3 cleanlexc.py",
        description=""" Reads a newly compiled LEXC FST, extracts its
        alphabet and selects all symbols which start with "¤" i.e.
        weights and all symbols starting with "£" i.e. pattern names and
        builds a FST which removes both kinds of symbols from the LEXC FST
        and transforms the weight symbols into corresponding weights in
        the resulting FST""")
    argparser.add_argument(
        "-p", "--pattern-names",
        help="Keep the pattern names of reg exps the result lexicon FST",
        action="store_true")
    args = argparser.parse_args()

    import sys
    import hfst

    in_stream = hfst.HfstInputStream()
    lex_fst = in_stream.read()
    in_stream.close()

    alphabet_tup = lex_fst.get_alphabet()

    weight_lst = sorted([sym for sym in alphabet_tup
                         if sym.startswith("¤")])
    if not args.pattern_names:
        patnam_lst = sorted([sym for sym in alphabet_tup
                             if sym.startswith("£")])
    else:
        patnam_lst = []

    rul_lst = []
    for patnam in patnam_lst:
        rul_lst.append("{} -> 0".format(patnam))
    for weight in weight_lst:
        rul_lst.append("{} -> 0::{}".format(weight, weight[1:]))
    rul_str = ", ".join(rul_lst)

    rul_fst = hfst.regex(rul_str)

    out_stream = hfst.HfstOutputStream()
    out_stream.write(rul_fst)
    out_stream.close()

if __name__ == "__main__":
    main()
