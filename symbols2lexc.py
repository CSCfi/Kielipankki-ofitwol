import sys, csv, re

rdr = csv.DictReader(sys.stdin, delimiter=',')
lexcF = open("morphophonemes.lexc", mode='w')
rulF = open("alpha.twolc", mode='w')
#exaF = open("test.m2s.pstr", mode='w')
for r in rdr:
    l = r['LEXICAL']
    print(" %s" % l, end=' ', file=lexcF)
    ex = r['EXAMPLES']
    #print(ex, file=exaF)
    for s in re.split(" +", r['SURFACE']):
        ll = re.sub(r"([{}_&-\<=>])", r"%\1", l)
        print(" %s:%s" % (ll, s),  end='', file=rulF)
    print(file=rulF)
print(file=lexcF)
