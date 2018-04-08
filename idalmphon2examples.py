import re, csv

mp_name = {
    '{aaaaØ}':'{aØ}', # koir<a> koir<>ia
    '{aaaaaØ}':'{aØ}', # asem<a> asem<>ia
    '{aaaaaaØØ}':'{aØ}', # vapa<a> vapa<>ita
    '{aaaao}':'{ao}', # kal<a> kal<o>ja
    '{aaaaao}':'{ao}', # kulkij<a> kulkij<o>ita
    '{aaaaaoo}':'{ao}', # mansikk<a> mansik<o>ita
    '{aaaaaØo}':'{aØo}', # matal<a> matal<>ia matal<o>ita
    '{aaaaaoØ}':'{aØo}', # herttu<a> herttu<o>ita herttu<>issa
    '{aaaaaoØo}':'{aØo}', # perun<a> perun<o>ita perun<>ia
    '{aaaaaooØ}':'{aØo}', # pasuun<a> pasuun<o>ita pasuun<>ia
    '{ØaaØaaØØ}':'{ØaØa}', # koiras<> koira<a>n koiras<>ta koira<a>na
    '{ØaaØaØØaØ}':'{ØaØØ}', # vieras<> viera<a>n vieras<>ta (vieras<>na)
    '{ØaaØaØØaØØ}':'{ØaØØ}', # saapas<> saappa<a>n saapas<>ta (saapas<>na)
    '{ØaØaaaØ}':'{ØaØa}', # vasen<> vasemm<a>n vasen<>ta vasemp<a>na
    '{ØaØaaaØØ}':'{ØaØØ}', # pahin<> pahimm<a>n pahin<>ta (pahin<>na)
    '{ØäØäääØØ}':'{ØäØØ}', # lämmin<> lämpim<ä>n lämmin<>tä (lämmmin<>nä) lämpim<>iä
    '{ØääØäØäØØ}':'{ØäØØ}', # kevät<> kävä<ä>n kevät<>tä (kevän<>nä)
    '{äääØääØØ}':'{ØäØØ}', # seitsem<ä>n seitsem<ä>ä seitsen<>tä (seitsen<>nä) seitsem<ä>nä
    '{ØØaØØaaaØØØ}':'{ØaØØ}',
    #        muuan<> muutam<a>n muuat<>ta (muuan<>na) muutam<a>na
    '{ØØaØØaØØØ}':'{ØaØØ}', # onneton<> onnettom<a>n onneton<>ta (onneton<>na)
    '{eeeeØ}':'{eØ}', # kame<e> kame<>ita
    '{eeeeeØ}':'{eØ}', # korke<e> korke<>ita
    '{eeØeØØØ}':'{ØeØeØ}',
    #        hevon<e>n hevos<>ta hevos<e>na (hevos<>na) hevos<>ia
    '{ØeØeØØ}':'{ØeØeØ}',
    #        ahven<> ahven<e>n ahven<>ta ahven<e>na (ahven<>na)
    #        sisar<> sisar<e>n sisar<>ta  uistin<> uistim<e>n uistin<>ta
    '{ØeØeØØØ}':'{ØeØeØ}',
    #        koiras<> koiraks<e>n koiras<>ta koiraks<e>na (koiras<>na)
    '{ØeeØeØeØØ}':'{ØeØeØ}',
    #        terve<> terve<e>n tervet<>tä (terveh<e>nä) (terven<>nä)
    '{ØeeØeeØØØ}':'{ØeØeØ}',
    #        kuollut<> kuolle<e>n kuollut<>ta (kuollun<>na) (kuolleh<>ia)
    '{ØeeØeØ}':'{ØeØe}', # askel<> askel<e>n askel<>ta askel<e>na
    '{ØeeØeeØØ}':'{ØeØe}', # vaate<> vaatte<e>n vaatet<>ta vaatteh<e>n vaatte<>ita
    '{ØhØØØØ}':'{ØhØ}', # korke<>e korke<h>ien korke<>isiin
    '{ØØhØØhØh}':'{ØhØ}', # vapa<>a (vapa<h>an) (vapa<h>asen) vapa<>issa
    '{ØØhØØØ}':'{ØhØ}', # leve<>e leve<h>enä leve<>itä leve<h>iä
    '{ØØhtØhØh}':'{Øht}', # vaate<> vaatte<h>en vaate<t>a
    '{ØhØtØØ}':'{Øht}', # askele<> askele<h>en askele<t>ta
    '{ØØhtØnhØh}':'{Øhtn}',
    #        terve<> (terve<h>en) terve<t>tä (terve<n>>ä) (terve<h>enä)
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
    '{}':'{}', #
    '{iiiiiiiiieie}':'{iiiiiiiiieie}', # kaun<i>s kaunae>hissa kaun<e>isiin 
    '{iiiiØ}':'{iØ}', # pi<i> pi<>iden
    '{iiiie}':'{iie}', # vat<i> vad<i>n vat<e>ja
    '{iiiiee}':'{iie}', # rist<i> rist<i>n rist<e>issä
    '{iiiØiee}':'{iiØie}', # sankar<i> sankar<i>n (sankar<>ten) sankar<i>na
    '{Øiiie}':'{Øiie}', # kalsium<> kalsium<i>n kalsium<e>ja
    '{iiiiiiiiieie}':'{iiee}', # kaun<i>s (kaun<i>hin) (kaun<e>hissa)
    '{ØiØØiØØiØ}':'{ØiØ}', # onneto<>n (onneto<i>n) onnetto<>mana onneto<i>nna
    '{ØiiØiØØiØØ}':'{ØiØØ}', # kauris <> kauri<i>n kauris<>ta (kauris<>na)
    '{ØiiØiØØiØØØØ}':'{ØiØØ}', # kaunis<> kauni<i>n kaunis<>ta (kaunis<>na)
    '{ØiiØiiØØ}':'{ØiØi}', # ori<Ø> ori<i>n orit<>ta orih<i>na 
    '{kØkkk}':'{kØ}', # ark<k>u ark<>un
    '{ØkØkk}':'{ØkØ}', # vastau<>s vastau<k>sen vastau<>sta
    '{ØØØØk}':'{ØØk}', # kalleu<>s kalleu<>den kalleu<>tta kalleu<k>sia
    '{kØkkkØ}':'{kØØ}', # sisäk<k>ö sisäk<k>öihin sisäk<>öihin
    '{kØkkkØk}':'{kØØ}', # mansik<k>oihin mansik<>oihin mansik<>oina
    '{kkkØkk}':'{kkØ}', # su<k>si su<>sta
    '{kkØkkk}':'{kkØ}', # u<k>si u<>sta
    '{khhhk}':'{khk}', # ka<k>si ka<h>den ka<h>ta ka<k>sia
    '{ØkØkØØk}':'{ØkØØ}', # koira<>s koira<k>sen (koira<>sna) koira<k>sia
    '{}':'{}', #
    '{mmnmmm}':'{mn}', # lu<m>i lu<n>ta
    '{mmmnmm}':'{mn}', # tuo<m>i tuo<n>ten nie<m>i nie<n>tä
    '{nmnmmmnm}':'{mn}', # lämmi<n> lämpi<m>än lämmi<n>tä lämpi<m>ää
    '{mmmnmmnm}':'{mn}', # seitse<m>än seitse<n>tä
    '{nmnmm}':'{mn}', # uisti<n> uisti<m>en uisti<n>ta uisti<m>ia
    '{nØØØØØØ}':'{nØØ}', # hevone<n> hevose<>ssa
    '{nØØØØØØØ}':'{nØØ}', # seitsemä<n> seitsemä<>ä seitsen<>ten
    '{}':'{}', #
    '{nssssss}':'{nss}', # hevo<n>en hevo<s>en hevo<s>ta hevo<s>ia
    '{ØnØnn}':'{ØnØ}', # tuha<>t tuha<n>nen tuha<>tta tuha<n>tena tuha<n>sia
    '{ØnØnØn}':'{ØnØ}', # kahdeksa<>s kahdeksa<n>nen kahdeksa<>tta (kahdeksa<>nna)
    '{}':'{}', #
    '{}':'{}', #
    '{mpmpppmp}':'{pm}', # läm<m>in läm<p>imän
    '{nmnmmmnm}':'{mn}', # lämpi<m>än pahi<n> pahi<m>man pahi<m>paa 
    '{nmnmmmm}':'{mn}', # vase<n> vase<m>man vase<n>ta vase<m>pia
    '{nnmnnmnnm}':'{mn}', # onneto<n> onnetto<m>an onneto<n>ta
    '{nnmttmmmnnm}':'{mnt}', # muua<n> muuta<m>an muua<t>ta
    '{}':'{}', #
    '{}':'{}', #
    '{ooooØ}':'{oØ}', # tenkkapo<o>
    '{ooooooØØ}':'{oØ}', # tieno<o> tieno<>ita
    '{ØooØooØØ}':'{ØoØo}', # uro<>s uro<o>n uro<>sta uro<o>na (uroh<o>na)
    '{}':'{}', #
    '{}':'{}', #
    '{ppØpØØp}':'{ppØ}', # la<p>si la<>sta
    '{pppØpØØp}':'{ppØ}', # ha<p>si ha<>sta
    '{ØmØpppp}':'{Øpm}', # vasen<> vasem<m>an vasen<>ta vasem<p>ana
    '{ØmØpppØp}':'{ØpmØ}', # pahin<> pahim<m>an pahin<>ta (pahin<>na) pahim<p>ana
    '{pØppp}':'{pØ}', # tup<p>i tup<>en
    '{ØppØpØØppp}':'{pØ}', # saap<>as saap<p>aan
    '{}':'{}', #
    '{}':'{}', #
    '{sØØsØØØØ}':'{sØsØ}', # koira<s> koira<>an koira<s>ta koira<>ita
    #'{snttns}':'{tns}', # kahdeksa<s> kahdeksa<n>essa kahdeksa<t>ta kahdeksan<s>ia
    '{sØhsØhØh}':'{sØh}', # uro<s> uro<>on uro<h>on
    '{sØhsØsshØh}':'{sØh}', # saapa<s> saappa<>an saappa<h>asen
    '{sØhsØsshØ}':'{sØh}', # viera<s> viera<>an viera<h>an
    '{sØhsØsshØØhh}':'{sØh}', # kauni<s> kauni<>in kauni<s>ta kauni<h>ia
    '{shshssh}':'{hs}', # mie<s> mie<h>en mie<s>tä mie<h>iä
    '{}':'{}', #
    '{}':'{}', #
    '{ØdtØdtttØdt}':'{Ødt}', # muu<>an (muu<d>an) muu<t>aman<
    '{tØttt}':'{tØ}', # pat<t>i pat<>in
    '{tØtttØ}':'{tØØ}', # ilmet<t>y ilmet<>yissä ilmet<t>yjä ilmet<>yitä
    '{ttØtt}':'{ttØ}', # vei<t>si vei<>stä
    '{ttØttt}':'{ttØ}', # pei<t>si pei<>stä
    '{ØØtØØtØØt}':'{tØ}', # onnet<>on onnet<>oin onnet<t>oman
    '{ØttØtttt}':'{tØ}', # vaat<>t vaat<t>een
    '{tdttt}':'{td}', # va<t>i va<d>in
    '{}':'{}', #
    '{dtdttt}':'{td}', # äi<d>yt äi<t>yen
    '{sdtts}':'{tds}', # kä<s>i kä<d>en kä<t>tä kä<t>enä kä<s>iä
    #       kalleu<s> kalleu<d>en kalleu<t>ena kalleuk<s>ia
    '{sdØts}':'{tdØs}', # kak<s>i kah<d>en kah<>ta kah<t>ena kak<s>ia
    '{sltts}':'{tls}', # jäl<s>i jäl<l>en jäl<t>tä jäl<s>iä
    '{sntts}':'{tns}', # kan<s>i kan<n>en kan<t>ena
    #'{tntts}':'{tns}', # tuha<t> tuhan<n>en tuhan<s>ia
    '{srtts}':'{trs}', # hir<s>i hir<r>en hir<t>tä hir<s>iä
    '{}':'{}', #
    '{}':'{}', #
    '{tØhtØhnØh}':'{tØhn}', # kuollu<t> kuolle<>en kuollu<t>ta kuolle<h>ia
    '{tØhtØnhØh}':'{tØhn}', # kevä<t> kevä<>än kevä<t>tä kevä<n>nä
    '{tØtØØh}':'{tØh}', # airu<t> airu<>en airu<t>a airu<h>ien
    '{}':'{}', #
    '{}':'{}', #
    '{ueeueeuee}':'{ue}', # kuoll<u>t kuoll<e>en kuoll<u>tta kuoll<e>ita
    '{uuuuØ}':'{uØ}', # leikku<u> leikku<>ita
    '{ØuuØuuØØ}':'{ØuØu}', # kiiru<> kiiru<u>n kiiruh<u>n kiirut<>ta 
    '{}':'{}', #
    '{}':'{}', #
    '{}':'{}', #
    '{äääääØö}':'{äØö}', # leve<ä> leve<>itä leve<ö>itä
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
