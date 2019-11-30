.SUFFIXES :
.INTERMEDIATE :

LEX=$(ID)lexic-n.lexc $(ID)lexic-v.lexc $(ID)lexic-a.lexc $(ID)lexic-p.lexc  $(ID)lexic-firstpart.lexc
##$(ID)lexic-compo.lexc

ID=sktp/
ANALYZER=../ksk/ksk-analy.ofst
WORDS=~/Dropbox/lang/fin/sktp-2plus.words
ANALYSES=$(ID)corpus.analyses

analy : $(ID)analy.ofst $(LEX)

analyses : $(ANALYSES)

guess : ofi-guess-n.ofst ofi-guess-v.ofst

$(ID)analy.ofst: $(ID)lexic.fst ofi-rules.fst delete.fst Makefile
	hfst-compose-intersect -a -1 $< -2 ofi-rules.fst |\
	hfst-compose -2 delete.fst |\
	hfst-invert |\
	hfst-minimize -o $(ID)analy.fst
	hfst-fst2fst -w -i $(ID)analy.fst -o $@

$(ID)lexic.fst: ofi-analy-aff.lexc $(LEX) Makefile
	hfst-lexc -E -f openfst-tropical -o $@ ofi-analy-aff.lexc $(LEX)

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

guess.ofst : guess-n.fst guess-v.fst
	hfst-disjunct -1 guess-n.fst -2 guess-v.fst -o guess.fst
	hfst-fst2fst -i guess.fst -o $@ -w

guess-n.ofst: guess-lex-n.fst ofi-rules.fst Makefile
	hfst-compose-intersect -e -a -1 $< -2 ofi-rules.fst |\
	hfst-compose -2 delete.fst |\
	hfst-invert |\
	hfst-minimize -o guess-n.fst
	hfst-fst2fst -w -i guess-n.fst -o $@

guess-v.ofst: guess-lex-v.fst ofi-rules.fst Makefile
	hfst-compose-intersect -e -a -1 $< -2 ofi-rules.fst |\
	hfst-compose -2 delete.fst |\
	hfst-invert |\
	hfst-minimize -o guess-v.fst
	hfst-fst2fst -w -i guess-v.fst -o $@

guess-lex-n.fst: guess-lex-n.lexc ofi-guess-aff.lexc
	hfst-lexc -E -f openfst-tropical -o $@ ofi-guess-aff.lexc $<

guess-lex-v.fst: guess-lex-v.lexc guess-aff.lexc
	hfst-lexc -E -f openfst-tropical -o $@ guess-aff.lexc $<

guess-lex-n.lexc : ofi-guespat-n.entries
	python3 guespat2lexc.py < $< > $@

#ofi-guess-lex-n.lexc : ofi-pat-n.csv pat-proc.py
#	python3 pat-proc.py -m g -n Verbs $< > $@

guess-lex-v.lexc : ofi-pat-v.csv pat-proc.py
	python3 pat-proc.py -m g -n Verbs $< > $@

ofi-guess-aff.lexc: ofi-affixes.csv affixes2guessing.py
	python3 affixes2guessing.py $< $@

ofi-analy-aff.lexc: ofi-affixes.csv affixes2analysis.py Makefile
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
