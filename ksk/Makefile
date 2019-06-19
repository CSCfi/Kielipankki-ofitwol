Q=-q

all:  guesser-v.fst ksk-lemmatizer-v.fst

fin-pat-conv-v.lexc: fin-pat-v.csv pat-proc.py affixmultich.py
	python3.6 pat-proc.py -p fin-pat-v.csv -c infl-codes-v.text > $@

fin-pat-conv-n.lexc: fin-pat-n.csv pat-proc.py affixmultich.py
	python3.6 pat-proc.py -p fin-pat-n.csv -c infl-codes-n.text> $@

fin-conv-v.fst: fin-pat-conv-v.lexc
	hfst-lexc $(Q) -E $< | hfst-minimize -E -o $@

fin-conv-n.fst: fin-pat-conv-n.lexc
	hfst-lexc $(Q) -E $< | hfst-minimize -E -o $@

fin-pat-guess-v.lexc: fin-pat-v.csv pat-proc.py affixmultich.py
	python3.6 pat-proc.py -m g -p fin-pat-v.csv > $@

affix-guess.lexc: affixes.csv affix-guesser.py
	python3.6 affix-guesser.py < affixes.csv > affix-guess.lexc

fin-guess-lex-v.fst: fin-pat-guess-v.lexc affix-guess.lexc
	hfst-lexc -E fin-pat-guess-v.lexc affix-guess.lexc | hfst-minimize -E -o $@

fin-guess-v.fst: fin-guess-lex-v.fst rul.m2s.fst delete.fst
	hfst-compose-intersect -1 $< -2 rul.m2s.fst | hfst-compose -2 delete.fst | hfst-minimize -E -o $@

guesser-v.fst: fin-guess-v.fst
	hfst-invert -i $< | hfst-minimize -E | hfst-fst2fst -w -o $@

rul.m2s.fst: rul.m2s.twolc
	hfst-twolc < $< -D -o $@

ksk-words-v.lexc: ~/Dropbox/lang/fin/ksk/ksk-v.dic ksk2lexc.py fin-conv-v.fst affixmultich.py
	python3.6 ksk2lexc.py -l $@ -c infl-codes-v.text -f fin-conv-v.fst < $< > ksk-words-v.log

ksk-words-n.lexc: ~/Dropbox/lang/fin/ksk/ksk-n.dic ksk2lexc.py infl-codes-n.text fin-conv-n.fst affixmultich.py
	python3.6 ksk2lexc.py -l $@ -c infl-codes-n.text -f fin-conv-n.fst < $< > ksk-words-n.log

ksk-lex-v.fst: ksk-words-v.lexc affix-analys.lexc
	hfst-lexc $(Q) -E $< affix-analys.lexc | hfst-minimize -E -o $@

ksk-analys-v.fst: ksk-lex-v.fst rul.m2s.fst delete.fst
	hfst-compose-intersect -1 $< -2 rul.m2s.fst | hfst-compose -2 delete.fst | hfst-minimize -E | hfst-invert -o $@ 

ksk-lem-v.fst: ksk-analys-v.fst rul.m2s.fst delete.fst
	hfst-compose-intersect -1 $< -2 rul.m2s.fst | hfst-compose -2 delete.fst | hfst-minimize -E -o $@

ksk-lemmatizer-v.fst: ksk-lem-v.fst
	hfst-fst2fst -w -i $< -o $@

affix-analys.lexc: affixes.csv affix-analys.py
	python3.6 affix-analys.py < affixes.csv > $@

affixmultich.py: affixes.csv collect-multich.py
	python3.6 collect-multich.py

delete.fst:
	echo "Ø -> 0" | hfst-regexp2fst -f openfst-tropical -o delete.fst

samp-words-v.lexc: ksk-v-samp.dic ksk2lexc.py fin-conv-v.fst affixmultich.py Makefile
	python3.6 ksk2lexc.py -l $@ < $< 

samp-lex-v.fst: samp-words-v.lexc affix-analys.lexc
	hfst-lexc $(Q) -E -f openfst-tropical -o $@ samp-words-v.lexc affix-analys.lexc

samp-analys-v.fst: samp-lex-v.fst rul.m2s.fst delete.fst affixmultich.py Makefile
	hfst-compose-intersect -1 samp-lex-v.fst -2 rul.m2s.fst | hfst-compose -2 delete.fst | hfst-minimize -E > $@
	hfst-invert -i $@ -o samp-lookup-v.fst

samp-lem-v.fst: samp-lookup-v.fst
	hfst-compose-intersect -1 $< -2 rul.m2s.fst | hfst-compose -2 delete.fst -o $@
