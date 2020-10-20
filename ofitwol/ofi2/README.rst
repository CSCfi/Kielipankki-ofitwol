OFI2 - the second version of OFITWOL
====================================

In order to use this version of OFITWOL, one has to get a copy of this
directory, e.g. by cloning the ofitwol project.  One also has to have
a Python 3.4, 3.5, or 2.7 available and to install a package ``twol``
which contains a compiler for the two-level rules and some other
tools.

This directory is intended to be complete so that anybody can build a
OFITWOL that can be used if one has the HFST tools installed.  OFITWOL
can be made as threee versions, each of them is a separate FST.

The following command builds an *analyser* FST out of the rules, lexicon
entries and the affixes.::
   
   $ make analyse
   
This command produces a file ``ofitwol.ofst`` which can be used with
``hfst-lookup`` in the normal way, e.g. a word form ``katosta`` is
given to the lookup program which produces two analyses for the input
word::

  $ hfst-lookup -i ofitwol.ofst 
  > katosta
  katosta	katos+N+SG+PTV	0,000000
  katosta	katto+N+SG+ELA	0,000000


The following builds, from the same rules and lexicon source files, a
slightly different FST, ``ofimphon.ofst`` which, instead of a
conventional base form, gives a ``morphophonemic`` version of the base
form::
   
   $ make ofimphon
   
This version knows the same lexemes and forms as the first one but
gives the base forms as strings of morphophonemes::
  
  $ hfst-lookup -i ofimphon.ofst 
  > katosta
  katosta	kato{ØkØkk}s{ØeØeØ}{§}+N+SG+PTV	0,000000
  katosta	kat{tØ}o{§}+N+SG+ELA	0,000000

The morphophonemic base forms are actually almost the lexicon entries
of those words.  This kind of an analyser might be useful in the
development stages as one sees what kind entries are involved in the
analysed forms.

The following builds a ``guesser`` FST ofiguess.ofst which is used in
guessing new entries e.g. out of corpus data::
   
   $ make guesser
   
The FST takes as an input, inflected word forms and computes all
tentative entries which would be capabe to analyse the given word
form.  This is particularly useful when one tries to deduce new
entries to the lexicon from given unanalysed word forms.  The guesser, again, takes a word form as its input and, in this case, it produces a set of lexicon entries.  The correct entry is expected to be one of those entries guessed, e.g.::

  $ hfst-lookup -i ofiguess.ofst
  > lato
  lato	la{td}o /s;	10,000000
  lato	lat{tØ}o /v;	20,000000
  lato	la{td}o /a;	30,000000
  lato	lato /s;	40,000000

The guesses are given weights so that the ones with the least weights
are the best candidates for new entries.

All questions and comments are most welcome!
