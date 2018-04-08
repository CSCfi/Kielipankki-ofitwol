import re,  csv
from alignments import aligned_morphs

aligned_morph = {}
mphon_repr = {}
morphophonemes = set()

def clean(str):
    if re.match(r"^(.)\1*$", str):
        return str[0]
    else:
        sym = '{' + str + '}'
        morphophonemes.add(sym)
        return sym

for morpheme_id, aligned_sym_seq in aligned_morphs.items():
    l = len(aligned_sym_seq[0])
    morphoph_seq = [clean(x) for x in aligned_sym_seq]
    zero_filled_morphs = [" ".join([x[i] for x in aligned_sym_seq])
                              for i in range(0,l)]
    original_morphs = [re.sub(r"[Ø ]+", r"", x) for x in zero_filled_morphs]
    for om, zm in zip(original_morphs, zero_filled_morphs):
        aligned_morph[(morpheme_id, om)] = zm 
    mphon_repr[morpheme_id] = " ".join(morphoph_seq)

#print(aligned_morph) ##
#print(mphon_repr, "\n") ##
#print(morphophonemes) ##

mphon_name = {
    '{aaoo}': '{ao}', # kal<a>~kal<o>ja
    '{aaØØ}': '{aØ}', # koir<a>~koir<>ia
    '{aaää}': '{aä}', # vowel harmony
    '{aeiouyäöaeiouyäö}': '{V}', # maah<a>n, valo<o>n
    '{aäaaä}': '{aä}', # vowel harmony
    '{aØo}': '{aoØ}', # perun<a>~perun<o>ita~perun<>ia
    '{dt}': '{td}', # pa<t>o~pa<d>on, mai<d>en~mait<t>en
    '{dttt}': '{td}',
    '{eeØØ}': '{eØ}', # korke<e>, leve<e>, kame<e>
    '{ieeØØ}': '{ieeØ}', # tupp<e>na, tupp<>ia
    '{ieei}': '{ei}', # s<e><e>n~s<i><i>n
    '{ijØ}': '{ij}',
    '{mpp}': '{pm}',
    '{pØpØp}': '{pØ}',
    '{sØhØh}': '{sØh}',
    '{tddtt}': '{td}',
    '{tØØtt}': '{tØ}',
    '{ØØØØØØØØhhhhhhhh}': '{Øh}', # maa<h>an, valo<>on
    }

with open("ksk-paradigms.csv") as csvfile:
    reader = csv.DictReader(csvfile, delimiter=';')
    for row in reader:
        for column_label in row:
            morphs = row[column_label]
            if column_label in {'ID', 'KSK'} or morphs == '':
                continue
            morpheme_id_list = column_label.split('.')
            if morpheme_id_list[0] == 'STM':
                morpheme_id_list[0] = row['ID']
            morphs_clean = re.sub(r'[][()]', '', morphs)
            morphs_list = re.split(r"\s+", morphs_clean.strip())
            for morphs in morphs_list:
                if morphs[0] == '*':
                    continue
                morph_list = morphs.split('.')
                if len(morph_list) != len(morpheme_id_list):
                    print(morph_list, "and", morpheme_id_list, "incompatible")
                mphon_lst = [mphon_repr[feat] for feat in morpheme_id_list]
                surf_lst = [aligned_morph[feat, morph]
                                for feat, morph
                                in zip(morpheme_id_list, morph_list)]
                mphon_repr_str = " ".join(mphon_lst)
                mphon_segment_lst = mphon_repr_str.split()
                mphon_segment_lst = [mphon_name[s] if s in mphon_name else s
                                         for s in mphon_segment_lst]
                surf_str = " ".join(surf_lst)
                surf_segment_lst = surf_str.split()
                pair_list = [ss if ms == ss else ms+":"+ss
                                 for ms, ss
                                 in zip(mphon_segment_lst, surf_segment_lst)]
                print(" ".join(pair_list))
