.SUFFIXES :
.INTERMEDIATE :

LEX=$(ID)lexic-n.lexc $(ID)lexic-v.lexc $(ID)lexic-a.lexc $(ID)lexic-p.lexc  $(ID)lexic-firstpart.lexc
##$(ID)lexic-compo.lexc

ID=sktp/
ANALYZER=../ksk/ksk-analy.ofst
WORDS=~/Dropbox/lang/fin/sktp-2plus.words
ANALYSES=$(ID)corpus.analyses
AFF=analy

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

guess-$(AFF).ofst : guess-$(AFF)-n.ofst guess-$(AFF)-a.ofst guess-$(AFF)-v.ofst Makefile
	hfst-disjunct -1 guess-$(AFF)-n.fst -2 guess-$(AFF)-a.fst |\
	hfst-disjunct -2 guess-$(AFF)-v.fst -o guess-$(AFF).fst
	hfst-fst2fst -i guess-$(AFF).fst -o $@ -w

guess-$(AFF)-n.ofst: guespat-$(AFF)-lex-n.fst ofi-rules.fst Makefile
	hfst-compose-intersect -e -a -1 $< -2 ofi-rules.fst |\
	hfst-compose -2 delete.fst |\
	hfst-invert |\
	hfst-minimize -o guess-$(AFF)-n.fst
	hfst-fst2fst -w -i guess-$(AFF)-n.fst -o $@

guess-$(AFF)-a.ofst: guespat-$(AFF)-lex-a.fst ofi-rules.fst Makefile
	hfst-compose-intersect -e -a -1 $< -2 ofi-rules.fst |\
	hfst-compose -2 delete.fst |\
	hfst-invert |\
	hfst-minimize -o guess-$(AFF)-a.fst
	hfst-fst2fst -w -i guess-$(AFF)-a.fst -o $@

guess-$(AFF)-v.ofst: guespat-$(AFF)-lex-v.fst ofi-rules.fst Makefile
	hfst-compose-intersect -e -a -1 $< -2 ofi-rules.fst |\
	hfst-compose -2 delete.fst |\
	hfst-invert |\
	hfst-minimize -o guess-$(AFF)-v.fst
	hfst-fst2fst -w -i guess-$(AFF)-v.fst -o $@

guespat-$(AFF)-lex-n.fst: guespat-n.lexc guess-aff.lexc Makefile
	hfst-lexc -E -f openfst-tropical -o $@ $(AFF)-aff.lexc $<

guespat-$(AFF)-lex-a.fst: guespat-a.lexc guess-aff.lexc Makefile
	hfst-lexc -E -f openfst-tropical -o $@ $(AFF)-aff.lexc $<

guespat-$(AFF)-lex-v.fst: guespat-v.lexc guess-aff.lexc Makefile analy-aff.lexc
	hfst-lexc -E -f openfst-tropical -o $@ $(AFF)-aff.lexc $<

guespat-a.lexc : guespat-a.entries guespat2lexc.py
	python3 guespat2lexc.py < $< > $@

guespat-n.lexc : guespat-n.entries guespat2lexc.py
	python3 guespat2lexc.py < $< > $@

guespat-v.lexc : guespat-v.entries guespat2lexc.py
	python3 guespat2lexc.py < $< > $@

guess-aff.lexc: ofi-affixes.csv affixes2guessing.py
	python3 affixes2guessing.py $< $@

analy-aff.lexc: ofi-affixes.csv affixes2analysis.py Makefile
	python3 affixes2analysis.py -e $< $@

ofi-rules.fst: ofi-rules.twol ofi-examples.pstr
	python3 ~/github/twol/twol.py -t 2 -v 1 -w ofi-wrong.fst -l ofi-lost.fst -o $@ ofi-examples.pstr $< > ofi-rules.log

delete.fst:
	echo "Ø -> 0" | hfst-regexp2fst -o $@

klk/sktp-rejected.fst : klk/sktp.rejected
	hfst-strings2fst -j -i $< | hfst-minimize -o $@

$(ID)words.fst : $(WORDS)
	hfst-strings2fst -j -i $< | hfst-minimize -o $@

clean:
	rm -f $(ID)*.fst
	rm -f $(ID)*.ofst
	rm -f $(ID)*.lexc
	rm -f $(ID)*.entries
	rm -f $(ID)n-*.words


features: ksk-zerofilled.csv
	cat $< | cut -d ',' -f 1 | cut -d ' ' -s -f 2,3 | tr ' ' '\n' | sort | uniq

rawlist: ksk-raw-examp.csv
	cat $< | cut -d ',' -f 4 | tr ' ' '\n' | sort | egrep '...' | uniq > raw_mphons.str
