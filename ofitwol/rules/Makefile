
.SUFFIXES :
.INTERMEDIATE :
.PHONY=all clear errors test

rules=consonants.twol nounfinal.twol nouninternal.twol verbinternal.twol verbsuff.twol verbfinal.twol vowels.twol
varrules=$(rules) variation.twol nounendings.twol
normrules=$(rules) normalize.twol
varfsts=$(varrules:.twol=-var.fst)
normfsts=$(normrules:.twol=-norm.fst)

errors : all
	@if grep -F -C 3 'ERROR' *.log ; \
	  then echo "*** Correct the corresponding rule" ; \
	  else echo "No formal syntax errors detected in the rules" ; \
	fi
	@if grep -F -B 1 -A 3 'Some positive' *.log ; \
	  then echo "*** Check the corresponding rules and/or examples" ; \
	  else echo "All positive examples were accepted" ; \
	fi

all : rules-norm.fst rules-var.fst

rules-var.fst: $(varfsts)
	cat $(varfsts) > $@

rules-norm.fst: $(normfsts)
	cat $(normfsts) > $@

$(varfsts) : %-var.fst : %.twol definitions.twol examples-var.fst
	twol-comp -t 2 -o $@ -e examples-var.fst \
	      -r definitions.twol $< > $*-var.log

$(normfsts) : %-norm.fst : %.twol definitions.twol examples-norm.fst
	twol-comp -t 2 -o $@ -e examples-norm.fst \
             -r definitions.twol $< > $*-norm.log

$(varfsts) : %-var.fst : examples-var.fst

$(normfsts) : %-norm.fst : examples-norm.fst

%.tmp-twol : %.twol definitions.twol
	cat definitions.twol $< > $@

examples-var.fst : examples.pstr examples-var.pstr
	twol-examples2fst -i examples.pstr examples-var.pstr -o $@

examples-norm.fst : examples.pstr examples-norm.pstr
	twol-examples2fst -i examples.pstr examples-norm.pstr -o $@

clear :
	rm -f *.fst

test : errors
	twol-tester -e examples-var.fst -r rules-var.fst -l lost-var.log -w wrong-var.log
	twol-tester -e examples-norm.fst -r rules-norm.fst -l lost-norm.log -w wrong-norm.log

rules-var-discov.fst: rules-var-discov.twol
	twol-comp -r rules-var-discov.twol \
		-e $< -o $@ --recursion 9999999 \
		> rules-var-discov.log

rules-var-discov.twol: examples-discov.pstr
	# rm $@
	twol-discover.py $< \
		-d setdefs.twol \
		-r recips.json -m 3 -v 1 -s '' > $@
