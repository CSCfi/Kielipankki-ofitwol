summary = """Reads CVS table describing the feature structure and
outputs three files: 'featlex' to be included in the LEXC lexicon,
'multich' to be inculded in the TWOLC rules, and 'featdic' to be
included in the cvs2twolc.py converter.
"""

import sys, csv, re, argparse

rdr = csv.DictReader(sys.stdin, delimiter=',')

featDic = {}
categSet = set()

prev = ',,,'
attname = ''
def attr(item):
    m = re.match(r"^([A-Z0-9]+)[.]([A-Z0-9]+)$", item)
    if m != None:
        return(m.group(1,2,0))
    else:
        return(attname, item, attname + '.' + item)

argpars = argparse.ArgumentParser(description=summary)
argpars.add_argument('-l', '--featlex', default='feats.lexc',
                     help='file for sublexicon output')
argpars.add_argument('-m', '--multich', default='mulsym.lexc',
                     help='file for multicharacter symbols for flag diacritics')
argpars.add_argument('-f', '--featdic', default='featdic.py',
                     help='Python module to be imported by cvs2twolc.py')
par = vars(argpars.parse_args())
#print(par)

flx = open(par['featlex'], mode='w')
for r in rdr:
    attname = r['ATTRIBUTE']
    if attname == '':
        attname = prev
    if attname != prev:
        prev = attname
        print("LEXICON {}".format(attname), file=flx)
    if r['FEATS'] == '':
        print("@D.{}@:@D.{}@ {};".format(attname, attname, r['NEXT']),
              file=flx)
        categSet.add(attname)
    else:
        featlist = re.split(" +", r['FEATS'])
        tuplelist = [attr(x) for x in featlist]
        namvallist = []
        vallist = []
        for (aname,fval,namval) in tuplelist:
             namvallist.append(namval)
             vallist.append(fval)
             featDic[fval] = aname
        d = '@R.' + '@@R.'.join(namvallist) + '@'
        g = '+' + '+'.join(vallist)
        print("{}{}:{} {};".format(d, g, d, r['NEXT']), file=flx)
        for t in featlist:
            #featDic[t] = attname
            categSet.add(attname)
flx.close()

mcs = open(par['multich'], mode='w')
print("Multichar_Symbols", file=mcs)
vals = featDic.keys()

for kf in sorted(vals):
    print(" @P.{}.{}@ @R.{}.{}@".format(featDic[kf], kf, featDic[kf], kf),
          file=mcs)

for ka in sorted(list(categSet)):
    print(" @D.{}@".format(ka), file=mcs)

for kf in sorted(vals):
    print(" +{}".format(kf), file=mcs)

print(file=mcs)
mcs.close()

fdicf = open(par['featdic'], mode='w')
print('featDic = ', featDic, file=fdicf)

