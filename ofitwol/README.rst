=======
OFITWOL
=======

This directory contains some central files, a set of programs useful
for developing OFITWOL lexicons and subdirectroies for making FST
analyzers and guessers to be used e.g. with hfst-lookup.

- ofi-rules.twol and its compiled form, ofi-rules.fst reside in this
  directory.  If the rules will be updated, the Makefiles in
  subdirectory guess is capable for recompiling the rules.

  This directory also contains ofi-aff.csv which contains inflectional
  affixes and information of their possible combinations.  The file is
  needed when building analysers or guessers.

- Subdirectory ``guess`` contains the patterns for guessing entries of
  Early Modern Standard Finnish nouns, adjectives and verbs as well as
  the Makefile to process and compile the patterns into a guesser FST.
  The guesser FST takes as input a word form and produces as output a
  set of lexicon entries which would accept the given word form.  One
  of the entries is expected to be the correct one.

- Subdirectory ``analys`` which contains an initial free OFITWOL
  lexicon consisting of sets of entries for nouns, adjectives, verbs,
  particles and first parts of noun compounds.  There is a Makefile
  which produces these out of some big corpora and using a set of
  headwords from the Reverse Dictionary of Modern Standard Finnish.

Programs:

- ``guesssfromwords.py`` uses the guessing FST in order to deduce
  lexical entries out of a list of word forms not analysed by the
  existing lexicon.  The program produces 
