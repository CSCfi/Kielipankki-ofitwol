import re, csv, collections
from alignments import aligned_morphs

aligned_morph = {}

principl = ["", "GEN", "PTV", "ESS", "PL.PTV"] # principal parts

affixes = {
    '': '',
    'GEN': 'n',
    'PTV': '{Øt} {aä}',
    'ESS': '{nrs} {aä}',
    'ILL': '{Øh} {V} n',
    'ILLseen': 's e {eØ} n',
    'PL.INE': '{ij} s s {aä}',
    'PL.GENiden': '{ij} {dt} {ØtIDEN} e n',
    'PL.GENien': '{ij} e n',
    'PLGENten': 't e n',
    'GENin': 'i n',
    'PL.PTV': '{ij} {Øt} {aä}',
    'PL.ILL': '{ij} {Øh} i n',
    'PL.ILLsiin': '{ij} s i {iØ} n',
    }

# compute the aligned morphs with some zeros
for morpheme_id, aligned_sym_seq in aligned_morphs.items():
    l = len(aligned_sym_seq[0])
    zero_filled_morphs = ["".join([x[i] for x in aligned_sym_seq])
                              for i in range(0,l)]
    original_morphs = [re.sub(r"[Ø ]+", r"", x) for x in zero_filled_morphs]
    for om, zm in zip(original_morphs, zero_filled_morphs):
        aligned_morph[(morpheme_id, om)] = zm 

csv_in = open("ksk-paradigms.csv", 'r')
reader = csv.DictReader(csv_in, delimiter=';')
col_labels = reader.fieldnames[2:]
ids_lst = [re.sub(r"^STM[.]?", r"", x) for x in col_labels]
# print("ids_lst:", ids_lst) ##

csv_out = open("ksk-zerofilledparad.csv", 'w')
writer = csv.DictWriter(csv_out, ['IDS', 'ALIGNED', 'MPHON'], delimiter=';')
writer.writeheader()

# process each row of the table as a dict
for row in reader:
    # compute and collect first all aligned morphs for this row
    aligned_words = collections.OrderedDict()
    morphemes = {}
    # process each cell of the row
    for col, ids in zip(col_labels, ids_lst):
        words = row[col] # contents of a cell
        # print("***", col, ids, words) ##
        if words == '': continue
        wids = row['ID'] + '.' + ids if ids != '' else row['ID']
        morphemes[ids] = wids
        morpheme_id_list = morphemes[ids].split('.')

        words_clean = re.sub(r'[][()]', '', words)
        # list of words, each is period separated seq of morphs
        words_in_cell = re.split(r"\s+", words_clean.strip())

        zlst = []
        for word in words_in_cell: # process each word (and its morphs)
            if word[0] == '*':
                continue
            morph_list = word.split('.')
            if len(morph_list) != len(morpheme_id_list):
                print(morph_list, "and", morpheme_id_list, "incompatible")
            # look up the aligned morphs with some zeros as computed above
            surf_lst = [aligned_morph[feat, morph] for feat, morph
                            in zip(morpheme_id_list, morph_list)]
            zlst.append(surf_lst)
        aligned_words[ids] = zlst
        # print('***', zlst) ##
    # extract morphophponemes from principal parts of this row/lexeme
    mfs = []
    l = len(aligned_words[''][0][0]) # all aligned words are equally long
    # print("aligned_words", aligned_words) ##
    for i in range(0,l):
        # print("i:", i) ##
        sym_lst = []
        for fm in principl:
            wl = aligned_words[fm]
            # print("fm:", fm) ##
            for w in wl:
                # print("w:", w) ##
                sym_lst.append(w[0][i])
        mf = ''.join(sym_lst)
        mfon = mf[0] if re.match(r"^([a-zåäöšžü])(\1)*$", mf) else '{' + mf + '}'
        mfs.append(mfon)
        # print("mfs:", mfs) ##
    lst = []
    outdic = {}
    mphon_str = ' '.join(mfs)
    for col, ids in zip(col_labels, ids_lst):
        for w in aligned_words.get(ids, []):
            lst.append((morphemes[ids], w, mphon_str))
        wids = row['ID'] + '.' + ids if ids != '' else row['ID']
        outdic['IDS'] = wids
        aligned_lst = aligned_words.get(ids, [])
        for aw in aligned_lst:
            outdic['ALIGNED'] = ''.join(aw)
            outdic['MPHON'] = (mphon_str + ' ' + affixes[ids]).strip()
            writer.writerow(outdic)

