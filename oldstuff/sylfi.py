""" Count syllables in (native) Finnish words
"""
import re, sys

# vowels
V = "[aeiouyäö]"

# consonants
C = "[bcdfghjklmnpqrsštvxzž]"

# long vowels
VV = "(aa|ee|ii|oo|uu|yy|ää|öö)"

# diphthongs in all positions
Vi = "(ai|ei|oi|ui|yi|äi|öi)"

# diphthong only in the first syllable (except: ien, ies, aie)
V12 = "(ie|uo|yö)"

# diphthong always in the first syllable, but later on only before an open syllable
V21 = "(au|äy|ou|öy|eu|ey|iy)"

S0 = re.compile(V)

# words with one syllable
Syl1 = "(" + C + "*(" + V + "|" + VV + "|" +  Vi + "|" + V12 + "|" + V21 + ")" + C + "*)"
S1 = re.compile(Syl1)

Nuk =  "((" + V + "|" + VV + "|" + Vi + ")" + C + "*" + ")"
Syl2 = "(" + Syl1 + "(" + Nuk + "|" + V21 + "))"
S2 = re.compile(Syl2)

Syl3 = "(" + Syl2 + C + "?(" + Nuk + "|" + V21 + "))"
S3 = re.compile(Syl3)

#print(Syl1)
#print(Syl2)
#print(Syl3)

def syllables(w):
    if not S0.search(w):
        return(0)
    elif S1.fullmatch(w):
        return(1)
    elif S2.fullmatch(w):
        return(2)
    elif S3.fullmatch(w):
        return(3)
    else: return(4)

if __name__ == "__main__":
    for l in sys.stdin:
        print(syllables(l.strip()))
