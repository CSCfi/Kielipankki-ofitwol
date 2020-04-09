.SUFFIXES :
.INTERMEDIATE :
.PHONY=build analyse 

ID=sktp
MODE=mphon
ANALYSER=ofi$(MODE).ofst
RULEFST=ofi-rules-in.fst
AFF=analy
DATA=../../data

LEXB=base-s.lexc base-v.lexc base-a.lexc base-p.lexc base-noncomp-s.lexc

LEXB2=base-r.lexc lexic-firstpart.lexc lexic-n.lexc

LEXM=mphon-s.lexc mphon-v.lexc mphon-a.lexc mphon-p.lexc mphon-noncomp-s.lexc

LEXM2=mphon-r.lexc lexic-firstpart.lexc lexic-n.lexc

LEXG=guess-s.lexc guess-a.lexc guess-v.lexc

LEXG2=lexic-firstpart.lexc

ANALYSES=$(ID)-corpus-$(MODE).big.analyses

rules : ofi-rules-in.fst ofi-rules-out.fst

build : $(ANALYSER)

ofibase : ofibase.ofst

ofimphon : ofimphon.ofst 

guesser : ofiguess.ofst

analyse : $(ANALYSES)

ofibase.ofst : base-lex.fst $(RULEFST) delete.fst Makefile
	hfst-compose-intersect -a -1 $< -2 $(RULEFST) |\
	hfst-compose -2 delete.fst |\
	hfst-invert |\
	hfst-minimize |\
	hfst-fst2fst -w -o $@

ofitwol.ofst : ofimphon.fst ofi-rules-out.fst bound.fst ofimphon.ofst Makefile
	hfst-project -p out -i $< -o ofimphon-out.fst
	hfst-compose-intersect -1 ofimphon-out.fst -2 ofi-rules-out.fst -o ofitwol-tmp.fst
	hfst-compose -1 ofitwol-tmp.fst -2 delete.fst |\
	hfst-compose -2 bound.fst -o ofitwol-aux.fst
	hfst-compose -1 ofimphon.fst -2 ofitwol-aux.fst -o ofitwol-cps.fst
	hfst-minimize -i ofitwol-cps.fst -o ofitwol.fst
	hfst-fst2fst -w -i ofitwol.fst -o $@

ofimphon.ofst : mphon-lex.fst $(RULEFST) delete.fst Makefile
	hfst-compose-intersect -a -1 $< -2 $(RULEFST) |\
	hfst-minimize |\
	hfst-compose -2 delete.fst |\
	hfst-invert |\
	hfst-minimize > ofimphon.fst
	hfst-fst2fst -w -i ofimphon.fst -o $@

ofiguess.ofst : guess-lex.fst $(RULEFST) delete.fst Makefile
	hfst-compose-intersect -a -1 $< -2 $(RULEFST) |\
	hfst-compose -2 delete.fst |\
	hfst-invert |\
	hfst-minimize |\
	hfst-fst2fst -w -o $@

base-lex.fst : base-aff.lexc $(LEXB) $(LEXB2) Makefile
	hfst-lexc -E -f openfst-tropical -o $@ $< $(LEXB) $(LEXB2)

mphon-lex.fst : mphon-aff.lexc $(LEXM) $(LEXM2) Makefile
	hfst-lexc -E -f openfst-tropical -o $@ $< $(LEXM) $(LEXM2)

guess-lex.fst : guess-aff.lexc $(LEXG) $(LEXG2) Makefile
	hfst-lexc -E -f openfst-tropical -o $@ $< $(LEXG) $(LEXG2)

#guess-lex.fst : guess-aff.lexc $(LEXG) $(LEXG2) Makefile
#	hfst-lexc -f sfst $< $(LEXG) $(LEXG2) | hfst-fst2fst -t  -o $@

base-aff.lexc : ofi-affixes.csv affixes2lexc.py
	python3 affixes2lexc.py -m BASE < $< > $@

mphon-aff.lexc : ofi-affixes.csv affixes2lexc.py
	python3 affixes2lexc.py -m MPHON < $< > $@

guess-aff.lexc : ofi-affixes.csv affixes2lexc.py
	python3 affixes2lexc.py -m GUESS < $< > $@

$(LEXB) : base-%.lexc : lexic-%.entries ofi-rules-out.fst entries2lexc.py
	python3 entries2lexc.py -r ofi-rules-out.fst < $< > $@

base-r.lexc : lexic-r.entries ofi-rules-out.fst entries2lexc.py
	python3 entries2lexc.py -r ofi-rules-out.fst -c End < $< > $@

lexic-n.lexc : lexic-n.entries ofi-rules-out.fst entries2lexc.py
	python3 entries2lexc.py -r ofi-rules-out.fst -c End < $< > $@

lexic-firstpart.lexc : lexic-firstpart.words entries2lexc.py
	python3 entries2lexc.py -n FirstPart -c SecondPart < $< > $@

$(LEXM) : mphon-%.lexc : lexic-%.entries entries2lexc.py
	python3 entries2lexc.py < $< > $@

mphon-r.lexc : lexic-r.entries entries2lexc.py
	python3 entries2lexc.py -c End < $< > $@

$(LEXG) : guess-%.lexc : guess-%.entries entries2lexc.py
	python3 entries2lexc.py < $< > $@

$(ANALYSES) : $(DATA)/$(ID)-corpus.words $(ANALYSER)
	hfst-lookup -b 15 -i $(ANALYSER) -I $< | \
		egrep '..' > $@

ofi-rules-in.fst : ofi-examples-in.pstr ofi-rules-in.twol
	twol-comp -t 2 -w ofi-wrong.fst -l ofi-lost.fst -o $@ \
		$+ > ofi-rules-in.log

ofi-rules-out.fst : ofi-examples-out.pstr ofi-rules-out.twol
	twol-comp -t 2 -w ofi-wrong-out.fst -l ofi-lost-out.fst -o $@ \
		$+ > ofi-rules-out.log

ofi-rules-in.twol : ofi-rules.twol ofi-rules-extra-in.twol
	cat $+ > $@

ofi-rules-out.twol : ofi-rules.twol ofi-rules-extra-out.twol
	cat $+ > $@

ofi-examples-in.pstr : ofi-examples.pstr ofi-examples-extra-in.pstr
	cat $+ > $@

ofi-examples-out.pstr : ofi-examples.pstr ofi-examples-extra-out.pstr
	cat $+ > $@

delete.fst :
	echo "Ø -> 0" | hfst-regexp2fst -o $@

bound.fst : Makefile
	echo '[§+ -> 0 || _ [%+N | %+A | %+V | %+P | %+PRON | %+NUM]] .o. [%§ -> %_]' | hfst-regexp2fst -o $@

guesses : sktp-corpus-base.big.analyses
	egrep 'inf$$' sktp-corpus-base.big.analyses | \
	cut -f 1 > sktp-rejected.big.words
	hfst-lookup -i ofiguess.ofst -I sktp-rejected.big.words -o sktp-guessed.big.analyses
	python3 ../guessfromwords.py < sktp-guessed.big.analyses > sktp-guessed.big.entries

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


