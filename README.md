# ofitwol
Open Finnish Two-Level morphological analyzer based on the HFST finite-state transducer tools and the new two-level rule compiler twol-comp.  OFITWOL makes heavy use of two-level rules in order to make it easy to modify and use for a variety of purposes.

See https://pytwolc.readthedocs.io/en/latest/ofitwol.html for more information on the goals and plans for this project and the methods and principles used for establishing the lexical representations for word stems and affixes as well as the methods in finding the two-level rules.  There is just one stem in the lexicon for nouns, verbs and adjectives and just one set of endings applicable to all lexemes.  The surface representations are accounted for using two-level rules.

See https://github.com/hfst/hfst for more information on the HFST Helsinki Finite-State Transducer tools such as hfst-compose, hfst-lexc, etc. 

Ofitwol is related to OMORFI (by Tommi Pirinen et al.) an open Finnish morphological analyzer based on the HFST tools, although OFITWOL and OMORFI share neither rules, lexicon nor code.  See https://github.com/flammie/omorfi for more information on OMORFI.

For some information on installing OFITWOL itself see the wiki page https://github.com/koskenni/ofitwol/wiki but most of the dicumentation of OFITWOL will appear in READTHEDOCS.

OFITWOL is in the development stages but one may well experiment with it.
