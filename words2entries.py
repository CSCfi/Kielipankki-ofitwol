"""Produces entries out of words by identifying the type and direction
of the consonant gradation and replacing the gradating consonant by 
an appropriate morphophoneme.
Copyright 2016 Kimmo Koskenniemi
Free software under GPL 3 License, see <http://www.gnu.org/licenses/>"""

import sys, csv, re

weaken = {
    'k':'{kØ}', 'kk':'k{kØ}', 'hk':'h{kØ}', 'lk':'l{kØ}', 'lkk':'lk{kØ}',
    'nk':'n{kg}', 'nkk':'nk{kØ}', 'rk':'r{kØ}', 'rkk':'rk{kØ}',
    'p':'{pv}', 'pp':'p{pØ}', 'lp':'l{pv}', 'lpp':'lp{pØ}',
    'mp':'m{pm}', 'mpp':'mp{pØ}', 'rp':'r{pv}', 'rpp':'rp{pØ}',
    't':'{td}', 'tt':'t{tØ}', 'ht':'h{td}', 'lt':'l{tl}', 'ltt':'lt{tØ}',
    'nt':'n{tn}', 'ntt':'nt{tØ}', 'rt':'t{tr}', 'rtt':'rt{tØ}'
}
strengthen = {
    '':'{kØ}', 'k':'k{kØ}', 'h':'h{kØ}', 'hj':'h{kj}',
    'lj':'l{kj}', 'l':'l{kØ}', 'lk':'lk{kØ}',
    'ng':'n{kg}', 'nk':'nk{kØ}','rj':'r{kj}', 'r':'r{kØ}', 'rk':'rk{kØ}',
    'v':'{pv}', 'p':'p{pØ}', 'lv':'l{pv}', 'lp':'lp{pØ}',
    'mm':'m{pm}', 'mp':'mp{pØ}', 'rv':'r{pv}', 'rp':'rp{pØ}',
    'd':'{td}', 't':'t{tØ}', 'hd':'h{td}', 'll':'l{tl}', 'lt':'lt{tØ}',
    'nn':'n{tn}', 'nt':'nt{tØ}', 'rr':'t{tr}', 'rt':'rt{tØ}'
}

grd0 = {"A":1, "B":1, "C":1, "D":1, "T":1}

def fixGradationMorphophoneme(BAS):
    """Set in the appropriate morphophoneme for the gradating stop in
    BAS where the position and direction of the gradation is marked by
    a > or < and the NSL gradation code GR indicates the alternation
    gradStop[GR].
    """
    m = re.match("^(.*[aeiouyäö])([dghjklmnprtv]*)([<>])(.*)$", BAS)
    if not m:
        return(BAS)
    (start,grad,dir,rest) = m.groups()
    if dir == '>':                       # weakening
        if grad not in weaken: print("***" + BAS); return(BAS)
        return(start + weaken[grad] + rest)
    if dir == '<':                       # strengthening
        if grad not in strengthen: print("***" + BAS); return(BAS)
        return(start + strengthen[grad] + rest)
    return(BAS)                          # no gradation

rdr = csv.DictReader(sys.stdin, delimiter=',')
wtr = csv.writer(sys.stdout, delimiter=',')

wtr.writerow(["ID", "NEXT", "MPHON", "FEAT", "BASEF", "FLAG"])

for entry in rdr:
    base =  entry['WORD']
    cont = entry['NEXT']
    if not re.match("^([^ ])*$", base):
        continue # näitä kaikkia ei saa heittää pois enää jatkossa !!!
    stem = fixGradationMorphophoneme(base)
    if stem == "***": continue
    #wtr.writerow(["Words", cont, re.sub(r"\|", r"§", stem), "", stem, ""])
    wtr.writerow(["Words", cont, re.sub(r"\|", r"§", stem), "",
                  entry['HEADWORD'], ""])

