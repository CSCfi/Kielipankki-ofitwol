all: ksk.samp.m2s.wpairs s2b.fst

accept:
	mv ksk.samp.m2s.wpairs  ksk.samp.m2s.bak.wpairs

ksk-examples.strings: ksk-zerofilledparad.csv idalmphon2examples.py
	python3.6 idalmphon2examples.py > $@

ksk-zerofilledparad.csv: ksk-paradigms.csv alignments.py parad2idalignmphon.py
	python3.6 parad2idalignmphon.py

alignments.py: ksk-paradigms.csv parad2alignedmorphs.py
	python3.6 parad2alignedmorphs.py

ksk.samp.m2s.wpairs: lex.b2m.fst rul.m2s.fst
	hfst-project -i lex.b2m.fst -p output | hfst-compose-intersect -2 rul.m2s.fst | hfst-fst2strings -X obey-flags | sort > ksk.samp.m2s.wpairs

s2b.fst: ofi.b2s.fst Makefile intro.fst delete.fst
	hfst-invert -i $< | hfst-compose -F delete.fst | hfst-minimize -o $@

ofi.b2s.fst: lex.b2m.fst rul.m2s.fst delete.fst Makefile
	hfst-compose-intersect -a -1 lex.b2m.fst -2 rul.m2s.fst | hfst-compose -F -2 delete.fst -o $@

lex.b2m.fst: lex.b2m.lexc Makefile
	hfst-lexc -A  -o $@ $< 

lex.b2m.lexc: featmultich.lexc morphophonemes.lexc affixes.lexc entries.lexc features.lexc Makefile
	cat featmultich.lexc morphophonemes.lexc affixes.lexc entries.lexc features.lexc > $@

affixes.lexc: affixes.csv csv2lexc.py
	python3 csv2lexc.py  < $< > $@

entries.lexc: entries.csv Makefile
	python3 csv2lexc.py < $< > $@

entries.csv: verb.words.csv  words2entries.py
	python3 words2entries.py < $< > $@

verb.words.csv: ksk-v-samp.dic ksk2words.py
	python3 ksk2words.py < $< > $@

features.lexc featmultich.lexc: features.csv feat2lexc.py
	python3 feat2lexc.py < $< -l features.lexc -m featmultich.lexc

rul.m2s.fst: rul.m2s.twolc
	hfst-twolc -R -i $< -o $@

test.result: rul.m2s.fst test.m2s.pstr
	hfst-pair-test -i $< -I test.m2s.pstr > test.result

%.csv: %.gnumeric
	ssconvert $< $@

test.m2s.pstr alpha.twolc morphophonemes.lexc: symbols.csv symbols2lexc.py
	python3 symbols2lexc.py < $<

delete.fst:
	echo 'Ø -> 0' | hfst-regexp2fst > $@

intro.fst: delete.fst
	hfst-invert -i $< -o $@
