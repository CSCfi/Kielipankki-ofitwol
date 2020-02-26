# converting KSK into a (perhaps proprietary) lexicon using patterns
#

LEX=ksk-lex-n.lexc ksk-lex-v.lexc ksk-lex-p.lexc

all : ksk-analy.ofst

ksk-analy.ofst: ksk-lex.fst ../ofi/ofi-rules.fst ../ofi/ofi-examples.pstr delete.fst Makefile
	hfst-compose-intersect -a -1 $< -2 ../ofi/ofi-rules.fst |\
	hfst-compose -2 delete.fst |\
	hfst-invert |\
	hfst-minimize -o ksk-analy.fst
	hfst-fst2fst -i ksk-analy.fst -O -o $@

ksk-lex.fst: ofi-analy-aff.lexc $(LEX) Makefile
	hfst-lexc -f openfst-tropical -o $@ ofi-analy-aff.lexc $(LEX)

ofi-analy-aff.lexc: ofi-affixes.csv ../src/affixes2analysis.py Makefile
	python3 ../src/affixes2analysis.py -e $< $@

ksk-lex-n.lexc: ksk-conv-n.fst classes-n.txt Makefile
	python3 ksk2lexc.py --codes=classes-n.txt ~/Dropbox/lang/fin/ksk/ksk-n.dic $< Nouns $@ > ksk-lex-n.log

ksk-lex-v.lexc: ksk-conv-v.fst classes-v.txt
	python3 ksk2lexc.py --codes=classes-v.txt ~/Dropbox/lang/fin/ksk/ksk-v.dic $< Verbs $@ > ksk-lex-v.log

ksk-lex-p.lexc : kskp2lexc.py
	cat ~/Dropbox/lang/fin/ksk/ksk-p.dic | python3 kskp2lexc.py > $@

ksk-conv-n.fst: ksk-conv-n.lexc
	hfst-lexc -f openfst-tropical -o $@ $<

ksk-conv-v.fst: ksk-conv-v.lexc
	hfst-lexc -f openfst-tropical -o $@ $<

ksk-conv-n.lexc classes-n.txt: ksk-pat-na.csv pat-proc.py
	python3 pat-proc.py -c classes-n.txt --mode c -n Root $< > $@

ksk-conv-v.lexc classes-v.txt: ksk-pat-v.csv pat-proc.py
	python3 pat-proc.py -c classes-v.txt --mode c -n Root $< > $@

ofi-rules.fst: ofi-rules.twol ksk-renamed.pstr
	twol-comp -o $@ --thorough 2 \
	  --wrong ofi-rules-wrong.fst \
	  --lost ofi-rules-lost.fst \
	  ksk-renamed.pstr $< > ofi-rules.log

delete.fst:
	echo "Ø -> 0" | hfst-regexp2fst -o $@

clean:
	rm -f ksk-*.ofst ksk-*.fst
	rm -f ksk-conv-*.lexc
