import sys
print("LEXICON FirstPart")
for linenl in sys.stdin:
    line = linenl.strip()
    if line.endswith("nen"):
        line = line[0:-3] + "s"
    print(line, "SecondPart ;")
