.SUFFIXES :
.INTERMEDIATE :

RULEFST=../ofi-rules.fst
ANALYAFFLEXC=../analy-aff.lexc
AFFIXCSV=../ofi-affixes.csv

guess : guess-analy.ofst

guess-analy.ofst : guess-analy-n.ofst guess-analy-a.ofst guess-analy-v.ofst Makefile
	hfst-disjunct -1 guess-analy-n.fst -2 guess-analy-a.fst |\
	hfst-disjunct -2 guess-analy-v.fst -o guess-analy.fst
	hfst-fst2fst -i guess-analy.fst -o $@ -w

guess-analy-n.ofst: guespat-analy-lex-n.fst $(RULEFST) delete.fst Makefile
	hfst-compose-intersect -e -a -1 $< -2 $(RULEFST) |\
	hfst-compose -2 delete.fst |\
	hfst-invert |\
	hfst-minimize -o guess-analy-n.fst
	hfst-fst2fst -w -i guess-analy-n.fst -o $@

guess-analy-a.ofst: guespat-analy-lex-a.fst $(RULEFST) delete.fst Makefile
	hfst-compose-intersect -e -a -1 $< -2 $(RULEFST) |\
	hfst-compose -2 delete.fst |\
	hfst-invert |\
	hfst-minimize -o guess-analy-a.fst
	hfst-fst2fst -w -i guess-analy-a.fst -o $@

guess-analy-v.ofst: guespat-analy-lex-v.fst $(RULEFST) delete.fst Makefile
	hfst-compose-intersect -e -a -1 $< -2 $(RULEFST) |\
	hfst-compose -2 delete.fst |\
	hfst-invert |\
	hfst-minimize -o guess-analy-v.fst
	hfst-fst2fst -w -i guess-analy-v.fst -o $@

guespat-analy-lex-n.fst: guespat-n.lexc guess-aff.lexc Makefile $(ANALYAFFLEXC)
	hfst-lexc -E -f openfst-tropical -o $@ $(ANALYAFFLEXC) $<

guespat-analy-lex-a.fst: guespat-a.lexc guess-aff.lexc Makefile $(ANALYAFFLEXC)
	hfst-lexc -E -f openfst-tropical -o $@ $(ANALYAFFLEXC) $<

guespat-analy-lex-v.fst: guespat-v.lexc guess-aff.lexc Makefile $(ANALYAFFLEXC)
	hfst-lexc -E -f openfst-tropical -o $@ $(ANALYAFFLEXC) $<

guespat-a.lexc : guespat-a.entries guespat2lexc.py
	python3 guespat2lexc.py < $< > $@

guespat-n.lexc : guespat-n.entries guespat2lexc.py
	python3 guespat2lexc.py < $< > $@

guespat-v.lexc : guespat-v.entries guespat2lexc.py
	python3 guespat2lexc.py < $< > $@

guess-aff.lexc: $(AFFIXCSV) affixes2guessing.py
	python3 affixes2guessing.py $< $@

$(ANALYAFFLEXC): $(AFFIXCSV) ../affixes2analysis.py Makefile
	python3 ../affixes2analysis.py -e $< $@

$(RULEFST): ../ofi-rules.twol ../ofi-examples.pstr
	twol-comp -o $@ --thorough 2 \
	  --wrong ofi-rules-wrong.fst \
	  --lost ofi-rules-lost.fst \
	  ../ofi-examples.pstr $< > ofi-rules.log

delete.fst:
	echo "Ø -> 0" | hfst-regexp2fst -o $@

clean:
	rm -f gues*.fst
	rm -f gues*.ofst
	rm -f gues*.lexc


