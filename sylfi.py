import re, sys
V = "[aeiouyäö]"
C = "[bcdfghjklmnpqrsštvxzž]"
VV = "(aa|ee|ii|oo|uu|yy|ää|öö)"
Vi = "(ai|ei|oi|ui|yi|äi|öi)"
V12 = "(ie|uo|yö)"
V21 = "(au|äy|ou|öy|eu|ey|iy)"

Syl1 = "(" + C + "*(" + V + "|" + VV + "|" +  Vi + "|" + V12 + "|" + V21 + ")" + C + "*)"
S1 = re.compile(Syl1)

Nuk =  "((" + V + "|" + VV + "|" + Vi + ")" + C + "*" + ")"
Syl2 = "(" + Syl1 + "(" + Nuk + "|" + V21 + "))"
S2 = re.compile(Syl2)

Syl3 = "(" + Syl2 + C + "?(" + Nuk + "|" + V21 + "))"
S3 = re.compile(Syl3)

print(Syl1)
print(Syl2)
print(Syl3)

def syllables(w):
    if S1.fullmatch(w):
        return("monosyllabic")
    elif S2.fullmatch(w):
        return("bisyllabic")
    elif S3.fullmatch(w):
        return("trisyllabic")
    else: return("other")

for l in sys.stdin:
    print(syllables(l.strip()))
