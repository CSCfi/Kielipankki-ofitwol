import sys, re

particles = set()

for line_nl in sys.stdin:
    line = line_nl.strip()
    lst = line.split()
    if len(lst) < 2:
        continue
    word = re.sub(r"[0-9]+$", r"", lst[0])
    #if word.endswith("sti") and len(word) > 4:
    #    continue
    if "-" in word:
        continue
    (first, separ, second) = word.partition("//")
    if second:
        word = second
    word = word.replace("/", "").replace(",", "")

    if len(lst) >= 3:
        suff_code = lst[2]
        if "X" in suff_code:
            particles.add(word + " /ps ;")
        elif "+" in suff_code:
            particles.add(word + " /po ;")
    else:
        if len(word) > 3:
            particles.add(word + " /pc ;")
        else:
            particles.add(word + " /p ;")

print("LEXICON Particles")
for entry in sorted(list(particles)):
    print(entry)
