=========================
Build an initial analyzer
=========================

The Makefile in this directory assumes that we have:

- One or more word lists produced out of text corpora.  The word lists
  reside in the directory ../../data/ and they have one word form per
  line and no other information on the lines.  The centra list is
  ``klk-corpus.words`` which is large but contains lots of OCR errors and
  also somewhat non-standard Early Modern Standard Finnish.

- A morphological analyzer made out of the vocabulary of non-compound
  headwords of *Nykysuomen Sanakirja*.  The analyzer FST
  ``ksk-analy.ofst`` which is built out of the possibly non-free list
  of words in KSK (*Reverse dictionary of Modern Standard Finnish*).

The Makefile has a recipe for building the KLK word list out of the
file available from Kielipankki by removing non-alphabetic entries and
deleting the frequency field.

The Makefile analyses the word list with ``hfst-lookup`` using the given morphological analyzer and produces a file ``klk-corpus.big.analy`` which contains some 122,774,930 lines out of which some 2,977,629 lines contained an analysis.  The file name contains ``.big.`` to signal that the file si too big to be stored as such in Github and therefore cannot be found from there.  The file contains lines such as::

  aakkoselle      aakko{ns}{eeØØ}{nØØØ} /s;+N+SG+ALL      0,000000
  aakkosellemme   aakko{ns}{eeØØ}{nØØØ} /s;+N+SG+ALL+PL1  0,000000
  aakkosellfll    aakkosellfll+?  inf
  aakkoselli      aakkoselli+?    inf
  aakkoselliben   aakkoselliben+? inf

Two first lines were recognized by the analyzer and given an entry as
a result plus the grammatical features that describe the inflectional
form of the word form.  The first column is the word form that was
analyzed and the last column contains a weight which is irrelevant at
this stage.  The last three lines were not recognized by the analyzer
which is indicated by the infinite weight ``inf``.  The rejected words
happen to be obvious errors, and they cause no harm for the process.

The Makefile can then produce initial LEXC lexicons out of
``klk-corpus.big.analy`` by collecting selectively some results of the
analysis, e.g. from the above examples, e.g.  entry
``aakko{ns}{eeØØ}{nØØØ} /s`` would be taken as a noun entry into
``klk-lexic-s.entries``.  Similarly, the Makefile collects verbal,
adjectival, and particle entries into respective files.  These entries
need a bit formatting and processing in order to become valid LEXC
files which is done by a short Python script
``../affixes2analysis.py``.

In order to handle compound words, the Makefile collects, from the
analyzed file, all word forms which are analyzed as nominative
singular or genitive singular nouns.  They are processed into LEXC
entries and stored into a file ``klk-firstpart.lexc``.  These words
are then used for restricted compoundin whrere they may start a word
and continue to any entry in the Noun sublexicon.  Other nouns are not
allowed to form compound words (at this stage).

One still needs the definitions for affixes and their sequencing,
which are free abd located in ``../ofi.affixed.csv``.  That file is
free software/data as well as all files produced by the Makefile.

In addition to the LEXC parts described above, the free
``../ofi-rules.twolc`` is used for building the FST for analysing
words.


