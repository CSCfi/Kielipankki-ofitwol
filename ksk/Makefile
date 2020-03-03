# converting KSK into a (perhaps proprietary) lexicon using patterns
#

LEX=ksk-lex-na.lexc ksk-lex-v.lexc ksk-lex-p.lexc
KSKDIC=~/Dropbox/lang/fin/ksk

all : ksk-analy.ofst

ksk-analy.ofst: ksk-lex.fst ofi-rules.fst ../ofitwol/ofi-examples.pstr delete.fst Makefile
	hfst-compose-intersect -a -1 $< -2 ofi-rules.fst |\
	hfst-compose -2 delete.fst |\
	hfst-invert |\
	hfst-minimize -o ksk-analy.fst
	hfst-fst2fst -i ksk-analy.fst -O -o $@

ksk-lex.fst: ofi-analy-aff.lexc $(LEX) Makefile
	hfst-lexc -f openfst-tropical -o $@ ofi-analy-aff.lexc $(LEX)

ofi-analy-aff.lexc: ofi-affixes.csv ../ofitwol/affixes2analysis.py Makefile
	python3 ../ofitwol/affixes2analysis.py -e $< $@

ksk-lex-na.lexc: ksk-conv-na.fst classes-na.txt $(KSKDIC)/ksk-n.dic Makefile
	python3 ksk2lexc.py --codes=classes-na.txt \
		$(KSKDIC)/ksk-n.dic $< Nouns $@ > ksk-lex-na.log

ksk-lex-v.lexc: ksk-conv-v.fst classes-v.txt
	python3 ksk2lexc.py --codes=classes-v.txt $(KSKDIC)/ksk-v.dic $< Verbs $@ > ksk-lex-v.log

ksk-lex-p.lexc : kskp2lexc.py
	cat $(KSKDIC)/ksk-p.dic | python3 kskp2lexc.py > $@

ksk-conv-na.fst: ksk-conv-na.lexc
	hfst-lexc -f openfst-tropical -o $@ $<

ksk-conv-v.fst: ksk-conv-v.lexc
	hfst-lexc -f openfst-tropical -o $@ $<

ksk-conv-na.lexc classes-na.txt: ksk-pat-na.csv pat-proc.py
	python3 pat-proc.py -c classes-na.txt --mode c -n Root $< > $@

ksk-conv-v.lexc classes-v.txt: ksk-pat-v.csv pat-proc.py
	python3 pat-proc.py -c classes-v.txt --mode c -n Root $< > $@

ofi-rules.fst: ofi-rules.twol ofi-examples.pstr
	twol-comp -o $@ --thorough 2 \
	  --wrong ofi-rules-wrong.fst \
	  --lost ofi-rules-lost.fst \
	  ofi-examples.pstr $< > ofi-rules.log

delete.fst:
	echo "Ø -> 0" | hfst-regexp2fst -o $@

clean:
	rm -f ksk-*.ofst ksk-*.fst
	rm -f ksk-conv-*.lexc
