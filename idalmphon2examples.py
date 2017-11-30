import re, csv

mp_name = {
    '{aaaaØ}':'{aØ}', # koir<a> koir<>ia
    '{aaaaaØ}':'{aØ}', # asem<a> asem<>ia
    '{aaaaaaØØ}':'{aØ}', # vapa<a> vapa<>ita
    '{}':'{}', # 
    '{}':'{}', #
    '{aaaao}':'{ao}', # kal<a> kal<o>ja
    '{aaaaao}':'{ao}', # kulkij<a> kulkij<o>ita
    '{aaaaaoo}':'{ao}', # mansikk<a> mansik<o>ita
    '{aaaaaØo}':'{aØo}', # matal<a> matal<>ia matal<o>ita
    '{aaaaaoØ}':'{aØo}', # herttu<a> herttu<o>ita herttu<>issa
    '{aaaaaoØo}':'{aØo}', # perun<a> perun<o>ita perun<>ia
    '{aaaaaooØ}':'{aØo}', # pasuun<a> pasuun<o>ita pasuun<>ia
    '{eeeeØ}':'{eØ}', # kame<e> kame<>ita
    '{eeeeeØ}':'{eØ}', # korke<e> korke<>ita
    '{eeØeØØØ}':'{ØeØeØ}', # hevon<e>n hevos<>ta hevos<e>na hevos<>na hevos<>ia
    '{ØeØeØØ}':'{ØeØeØ}', # ahven<> ahven<e>n ahven<>ta ahven<e>na ahven<>na
    '{ØeØeØØØ}':'{ØeØeØ}', # koiras<> koiraks<e>n koiras<>ta koiraks<e>na koiras<>na
    '{ØeeØeØeØØ}':'{ØeØeØ}', # terve<> terve<e>n tervet<>tä terveh<e>nä terveh<>nä
    '{ØeeØeeØØØ}':'{ØeØeØ}', # kuollut<> kuollut<>ta kuolleh<e>na kuollun<>na
    '{}':'{}', # 
    '{ØhØØØØ}':'{ØhØ}', # korke<>e korke<h>ien korke<>isiin
    '{ØØhØØhØh}':'{ØhØ}', # vapa<>a (vapa<h>an) (vapa<h>asen) vapa<>issa
    
    '{ieeeØ}':'{ieee}', # tupp<i> tup<e>n tupp<e>a tupp<e>na tupp<>ia
    '{ieØeØ}':'{ieØe}',
    #        tuoh<i> tuoh<e>n tuoh<>ta tuoh<>ia
    #        käs<i> käd<e>n kät<>ä kät<e>nä käs<>iä
    #        tos<i> tod<e>n tot<>ta tot<e>na tos<>ia
    #        hirs<i> hirr<e>n hirt<>tä hirt<e>nä hirs<>iä
    #        jäls<i> jäll<e>n jält<>tä jält<e>nä
    #        kans<i> kann<e>n kant<>ta kant<e>na kans<>ia
    #        kaks<i> kahd<e>n kah<>ta kaht<e>n kaks<>ia
    #        veits<i> veits<e>n veis<>tä veits<e>nä veits<>iä
    '{ieØeeØ}':'{ieØe}',
    #        lum<i> lum<e>n lun<>ta [lum<e>a] lum<e>na lum<>ia
    '{ieeØeØ}':'{ieØe}',
    #        tuom<i> tuom<e>n tuom<e>a (tuon<>ta) tuom<e>na tuom<>ia
    #        niem<i> niem<e>ä nien<>tä niem<e>nä niem<>iä
    #        suks<i> suks<e>n suks<e>a (sus<>ta) suks<e>n
    #        uks<i> uks<e>n us<>ta (uks<e>a) uks<e>na
    '{ieØeeØ}':'{ieØe}',
    #        peits<i> peits<e>n (peits<e>ä) peis<>tä peits<e>nä
    '{ieØeØØ}':'{ieØØ}',
    #        pien<i> pien<e>n pien<>tä pien<e>nä (pien<>nä) pien<>iä
    #        nuor<i> nuor<e>n nuor<>ta nuor<e>na (nuor<>na) (nuor<>ra) nuor<>ia
    '{ieØeØØØ}':'{ieØØ}',
    #        laps<i> laps<e>n las<>ta laps<e>na (las<>na) (las<>sa)
    '{ieeØeØØØ}':'{ieØØ}', # ?? exists no more
    #        haps<i> haps<e>n haps<e>a has<>ta haps<e>na (has<>na) (has<>sa)
    
    '{iiiiiiiiieie}':'{iiiiiiiiieie}', # kaun<i>s kaunae>hissa kaun<e>isiin 
    
    '{iiiiØ}':'{iØ}', # pi<i> pi<>iden
    '{iiiie}':'{iie}', # vat<i> vad<i>n vat<e>ja
    '{iiiiee}':'{iie}', # rist<i> rist<i>n rist<e>issä
    '{Øiiie}':'{Øiie}', # kalsium<> kalsium<i>n kalsium<e>ja
    '{kØkkk}':'{kØ}', # ark<k>u ark<>un
    '{kØkkkØ}':'{kØØ}', # sisäk<k>ö sisäk<k>öihin sisäk<>öihin
    '{kØkkkØk}':'{kØØ}', # mansik<k>oihin mansik<>oihin mansik<>oina
    '{}':'{}', # 
    '{}':'{}', #
    '{}':'{}', # 
    '{}':'{}', #
    '{}':'{}', # 
    '{}':'{}', #
    '{kkkØkk}':'{kkØ}', # su<k>si su<>sta
    '{kkØkkk}':'{kkØ}', # u<k>si u<>sta
    '{mmnmmm}':'{mn}', # lu<m>i lu<n>ta
    '{mmmnmm}':'{mn}', # tuo<m>i tuo<n>ten nie<m>i nie<n>tä
    '{nmnmmmnm}':'{mn}', # lämmi<n> lämpi<m>än lämmi<n>tä lämpi<m>ää
    '{nmnmm}':'{mn}', # uisti<n> uisti<m>en uisti<n>ta uisti<m>ia
    '{nØØØØØØ}':'{nØØ}', # hevone<n> hevose<>ssa
    '{nØØØØØØØ}':'{nØØ}', # seitsemä<n> seitsemä<>ä seitsen<>ten
    '{ooooØ}':'{oØ}', # tenkkapo<o>
    '{ooooooØØ}':'{oØ}', # tieno<o> tieno<>ita
    '{}':'{}', #
    '{nssssss}':'{nss}', # hevo<n>en hevo<s>en hevo<s>ta hevo<s>ia
    '{}':'{}', #
    '{}':'{}', # 
    '{mmmnmmnm}':'{mn}', # seitse<m>än seitse<n>tä
    '{mpmpppmp}':'{pm}', # läm<m>in läm<p>imän
    '{nmnmmmnm}':'{mn}', # lämpi<m>än pahi<n> pahi<m>man pahi<m>paa 
    '{nmnmmmm}':'{mn}', # vase<n> vase<m>man vase<n>ta vase<m>pia
    '{nnmnnmnnm}':'{mn}', # onneto<n> onnetto<m>an onneto<n>ta
    '{nnmttmmmnnm}':'{nnmttmmmnnm}', # ?? muuan
    '{}':'{}', #
    '{ppØpØØp}':'{ppØ}', # la<p>si la<>sta
    '{pppØpØØp}':'{ppØ}', # ha<p>si ha<>sta
    '{pØppp}':'{pØ}', # tup<p>i tup<>en
    '{tØttt}':'{tØ}', # pat<t>i pat<>in
    '{tØtttØ}':'{tØ}', # ilmet<t>y ilmet<>yissä ilmet<t>yjä ilmet<>yitä
    '{ØØtØØtØØt}':'{tØ}', # onnet<>on onnet<>oin onnet<t>oman
    '{tdttt}':'{td}', # va<t>i va<d>in
    '{dtdttt}':'{td}', # äi<d>yt äi<t>yen
    '{sdtts}':'{tds}', # kä<s>i kä<d>en kä<t>tä kä<t>enä kä<s>iä
    #       kalleu<s> kalleu<d>en kalleu<t>ena kalleuk<s>ia
    '{}':'{}', #
    '{}':'{}', #
    '{}':'{}', #
    '{ttØtt}':'{ttØ}', # vei<t>si vei<>stä
    '{ttØttt}':'{ttØ}', # pei<t>si pei<>stä
    '{uuuuØ}':'{uØ}', # leikku<u> leikku<>ita
    '{äääääØö}':'{äØö}', # leve<ä> leve<>itä leve<ö>itä
    '{}':'{}', #
    }


csv_in = open("ksk-zerofilledparad.csv", 'r')
reader = csv.DictReader(csv_in, delimiter=';')

for row in reader:
    surf = list(row['ALIGNED'])
    mphons = row['MPHON'].strip().split()
    lst = []
    for s, m in zip(surf, mphons):
        m = mp_name.get(m, m)
        lst.append(s if s == m else m + ':' + s)
    print(' '.join(lst))
