.SUFFIXES :
.INTERMEDIATE :
.PHONY=build analyse

ID=sktp
ANALYSER=ofitwol.ofst
RULEFST=ofi-rules.fst
AFF=analy
DATA=../../data
LEX=lexic-s.lexc lexic-v.lexc lexic-a.lexc \
    lexic-p.lexc lexic-firstpart.lexc \
    lexic-edited.lexc lexic-noncomp-s.lexc
##$(ID)-lexic-compo.lexc
ANALYSES=$(ID)-corpus.big.analyses

build : ofitwol.ofst $(LEX)

analyse : $(ANALYSES)

ofitwol.ofst : lexic.fst $(RULEFST) delete.fst Makefile
	hfst-compose-intersect -a -1 $< -2 $(RULEFST) |\
	hfst-compose -2 delete.fst |\
	hfst-invert |\
	hfst-minimize -o $(ID)-analy.fst
	hfst-fst2fst -w -i $(ID)-analy.fst -o $@

lexic.fst : lexic-aff.lexc $(LEX) Makefile
	hfst-lexc -E -f openfst-tropical -o $@ $< $(LEX)

lexic-aff.lexc : ofi-affixes.csv ../affixes2analysis.py
	python3 ../affixes2analysis.py -e $< $@

lexic-noncomp-s.lexc : lexic-noncomp-s.entries entries2lexc.py
	python3 entries2lexc.py Compounds < $< > $@

lexic-edited.lexc : lexic-edited.entries entries2lexc.py
	python3 entries2lexc.py EditedEntries < $< > $@

lexic-a.lexc : lexic-a.entries entries2lexc.py
	python3 entries2lexc.py Adjectives < $< > $@

lexic-p.lexc : lexic-p.entries entries2lexc.py
	python3 entries2lexc.py Particles < $< > $@

lexic-s.lexc : lexic-s.entries entries2lexc.py
	python3 entries2lexc.py Nouns < $< > $@

lexic-v.lexc : lexic-v.entries entries2lexc.py entries2lexc.py
	python3 entries2lexc.py Verbs < $< > $@

lexic-firstpart.lexc : lexic-sgnom.words lexic-sggen.words
	cat $+ | python3 entries2lexc.py -c SecondPart FirstPart > $@

$(ANALYSES) : $(DATA)/$(ID)-corpus.words $(ANALYSER)
	hfst-lookup -b 15 -i $(ANALYSER) -I $< | \
		egrep '..' > $@

$(RULEFST) : ../ofi-examples.pstr ../ofi-rules.twol
	twol-comp -t 2 -w ofi-wrong.fst -l ofi-lost.fst -o $@ \
		$+ > ofi-rules.log

delete.fst :
	echo "Ø -> 0" | hfst-regexp2fst -o $@

$(ID)-compo-by-secd.analyses : $(ANALYSES)
	cut -f 2 $< | \
	egrep '§' | \
	cut -d ';' -f 1 | \
	sort -k 2 -t '}' | \
	tr '§' ' ' | \
	uniq -c > $@

clean:
	rm -f *.fst
	rm -f *.ofst
	rm -f *.lexc

distclean : clean 
	rm -f $(ID)-corpus.big.analyses


