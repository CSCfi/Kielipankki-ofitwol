

entry_set = {}          # entry_set[wrd] == {ent1, ..., entn}
word_set = {}           # word_set[entr] == {word1, ..., wordk}
weight_sum = {}         # weight_sum[entr] == sum(we1, we2, ...)
entriesofwords = {}     # entriesofwords["w1 w2 ... wn"] == {e1, .., ek}

def delete_entry(entry):
    """Delete an entry cand and the words it would analyse from the dicts"""
    global entry_set, word_set
    for word in word_set[entry]:
        entry_set[word].discard(entry)
    del word_set[entry]
    del weight_sum[entry]
    return

def delete_all_words(entry):
    """Delete from dicts its words from remaining entry candidates"""
    global entry_set, word_set
    siz = len(word_set[entry])
    for word in word_set[entry]:
        for entr in entry_set[word]:
            if entr in word_set and siz > len(word_set[entr]):
                word_set[entr].discard(word)
        if not entry_set[word]:
            del entry_set[word]
    return

def unique_entry(entry):
    global entry_set, word_set
    word_lst = list(word_set[entry])
    if not word_lst:
        return set()
    else:
        u_set = entry_set[word_lst[0]]
        for word in word_lst[1:]:
            e_set = entry_set[word]
            u_set = u_set & e_set
        return u_set

def main():
    global entry_set, word_set
    import argparse
    arpar = argparse.ArgumentParser("python3 guessfromwordsofentry.py")
    arpar.add_argument(
        "-a", "--analysed",
        help="file of analyzed word forms in a format "
        "compatible with hfst-lookup output")
    arpar.add_argument(
        "-b", "--beam",
        help="""Entry candidates for identical sets of words
        but with a weight sum higher than the best plus this beam
        are discarded.  Default is 10""",
        type=int, default=10)
    arpar.add_argument(
        "-d", "--delta",
        help="Default is 3",
        type=int, default=3)
    arpar.add_argument(
        "-m", "--minimum",
        help="""Ignore entry candidates with fewer words than this. 
        Default is 4""",
        type=int, default=3)
    arpar.add_argument(
        "-v", "--verbosity",
        help="level of  diagnostic output, default is 0.",
        type=int, default=0)
    args = arpar.parse_args()

    if not args.analysed:
        import sys
        ana_fil = sys.stdin
    else:
        ana_fil = open(args.analysed, "r")
#
# First pass: Collect data from the analysed words
#
    for line_nl in ana_fil:
        line = line_nl.strip()
        if not line:
            continue
        if line.count("\t") != 2:
            print("***", line)
            continue
        [word, entry_and_feats, weight] = line.split("\t")
        if weight == "inf":
            continue
        else:
            weight = float(weight.strip().replace(",", "."))
        entry, semicol, feats = entry_and_feats.partition(";")
        if not semicol:
            entry, plus, feats = entry.partition("+")
        if entry not in word_set:
            word_set[entry] = set()
        word_set[entry].add(word)
        if word not in entry_set:
            entry_set[word] = set()
        entry_set[word].add(entry)
        weight_sum[entry] = weight_sum.get(entry, 0.0) + weight
    ana_fil.close()
    #
    # Second pass: Delete inferior enty candidates
    #
    for entry in word_set.keys():
        if not unique_entry(entry):
            delete_entry(entry)
    for entry in sorted(word_set.keys(),
                        key=lambda en: len(en),
                        reverse=True):
        if len(word_set[entry]) < args.minimum:
            delete_entry(entry)
            continue
        for word in word_set[entry]:
            for e in entry_set[word]:
                if word_set[entry] < word_set[e]:
                    delete_entry(entry)
                    #print("deleting", entry, "which is inferior to", e)###
                    break # the innermost loop
            else:
                continue # the middle loop
            break # the middle loop
    #
    # Third pass: Select the entry candidate with the smallest weight
    # out of candidates competing of the same set of words
    #
    for entry, w_set in word_set.items():
        words_str = " ".join(sorted(w_set))
        if not words_str in entriesofwords:
            entriesofwords[words_str] = set()
        entriesofwords[words_str].add(entry)

    for words_str, ent_set in entriesofwords.items():
        # print(words_str) ###
        best_weight = min(weight_sum[ent] for ent in ent_set)
        for ent in ent_set:
            if weight_sum[ent] > best_weight + args.beam:
                delete_entry(ent)
        
    #
    # Fourth pass: Select most likely entries first and remove their
    # words from the entries coming later in the queue
    #
    if not word_set:
        return
    sz = max([len(word_set) for entry, word_set in word_set.items()])
    #print("largest set of word_set", sz)

    delta = args.delta
    while sz > 4:
        del_ent_lst = []
        for entry in word_set:
            #print(sz, entry, word_set[entry])###
            lgt = len(word_set[entry])
            if lgt < args.minimum:
                del_ent_lst.append(entry)
                continue
            wght = weight_sum[entry] / lgt
            if entry in word_set and len(word_set[entry]) >= sz - delta:
                print("{} ; ! {:.2f} {}".
                      format(entry,
                             wght,
                             " ".join(sorted(list(word_set[entry])))))
                delete_all_words(entry)
                del_ent_lst.append(entry)
        for ent in del_ent_lst:
            del word_set[ent]
        sz = sz - delta
    return

if __name__ == "__main__":
    main()
    
