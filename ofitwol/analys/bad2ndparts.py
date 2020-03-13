import sys

firstparts = {}

for lineln in sys.stdin:
    line = lineln.strip()
    if line.count("\t") != 2:
        continue
    #print("line = '" + line + "'")###
    [word, analysis, weight] = line.split("\t")
    #print("word, analysis, weight =", word, analysis, weight)###
    if weight.strip() == "inf":
        continue
    if not "§" in analysis:
        continue
    entry, semicolon, features = analysis.partition(";")
    #print("entry, semicolon, features =", entry, semicolon, features)###
    firstpart, boundary, secondpart = entry.partition("{§}")
    #print("firstpart, secondpart =", firstpart, secondpart)###
    if secondpart not in firstparts:
        firstparts[secondpart] = set()
    firstparts[secondpart].add(firstpart)

#print(firstparts)###
    
for secondpart, firstpart_set in sorted(firstparts.items()):
    if len(firstpart_set) >= 50 and len(firstpart_set) < 100:
        firstpart_lst = sorted(list(firstpart_set))
        print(secondpart, " ".join(firstpart_lst))
        print()
        
    
