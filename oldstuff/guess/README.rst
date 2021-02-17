=====================
Building guesser FSTs
=====================

This directory is for producing multi-purpose FSTs whose input is a
Finnish word form and the output is a set of possible LEXC entries which could
recognize the word form.  This mapping can be used for many purposes,
including interactive compilation of new lexicon entries and
harvesting large amounts of entries out of word lists from corpuses,
but suchprograms are in the directory above this one.

This directory contains a Makefile for creating the FSTs out of the following files in this directory:

- ``guespat-a.entries``, ``guespat-n.entries`` and ``guespat-v.entries`` which contain patterns for different types of inflection i.e. what kinds of morphophonemic representations Finnish LEXC entries can have.

Following files outside this directory are used for creating the
guesser FSTs:

- The compiled two-level rules (usually ``../ofi-rules.fst`` )

- The inflectional affixes and their sequencing information (usually
  ``../ofi-affixes.csv``)

- A program ``../affixes2analysis.py`` which converts the affix CSV
  file into a LEXC file which not only recognizes the affixes but also
  gives appropriate syntactic tags for the affixes.
