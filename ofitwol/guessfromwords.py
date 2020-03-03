

def main():
    import argparse
    arpar = argparse.ArgumentParser("python3 guessfromwords.py")
    arpar.add_argument(
        "-a", "--analysed",
        help="file of analyzed word forms in a format "
        "compatible with hfst-lookup output")
    arpar.add_argument(
        "-d", "--delta",
        help="Default is 3",
        type=int, default=3)
    arpar.add_argument(
        "-m", "--minimum",
        help="Default is 4",
        type=int, default=3)
    arpar.add_argument(
        "-v", "--verbosity",
        help="level of  diagnostic output, default is 0.",
        type=int, default=0)
    args = arpar.parse_args()

    entries = {}                # entries[wrd] == {ent1, ..., entn}
    words = {}                  # words[entr] == {word1, ..., wordk}

    def delete_entry(entry):
        for word in words[entry]:
            entries[word].discard(entry)
        del words[entry]
        return

    def delete_all_words(entry, word_lst):
        #print("deleting:", word_lst)###
        siz = len(words[entry])
        for word in word_lst:
            for entry in entries[word]:
                if entry in words and siz > len(words[entry]):
                    words[entry].discard(word)
            if not entries[word]:
                del entries[word]
        return

    if not args.analysed:
        import sys
        ana_fil = sys.stdin
    else:
        ana_fil = open(args.analysed, "r")
    for line in ana_fil:
        if not line.strip():
            continue
        if line.count("\t") != 2:
            print("***", line)
            exit()
        [word, entry_and_feats, weight] = line.strip().split("\t")
        if weight == "inf":
            continue
        entry, semicol, feats = entry_and_feats.partition(";")
        if entry not in words:
            words[entry] = set()
        words[entry].add(word)
        if word not in entries:
            entries[word] = set()
        entries[word].add(entry)
    ana_fil.close()

    for entry in sorted(words.keys(), key=lambda en: len(en), reverse=True):
        for word in words[entry]:
            for e in entries[word]:
                if words[entry] < words[e]:
                    delete_entry(entry)
                    #print("deleting", entry, "which is inferior to", e)###
                    break # the innermost loop
            else:
                continue # the middle loop
            break # the middle loop

    sz = max([len(word_set) for entry, word_set in words.items()])
    #print("largest set of words", sz)

    delta = args.delta
    while sz > 4:
        del_ent_lst = []
        for entry in words:
            #print(sz, entry, words[entry])###
            if entry in words and len(words[entry]) >= sz - delta:
                print(entry, "--", " ".join(sorted(list(words[entry]))))
                delete_all_words(entry, list(words[entry]))
                del_ent_lst.append(entry)
        for ent in del_ent_lst:
            del words[ent]
        sz = sz - delta
    return

if __name__ == "__main__":
    main()
    
