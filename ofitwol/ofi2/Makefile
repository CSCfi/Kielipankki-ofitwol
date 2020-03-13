.SUFFIXES :
.INTERMEDIATE :
.PHONY=build analyse

ID=
OLDANALYSER=../../ksk/ksk-analy.ofst
RULEFST=ofi-rules.fst
AFF=analy
DATA=../../data
LEX=$(ID)-lexic-s.lexc $(ID)-lexic-v.lexc $(ID)-lexic-a.lexc \
    $(ID)-lexic-p.lexc $(ID)-lexic-firstpart.lexc
##$(ID)-lexic-compo.lexc
ANALYSES=$(ID)-corpus.big.analyses

analyse : $(ANALYSES)
build : ofitwol.ofst $(LEX)

ofitwol.ofst : lexic.fst $(RULEFST) delete.fst Makefile
	hfst-compose-intersect -a -1 $< -2 $(RULEFST) |\
	hfst-compose -2 delete.fst |\
	hfst-invert |\
	hfst-minimize -o $(ID)-analy.fst
	hfst-fst2fst -w -i $(ID)-analy.fst -o $@

lexic.fst : lexic-aff.lexc $(LEX) Makefile
	hfst-lexc -E -f openfst-tropical -o $@ $< $(LEX)

lexic-aff.lexc : ../ofi-affixes.csv ../affixes2analysis.py
	python3 ../affixes2analysis.py -e $< $@

lexic-s.lexc : lexic-s.entries
	python3 entries2lexc.py Nouns < $< > $@

lexic-a.lexc : lexic-a.entries
	python3 entries2lexc.py Adjectives < $< > $@

lexic-p.lexc : lexic-p.entries
	python3 entries2lexc.py Particles < $< > $@

lexic-v.lexc : lexic-v.entries
	python3 entries2lexc.py Verbs < $< > $@

lexic-firstpart.lexc : lexic-sgnom.words lexic-sggen.words
	cat $+ | python3 firstpart2lexc.py > $@

$(ANALYSES) : $(DATA)/$(ID)-corpus.words $(OLDANALYSER)
	hfst-lookup -i $(OLDANALYSER) -I $< | \
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
	rm -f $(ID)-*.fst
	rm -f $(ID)-*.ofst
	rm -f $(ID)-*.lexc

distclean : clean 
	rm -f $(ID)-corpus.big.analyses


