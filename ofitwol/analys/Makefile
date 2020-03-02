.SUFFIXES :
.INTERMEDIATE :
.PHONY=analy analyses

ID=klk
OLDANALYSER=../../ksk/ksk-analy.ofst
RULEFST=../ofi-rules.fst
AFF=analy
DATA=../../data
LEX=$(ID)-lexic-s.lexc $(ID)-lexic-v.lexc $(ID)-lexic-a.lexc \
    $(ID)-lexic-p.lexc $(ID)-lexic-firstpart.lexc
##$(ID)-lexic-compo.lexc
ANALYSES=$(ID)-corpus.big.analyses

analyses : $(ANALYSES)
analy : $(ID)-analy.ofst $(LEX)

$(ID)-analy.ofst : $(ID)-lexic.fst $(RULEFST) delete.fst Makefile
	hfst-compose-intersect -a -1 $< -2 $(RULEFST) |\
	hfst-compose -2 delete.fst |\
	hfst-invert |\
	hfst-minimize -o $(ID)-analy.fst
	hfst-fst2fst -w -i $(ID)-analy.fst -o $@

$(ID)-lexic.fst : ../analy-aff.lexc $(LEX) Makefile
	hfst-lexc -E -f openfst-tropical -o $@ $< $(LEX)

../analy-aff.lexc : ../ofi-affixes.csv ../affixes2analysis.py
	python3 ../affixes2analysis.py -e $< $@

$(ID)-lexic-s.lexc : $(ID)-lexic-s.entries
	python3 entries2lexc.py Nouns < $< > $@

$(ID)-lexic-s.entries : $(ANALYSES)
	egrep '/s;' $< | \
	cut -f 2 | cut -d ';' -f 1 | sort -u > $@

$(ID)-lexic-a.lexc : $(ID)-lexic-a.entries
	python3 entries2lexc.py Adjectives < $< > $@

$(ID)-lexic-a.entries : $(ANALYSES)
	egrep '/a;' $< | \
	cut -f 2 | cut -d ';' -f 1 | sort -u > $@

$(ID)-lexic-p.lexc : $(ID)-lexic-p.entries
	python3 entries2lexc.py Particles < $< > $@

$(ID)-lexic-p.entries : $(ANALYSES)
	egrep '/p[a-z]*;' $< | \
	cut -f 2 | cut -d ';' -f 1 | sort -u > $@

$(ID)-lexic-v.lexc : $(ID)-lexic-v.entries
	python3 entries2lexc.py Verbs < $< > $@

$(ID)-lexic-v.entries : $(ANALYSES)
	egrep '/v;' $< | \
	cut -f 2 | cut -d ';' -f 1 | sort -u > $@

$(ID)-lexic-firstpart.lexc : $(ID)-sgnom.words $(ID)-sggen.words
	cat $+ | python3 firstpart2lexc.py > $@

$(ID)-sgnom.words :$(ANALYSES)
	egrep '/s;\+N\+SG\+NOM\s' $< | cut -f 1 | sort -u > $@

$(ID)-sggen.words : $(ANALYSES)
	egrep '/s;\+N\+SG\+GEN\s' $< | cut -f 1 | sort -u > $@

$(ANALYSES) : $(DATA)/$(ID)-corpus.words $(OLDANALYSER)
	hfst-lookup -i $(OLDANALYSER) -I $< | \
		egrep '..' > $@

$(RULEFST) : ../ofi-examples.pstr ../ofi-rules.twol
	twol-comp -t 2 -w ofi-wrong.fst -l ofi-lost.fst -o $@ \
		$+ > ofi-rules.log

delete.fst :
	echo "Ø -> 0" | hfst-regexp2fst -o $@

$(DATA)/klk-corpus.words : $(DATA)/klk_fi_1grams_all
	egrep '^ *[0-9]+ [a-zåäöšž][-a-zåäöšž'"'"']+[a-zåäöšž]$$' $< | \
	tr -d ' 0-9' | \
	sort -u > $@

$(DATA)/vns-corpus.words : $(DATA)/vns-freq.text
	cut -d ' ' -f 3 $< | \
	tr -d '0-9' | \
	egrep "^[a-zåäöšž]+$$" | \
	sort | uniq > $@

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
	rm -f $(ID)-*.entries

distclean : clean 
	rm -f $(ID)-corpus.big.analyses


