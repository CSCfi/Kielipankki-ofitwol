import sys, csv, re

dd = {
    # 'V00':[(r"()$", r"\1", '/v')], #
    'V01':[(r"([ou])a$", r">\1", '/v'), # punoa, kiekua
           (r"([öy])ä$", r">\1", '/v')], # kiintyä
    'V02':[(r"aa$", r">{aØe}", '/v'), # muistaa, johtaa
           (r"ää$", r">{äØe}", '/v')], # kylvää, nyhtää
    'V03':[(r"taa$", r"{tds}{aØe}", '/v'), # kaataa, huutaa
           (r"tää$", r"{tds}{äØe}", '/v')], # pyytää, löytää
    'V04':[(r"taa$", r"{tds}{aØe}", '/v'), # soutaa
           (r"tää$", r"{tds}{äØe}", '/v')], # häätää
    'V05':[(r"ltaa$", r"l{tls}{aØe}", '/v'),  # puoltaa
           (r"ltää$", r"l{tls}{äØe}", '/v')],  # yltää
    'V06':[(r"rtaa$", r"r{trs}{aØe}", '/v'),  # murtaa
           (r"rtää$", r"r{trs}{äØe}", '/v')],  # piirtää
    'V07':[(r"rtaa$", r"r{trs}{aØe}", '/v')],  # sortaa
    'V08':[(r"ntaa$", r"n{tns}{aØe}", '/v'),  # pahentaa
           (r"ntää$", r"n{tns}{äØe}", '/v')],  # myöntää
    'V09':[(r"aa$", r">{aoe}", '/v')],  # kaivaa, ahtaa
    'V10':[(r"taa$", r"t>{aoØe}", '/v')],  # haastaa, laittaa
    'V11':[(r"taa$", r"t>{aoØe}", '/v')],  # paistaa, taittaa
    'V12':[(r"taa$", r"{trs}{aoØe}", '/v')],  # saartaa
    'V13':[(r"kea$", r"k>{eiØ}", '/v')],  # laskea
    'V14':[(r"tea$", r"{tns}>{eiØ}", '/v')],  # tuntea
    'V15':[(r"tea$", r"{tds}{eiØ}", '/v')],  # potea
    'V16':[(r"lähteä$", r"lä", 'lä-hte/v')],  # lähteä
    'V17':[(r"ia$", r">{iØ}", '/v')],  # sallia, oppia
    'V18':[(r"([aäoö])id[aä]$", r"\1{iØ}", '/v')],  #  voida, naida, yksilöidä
    'V19':[(r"aada$", r"a{VØ}", '/v'),  # saada
           (r"äädä$", r"ä{VØ}", '/v')],  # jäädä
    'V20':[(r"myydä$", r"my{VØ}", '/v')],  # myydä
    'V21':[(r"uoda$", r"{uØ}o", '/v'),  # juoda
           (r"yödä$", r"{yØ}ö", '/v')],  # lyödä
    'V22':[(r"iedä$", r"{iØ}e", '/v')],  # viedä
    'V23':[(r"äydä$", r"ä", 'kä-y/v')],  # käydä
    'V24':[(r"(a?is)ta$", r"<\1{eØ}", '/v'),  # nuolaista, vilaista
           (r"(ä?is)tä$", r"<\1{eØ}", '/v')],  # vikistä, läväistä
    'V25':[(r"ll[aä]$", r"l{eØ}", '/v')], # tulla, niellä
    'V26':[(r"rr[aä]$", r"r{eØ}", '/v')], # purra, pierrä
    'V27':[(r"nn[aä]$", r"n{eØ}", '/v')], # mennä, panna
    'V28':[(r"([ei]l)l[aä]$", r"<\1{eØe}", '/v')], # katsella, hymähdellä
    'V29':[(r"ll[aä]$", r"l{eØe}", '/v')], # arvailla, pälyillä
    'V30':[(r"([oö])id[aä]$", r">\1", 'haravo-i/v')],  # haravoida, näpelöidä
    'V31':[(r"it[aä]$", r"i", 'vali-tse/v')], # valita, tilkitä
    'V32':[(r"st[aä]$", r"", 'juo-kse/v')],  # juosta, piestä
    'V33':[(r"hd[aä]$", r"", 'nä-ke/v')],  # nähdä, tehdä
    'V34':[(r"([ae])t[aä]$", r"<\1", 'ale-ne/v')],  # aleta, hapata, synketä
    'V35':[(r"([aä])t[aä]$", r"<\1", 'sala-V/v')],  # salata, vallata, iätä
    'V36':[(r"et[aä]$", r"<e", 'katke-A/v')],  # katketa, todeta, teljetä
    'V37':[(r"it[aä]$", r"<i", 'selvi-A/v')],  # selvitä, kuumita, lämmitä, siitä
    'V38':[(r"([oöuy])t[aä]$", r"<\1", 'koho-A/v')],  # kohota, seota, ryöpytä
    'V39':[(r"([uy])t[aä]$", r"<\1", 'halu-A/v')], # haluta, öljytä
    'V40':[(r"([aä])t[aä]$", r"<\1", 'pala-V/v')],  # palata, kaivata, hylätä, 
    'V41':[(r"^([^äyöe]*)ist[aä]$", r"\1", 'kih-ise/v'),  # kihistä, kohista
           (r"istä$", r"", 'öl-ise/v')], # ähistä, ölistä
    'V42':[(r"nt[aä][aä]$", r"", 'rake-ntA/v'),  # rankentaa
           (r"t[aä]$", r"", 'rake-ntA/v')], # käätä, parata
    'V43':[(r"it[aä][aä]$", r"i", 'tai-tA/v')],  # taitaa, tietää
    'V44':[(r"([uy])(tua|tyä)$", r"\1", 'antau-tU/v')],  # antautua, repeytyä
    'V45':[(r"ta$", r"", 'kaa-ta/v')],  #  kaata, taita, tuta
    'XX': [(r"$", r"", ''), (r"$", r"", '')]
}
#   '': [(r"$", r"", ''), (r"$", r"", '')], #
#   '': [(r"$", r"", '')], #



def markGradation(BAS, INFL, GR):
    if INFL in dd:
        patternList = dd[INFL]      # list of patterns for this infl class
    else: return("***", "*")
    for (pattern,replacement,contClass) in patternList:
        (ss,replacementCount) = re.subn(pattern, replacement, BAS)
        if (replacementCount > 0): # substitution succeeded
            if GR == 0:          # undo the marking, no gradation
                ss = re.sub(r"[<>]", "", ss)
            return(ss, contClass)
    return("***", "**")

rdr = csv.reader(sys.stdin, delimiter=' ')
wtr = csv.writer(sys.stdout, delimiter=',')

wtr.writerow(["HEADWORD", "WORD", "NEXT", "FEAT", "DERFROM", "GRAD"])

for entry in rdr:
    l = len(entry)
    if l < 2: continue   # it is a comment or something and is skipped
    base = re.sub(r"[1-9]", "", entry[0])
    infl = entry[1]
    astev = 1 if (l > 2 and entry[2]=='*') else 0
    #print("---", base, infl, astev)
    if not infl in dd: continue # it is a comment or something and is skipped
    (stem, cont) = markGradation(base, infl, astev)
    #if stem == "***":
    #    continue
    wtr.writerow([base, stem, cont, '', ''])

