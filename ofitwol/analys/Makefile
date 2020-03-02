.SUFFIXES :
.INTERMEDIATE :

ID=sktp/
ANALYZER=../ksk/ksk-analy.ofst
WORDS=~/Dropbox/lang/fin/sktp-2plus.words
ANALYSES=$(ID)corpus.analyses
AFF=analy
DATA=../../data

LEX=$(ID)lexic-n.lexc $(ID)lexic-v.lexc $(ID)lexic-a.lexc $(ID)lexic-p.lexc  $(ID)lexic-firstpart.lexc
##$(ID)lexic-compo.lexc

analy : $(ID)analy.ofst $(LEX)

analyses : $(ANALYSES)

guess : ofi-guess-n.ofst ofi-guess-v.ofst

$(ID)analy.ofst: $(ID)lexic.fst ofi-rules.fst delete.fst Makefile
	hfst-compose-intersect -a -1 $< -2 ofi-rules.fst |\
	hfst-compose -2 delete.fst |\
	hfst-invert |\
	hfst-minimize -o $(ID)analy.fst
	hfst-fst2fst -w -i $(ID)analy.fst -o $@

$(ID)lexic.fst: analy-aff.lexc $(LEX) Makefile
	hfst-lexc -E -f openfst-tropical -o $@ analy-aff.lexc $(LEX)

$(ANALYSES) : $(WORDS) $(ANALYZER)
	hfst-lookup -p -i $(ANALYZER) -I $(WORDS) -o $@

$(ID)lexic-n.entries : $(ANALYSES)
	egrep '/s;' $< | \
	cut -f 2 | cut -d ';' -f 1 | sort | uniq > $@

$(ID)lexic-n.lexc: $(ID)lexic-n.entries
	python3 entries2lexc.py Nouns < $< > $@

$(ID)lexic-a.entries : $(ANALYSES)
	egrep '/a;' $< | \
	cut -f 2 | cut -d ';' -f 1 | sort | uniq > $@

$(ID)lexic-a.lexc : $(ID)lexic-a.entries
	python3 entries2lexc.py Adjectives < $< > $@

$(ID)lexic-p.entries : $(ANALYSES)
	egrep '/p[a-z]*;' $< | \
	cut -f 2 | cut -d ';' -f 1 | sort | uniq > $@

$(ID)lexic-p.lexc : $(ID)lexic-p.entries
	python3 entries2lexc.py Particles < $< > $@

$(ID)lexic-v.entries : $(ANALYSES)
	egrep '/v;' $< | \
	cut -f 2 | cut -d ';' -f 1 | sort | uniq > $@

$(ID)lexic-v.lexc : $(ID)lexic-v.entries
	python3 entries2lexc.py Verbs < $< > $@

$(ID)n-sgnom.words :$(ANALYSES)
	egrep '/s;\+N\+SG\+NOM\s' $< | cut -f 1 | sort | uniq > $@

$(ID)n-sggen.words : $(ANALYSES)
	egrep '/s;\+N\+SG\+GEN\s' $< | cut -f 1 | sort | uniq > $@

$(ID)lexic-firstpart.lexc : $(ID)n-sgnom.words $(ID)n-sggen.words
	cat $(ID)n-sgnom.words $(ID)n-sggen.words | python3 firstpart2lexc.py > $@

ofi-rules.fst: ofi-rules.twol ofi-examples.pstr
	python3 ~/github/twol/twol.py -t 2 -v 1 -w ofi-wrong.fst -l ofi-lost.fst -o $@ ofi-examples.pstr $< > ofi-rules.log

delete.fst:
	echo "Ø -> 0" | hfst-regexp2fst -o $@

$(DATA)/klk-corpus.words : ../../data/klk_fi_1grams_all
	egrep "^ *[0-9]+ [a-zåäöšž][-a-zåäöšž']+[a-zåäöšž]$" klk_fi_1grams_all |\
	tr -d ' 0-9' | \
	sort > $@

clean:
	rm -f $(ID)*.fst
	rm -f $(ID)*.ofst
	rm -f $(ID)*.lexc
	rm -f $(ID)*.entries
	rm -f $(ID)n-*.words


