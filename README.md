# ofitwol
Open Finnish Two-Level morphological analyzer based on the HFST finite-state transducer tools.

See https://kitwiki.csc.fi/twiki/bin/view/KitWiki/HfstHome for more information on the HFST Helsinki Finite-State Transducer tools such as hfst-twolc, hfst-lexc, etc. 

Ofitwol is related to OMORFI (by Tommi Pirinen et al.) an open Finnish morphological analyzer based on the HFST tools, see https://github.com/flammie/omorfi for more information on OMORFI.

In my oppinion, OFITWOL appears to differ from OMORFI in some respects:

(1) Whereas OMORFI aims to follow the current norm of the Finnish language by excluding less frequent inflectional forms, OFITWOL aims to be tolerant and accepts wider sets of forms that were used some 50 or 100 years ago.

(2) OFITWOL aims to be more flexible so that a researcher may adjust it to accept even more dialectal variation or modify it for the purposes of historical and comparative linguistics.

(3) OMORFI aims to cover the vocabulary of present day Finnish as completely as possible whereas there are presently no plans to make OFITWOL become a practical spelling checker.

(4) In generation mode, OMORFI is prepared to produce the most preferred inflectional form (which is essential for using it as a part of machine translation into Finnish). OFITWOL has no such capabilities.

OFITWOL is in the development stages and it is capable of handling Finnish verbal and nominal inflection. Python scripts for converting entries from "Nykysuomen sanalista" and "Suomen kielen käänteissanakirja" to OFITWOL exist at this point, March 6th, 2016.
