# AOC - Day2 - Yanis Srairi

import sys

nom_fichier = sys.argv[1] if len(sys.argv) > 1 else "input.txt"

with open(nom_fichier) as f:
    data = f.read().strip()
    lignes = data.splitlines()

data = lignes[0].split(",")
print(data)

doublon = []

for donnee in data:
    range_data = donnee.split("-")
    for i in range(int(range_data[0]), int(range_data[1]) + 1):
        number_to_string = str(i)
        a, b = (
            number_to_string[: int(len((number_to_string)) / 2)],
            number_to_string[int(len((number_to_string)) / 2) :],
        )
        if a == b:
            doublon.append(int(i))

print(sum(doublon))
