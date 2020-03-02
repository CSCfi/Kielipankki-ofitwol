import csv, re
fil = open("ofi-n-guesses.csv", "r")
rdr = csv.reader(fil)
d = {}
for entry, guesses, forms in rdr:
    #print(entry, guesses, forms) ###
    lst = entry.split("{", maxsplit=1)
    #print("lst =", lst) ###
    entry_a = lst[0]
    entry_z = "{" + lst[1] if len(lst) == 2 else ""
    #print("entry =", entry_a, entry_z) ###
    guess_lst = guesses.split(" | ")
    #print("guess_lst =", guess_lst) ###
    form_count = len(forms.split(" "))
    found_one = False
    for guess_entry in guess_lst:
        guess = guess_entry.split(" ")[0]
        if guess == entry:
            found_one = True
            continue
        lst = guess.split("{", maxsplit=1)
        guess_a = lst[0]
        guess_z = "{" + lst[1] if len(lst) == 2 else ""
        #print("guess =", guess) ###
        if (entry_z, guess_z) in d:
            d[(entry_z, guess_z)].add(entry_a + "_" + str(form_count))
        else:
            d[(entry_z, guess_z)] = {entry_a + "_" + str(form_count)}
    if not found_one:
        print("***{}, {}, {}***".format(entry, guesses, forms))

empty = set()
for pair, set in sorted(d.items()):
    correct, wrong = pair
    print("»{}« »{}«".format(correct, wrong))
    print(" ".join(sorted(list(set))))
    print()
    print("»{}« »{}«".format(wrong, correct))
    print(" ".join(sorted(list(d.get((wrong, correct), empty)))))
    print("\n--------\n")
