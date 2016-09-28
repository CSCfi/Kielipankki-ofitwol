import re, sys
V = "(a|e|i|o|u|y|ä|ö)"
C = "(b|c|d|f|g|h|j|k|l|m|n|p|q|r|s|š|t|v|x|z|ž)"
VV = "(aa|ee|ii|oo|uu|yy|ää|öö)"
Vi = "(ai|ei|oi|ui|yi|äi|öi)"
V12 = "(ie|uo|yö)"
V21 = "(au|äy|ou|öy|eu|ey|iy)"

Syl1 = "(" + C + "*(" + V + "|" + VV + "|" +  Vi + "|" + V12 + "|" + V21 + ")" + C + "*)"
S1 = re.compile(Syl1)

Nuk =  "(" + V + "|" + VV + "|" + Vi + "|" + V21 + ")"
Syl2 = "(" + Syl1 + "(" + Nuk + C + "*" + "|" + V21 + "))"
S2 = re.compile(Syl2)

# print(Syl1)

def syllables(w):
    if S1.fullmatch(w):
        return("monosyllabic")
    elif S2.fullmatch(w):
        return("bisyllabic")
    else: return("other")

for l in sys.stdin:
    print(syllables(l.strip()))
