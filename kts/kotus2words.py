import sys, csv, re

dd = {
    '1':[(r"([ouyö])$", r">\1", '01'),  # valo, laukku
         (r"([ouyö])t$", r"<\1", '01')],  # aivot, opinnot
    '2':[(r"([ouyö])$", r"\1", '02'),  # palvelu
         (r"([ouyö])t$", r"\1", '02')],  # pippalot
    '3':[(r"([aeiouyäö][aeiouyäåö])$", r"\1", '03'),  # valtio
         (r"([aeiouyäö][aeiouyäåö])t$", r"\1", '03')],  # kapiot
    '4':[(r"(kk)([oö])$", r"\1>\2", '04')],  # laatikko
    '5':[(r"([bcdfghjklmnpqrsšvwxzž])$", r"\1", '05C'),  # kalsium, vorscmack
         (r"([bcdfghjklmnpqrsštvwxzž])i$", r"\1>{ie}", '05'),  # risti, vati
         (r"([aeouyäö]t)$", r"\1", '05C'),  # offset, beat
         (r"^(kredit|sanskrit|tilsit)$", r"\1", '05C'),
         (r"it$", r"<{ie}", '05')],  # paarit, juomingit
    '6':[(r"([bcdfghjklmnpqrsšvwxzž])$", r"\1", '06C'),  # kassler
         (r"([bcdfghjklmnpqrsštvwxzž])i$", r"\1{ie}", '06'),  # paperi
         (r"([aeouyäö]t)$", r"\1", '06C'),  # 
         (r"it$", r"{ie}", '06')],  # kekkerit
    '7': [(r"i$", r">{e}", '07'),   # lehti, ovi
          (r"et$", r"<{e}", '07')],  # länget, sakset
    '8': [(r"e$", r">e", '08'), # nalle
          (r"et$", r"<e", '08')],
    '9': [(r"aika$", r"a{I}{k}{ao}", '09'),
          (r"a$", r">{ao}", '09'), # kala, laiha
          (r"at$", r"<{ao}", '09'), 
          (r"ä$", r">{äö}", '09'),
          (r"ät$", r"<{äö}", '09')],
    '1009': [(r"aika$", r"a{I}{k}{ao}", '09')],
    '10': [(r"poika$", r"po{I}{k}{a}", '10'),
           (r"pojat$", r"po{I}{k}{a}", '10'),
           (r"a$", r">{ae}", '10'), # koira, ovela
           (r"at$", r"<{a}", '10'), # oltavat
           (r"ä$", r">{ä}", '10'), # kehä
           (r"ät$", r"<{ä}", '10')], # käräjät
    '1010': [(r"poika$", r"po{I}{k}{a}", '10'),
             (r"pojat$", r"po{I}{k}{a}", '10')],
    '11': [(r"a$", r">", '11a'), # omena
           (r"ä$", r">", '11ä')], # mäkärä
    '12': [(r"a$", r"{ao}", '12'), # kulkija
           (r"at$", r"{ao}", '12'),
           (r"ä$", r"{äö}", '12'),
           (r"ät$", r"{äö}", '12')],
    '13': [(r"a$", r"{ao}", '13'), # katiska
           (r"at$", r"{ao}", '13'),
           (r"ä$", r"{äö}", '13'),
           (r"ät$", r"{äö}", '13')],
    '14': [(r"a$", r">{ao}", '14'), # solakka, ulappa, pohatta
           (r"at$", r"<{ao}", '14'), # rintsikat
           (r"ä$", r">{äö}", '14'), # ötökkä
           (r"ät$", r"<{äö}", '14')],
    '15': [(r"ea$", r"e{a}", '15'), # korkea
           (r"eä$", r"e{ä}", '15')], # römeä
    '17': [(r"([aeiouyäö])(\1)$", r"\1{V}", '17'), # suklaa, tienoo, riiuu
           (r"([aeiouyäö])(\1)t$", r"\1{V}", '17')], # talkoot, hynttyyt
    '18': [(r"([aeiouyäö])(\1)$", r"\1{V}", '18'), # maa, syy
           (r"([aeiouyäö])(\1)t$", r"\1{V}", '18'), # häät
           (r"([aeouyäö])i$", r"\1", '18i')], # voi, täi
    '19': [(r"uo$", r"", '19uo'),
           (r"yö$", r"", '19yö'),
           (r"ie$", r"", '19ie')],
    '20': [(r"([aeiouyäö])(\1)$", r"\1{V}", '20'), # filee
           (r"([aeiouyäö])(\1)t$", r"\1{V}", '20')], # bileet
    '23': [(r"i$", r"{e}", '23'), # tiili
           (r"et$", r"{e}", '23')],
    '24': [(r"i$", r"{e}", '24'), # uni
           (r"et$", r"{e}", '24')],
    '25': [(r"mi$", r"", '25'), # lumi toimi
           (r"met$", r"", '25')],
    '26': [(r"i$", r"{e}", '26'), # pieni kieli
           (r"et$", r"{e}", '26')],
    '27': [(r"si$", r"", '27'), (r"det$", r"", '27')],
    '28': [(r"lsi$", r"", '28lsi'), # jälsi
           (r"nsi$", r"", '28nsi'), # ponsi
           (r"rsi$", r"", '28rsi')], # hirsi
    '29': [(r"psi$", r"", '29')], # lapsi
    '30': [(r"tsi$", r"", '30')],
    '32': [(r"(el)$", r"\1", '32'), # nivel sävel
           (r"(en)$", r"<\1", '32'), # ien siemen
           (r"([aä]r)$", r"<\1", '32')], # sisar tytär opettajatar
    '33': [(r"kerroin$", r"ker{tr}o{I}", '33'), # kerroin - astev. paikka!
           (r"(i)n$", r"<\1", '33'), # kytkin kaadin puin
           (r"(ä)n$", r"<\1", '33'), # sydän
           (r"(i)met$", r">\1", '33')], # näkimet
    '34': [(r"alaston$", r"alasto", '34'), # alaston (ainoa astev:ton)
           (r"t([oö])n$", r"t<\1", '34')], # onneton työtön
    '35': [(r"lämmin$", r"lämm<i", '35')], # lämmin
    '36': [(r"in$", r"i", '36')], # sisin
    '37': [(r"vasen$", r"vase", '37')], # vasen
    '38': [(r"nen$", r"", '38')], # nainen aikainen
    '39': [(r"s$", r"", '39'), # vastaus
           (r"kset$", r"", '39')], # kälykset
    '40': [(r"(u|y)s$", r"\1", '40')], # kalleus
    '41': [(r"([aäuyei])s$", r"<\1", '41'),  # vieras, rengas
           (r"(a)at$", r">\1", '41'),  # tikkaat
           (r"(y)yt$", r">\1", '41')],  # rynttyyt
    '42': [(r"mies$", r"mie", '42')], # mies
    '43': [(r"(u|y)t$", r"<\1", '43'), (r"$", r"", '')], # ohut airut immyt
    '44': [(r"kevät$", r"kevä", '44')],
    '47': [(r"(u|y)t$", r"", '47'),
           (r"eet$", r"", '47')],
    '48': [(r"e$", r"<e", '48'), # hame
           (r"(i|u)$", r"\1", '48'), # ori, kiiru
           (r"eet$", r">e", '48')], # alkeet
    '49': [(r"auer$", r"au<er", '49auer'), # auer
           (r"([aäe][lnr])$", r"<\1", '49C'), # askel ommel
           (r"e$", r"e", '49e')], # askele ompele
    'XX': [(r"$", r"", ''), (r"$", r"", '')]
    }
#   '': [(r"$", r"", ''), (r"$", r"", '')],

def fixPluralAndMarkGradation(BAS, INFL, GR, POS):
    if INFL in dd:
        patternList = dd[INFL]      # list of patterns for this infl class
    else: return("***", "***")
    for (pattern,replacement,contClass) in patternList:
        (ss,replacementCount) = re.subn(pattern, replacement, BAS)
        if (replacementCount > 0): # substitution succeeded
            if GR == "0":          # undo the marking, no gradation
                ss = re.sub(r"[<>]", "", ss)
            return(ss, POS + contClass)
    return("***", "***")

compounds = {}
cf = open("../ofitwol/compounds.txt", "r")
for cw in cf:
    clncw = re.sub(r"[|_]", r"", cw[:-1])
    compounds[clncw] = cw[:-1]


rdr = csv.reader(sys.stdin, delimiter=',')
wtr = csv.writer(sys.stdout, delimiter=',')

wtr.writerow(["HEADWORD", "WORD", "NEXT", "FEAT", "DERFROM", "GRAD"])

for entry in rdr:
    if len(entry)<2: continue   # it is a comment or something and is skipped
    base = compounds[entry[0]] if entry[0] in compounds else entry[0]
    infl = entry[1]
    if not infl in dd: continue # it is a comment or something and is skipped
    if not re.match("^\w*$", entry[0]):
        continue # näitä kaikkia ei saa heittää pois enää jatkossa !!!
    gr = entry[2]
    wclass = entry[3]
    (stem, cont) = fixPluralAndMarkGradation(base, infl, gr, wclass)
    if stem == "***" or not (wclass == 'N' or wclass == 'A'):
        continue
    wtr.writerow([entry[0], stem, cont, '', '', gr])
        
