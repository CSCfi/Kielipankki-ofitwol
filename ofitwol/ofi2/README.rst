OFI2 - the second version of OFITWOL
====================================

This directory should be complete enough to let anybody build several kinds of FSTs.
The following builds an analyser FST out of the rules, lexicon entries and the affixes.::
   
   $ make analyse
   
The ofitwol.ofst takes as input a lower case Finnish word form and gives as output the possible analyses
i.e. a base form plus a sequence of grammatical features which identify the particular form in which the 
word form is.

The following builds a similar FST, ofimphon.ofst which, instead of a conventional base form, gives
a morphophonemic version of the base form::
   
   $ make ofimphon
   
This kind of an analyser might be useful in the development stages as one sees what kind entries the analyser produces.
The ofitwol.ofst is actually produced out of the morphophonemic analyser ofimphon.fst by composing it and the rule FST.

The following builds a guesser FST ofiguess.ofst which is used in guessing new entries e.g. out of corpus data::
   
   $ make guesser
   
The FST takes as an input, inflected word forms and outputs all tentative entries which would analyse this word form. 
Each output contains the tentative entry plus the inflectional features.  This FST can be used in guessing new entries
out of lists of word forms which were not recognised by the ofitwol.ofst analyser.

All questions and comments are most welcome!
