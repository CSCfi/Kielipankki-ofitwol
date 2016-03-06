import re, csv, sys
from featdic import *

rdr = csv.DictReader(sys.stdin, delimiter=',')
prevID = ",,"
for r in rdr:
    if r['NEXT'] == '' or r['NEXT'][0] == '!':
        continue
    id = prevID if r['ID'] == '' else r['ID']
    if prevID != id:
        prevID = r['ID']
        print("LEXICON %s" % id)
#    if r['FEAT'] == '' and r['BASEF'] == '':
#        r['BASEF'] = r['MPHON']

#    if r['FEAT'] != '':
#        f = '+' + '+'.join(re.split(" +", r['FEAT']))
#    else: f = ''
    if r['FEAT'] == '':
        f = ''
    else:
        fl = re.split(" +", r['FEAT'])
        al = [featDic[item] + '.' + item for item in fl]
        #al = map(attF, fl)
        f = '@P.' + '@@P.'.join(al) + '@'
    if ('FLAG' in r) and r['FLAG'] != '':
        g = '@' + '@@'.join(re.split(" +", r['FLAG'])) + '@'
    else:
        g = ''
    for n in re.split(" +", r['NEXT']):
        if n != '':
            if r['BASEF'] + f == r['MPHON']:
                print("{}{}{} {};".format(r['BASEF'], f, g, n))
            else:
                print("{}{}{}:{}{}{} {};".format(f, g, r['BASEF'],
                                                 f, g, r['MPHON'], n))

