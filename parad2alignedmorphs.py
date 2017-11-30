import csv, re, sys
from orderedset import OrderedSet
morph_set = {}
with open("ksk-paradigms.csv") as csvfile:
    reader = csv.DictReader(csvfile, delimiter=';')
    for row in reader:
        for column_label in row: # process each cell of the row
            words = row[column_label] # space separated string of words
            if column_label in {'ID', 'KSK'} or words == '': continue
            morpheme_id_list = column_label.split('.')
            if morpheme_id_list[0] == 'STM':
                morpheme_id_list[0] = row['ID']
            words_clean = re.sub(r'[][()]', '', words)
            word_list = re.split(r"\s+", words_clean.strip())
            # each word as a . separated string of morphs
            for morphs in word_list:
                if morphs[0] == '*':
                    continue
                morph_list = morphs.split('.')
                if len(morph_list) != len(morpheme_id_list):
                    print(morph_list, "and", morpheme_id_list, "incompatible")
                for feat, morph in zip(morpheme_id_list, morph_list):
                    if feat not in morph_set:
                        morph_set[feat] = OrderedSet()
                    morph_set[feat].add(morph)

sys.path.insert(0, "/Users/koskenni/github/alignment/")
from multialign import aligner

fil = open("alignments.py", 'w')
alignments = {}
morphs = {}
vowels = 'aeiouyäö'
l = len(vowels)

for morpheme_id in sorted(morph_set.keys()):
    if morpheme_id in {'ILL'}:
        morphs[morpheme_id] = [x+y+'n' for x in ['', 'h'] for y in vowels]
        aligned_sym_seq = ['Ø'*l+'h'*l, vowels*2, 'n'*l*2 ]
    else:
        morphs[morpheme_id] = list(morph_set[morpheme_id])
        aligned_sym_seq = aligner(list(morph_set[morpheme_id]),
                                    2, morpheme_id, verbosity=0,
                                    max_weight_allowed=10000.0)
    alignments[morpheme_id] = aligned_sym_seq

print("aligned_morphs =", alignments, "\n", file=fil)

print("morphs =", morphs, file=fil)

        
            
        



    
