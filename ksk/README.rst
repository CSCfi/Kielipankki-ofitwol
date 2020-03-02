============================================
Compiling a FST from Käänteissanakirja (KSK)
============================================

The Makefile needs:

1. A test file of pair strings ``ofi-renamed.pstr`` (which comes from
   the process of alignment using the package ``twol``.)

2. Two-level rules ``ofi-rules.twol``

These are freely available in source form in this repository and located in this directory.

3. The files which contain the headwords and their inflectional class
   numbers from *Suomen kielen käänteissanakirja* (KSK)(Reverse
   Dictionary of Modern Standard Finnish.  The files ksk-n.dic,
   ksk-a.dic, ksk-v-dic and ksk-p.dic are not free and cannot be
   included in the public repository.  Fortunately, these files can be
   used for creating a free version OFITWOL which covers much of the
   vocabulary of KSK and large areas beyond KSK.

4. Conversion patterns (``ksk-pat-na.csv``, ``ksk-pat-v.csv``) which
   use the shape of headwords and the number of the inflection class
   in transforming the headword into a two-level lexicon entry with
   morphophonemes.

5. A CSV file ``ofi-affixes.csv`` containing inflectional affixes,
   their morphophonological forms and sequencing information and the
   program ``affixes2analysis.py`` which converts the file into a LEXC
   file of the affixes..

The conversion programs and patterns etc. are nevertheless documented
and published here for other scholars and researchers who might have
access to the no-open dictionary data.

The ``Makefile`` is responsible for building an analysing program out
of the ksk-*-dict file in steps:

1. Conversion patterns are converted into LEXC format files by
   ``pat-proc.py``.

2. The LEXC format patterns are compiled into FSTs.

3. The KSK .dic files are converted into LEXC format files where the
   lexicon entries now are represented with morphophonemes.

4. The two-level rule file is compiled into a FST file.

5. The affix file is converted into a LEXC file.

6. The LEXC files are compiled into a FST.

7. The rule file is compiled into a FST.

8. The compiled LEXC file is compose-intersected with the rule FST
   file, inverted and optimized file ``ksk-analy.ofst`` for lookup.

The analyzer produces following kinds of results (the second column)
from input word forms (as the first column)::

  katossa    kat{tØ}o /s;+N+SG+INE                 0,000000
  katosta    kato{ØkØkk}s{ØeØeØ} /s;+N+SG+PTV      0,000000
  katosta    kat{tØ}o /s;+N+SG+ELA                 0,000000
  katostaan  kato{ØkØkk}s{ØeØeØ} /s;+N+SG+PTV+SG3  0,000000
  katostaan  kat{tØ}o /s;+N+SG+ELA+SG3             0,000000
  katosten   kato{ØkØkk}s{ØeØeØ} /s;+N+PL+GEN      0,000000
  katot      kat{tØ}o /s;+N+PL+NOM                 0,000000

The net result of the lookup is an entry for the underlying headword
followed by a semicolon and a set of inflectional tags which
determines the grammatical form of the word form.  The entry contains
information for determining a reasonably correct human readable
headword if one appends the appropriate base form ending and uses the
two-level rules in reverse direction.
