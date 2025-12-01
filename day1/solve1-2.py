# AOC - Day1 - Yanis Srairi

import sys

nom_fichier = sys.argv[1] if len(sys.argv) > 1 else "input.txt"

with open(nom_fichier) as f:
    data = f.read().strip()
    lignes = data.splitlines()

resultat = []

for ligne in lignes:
    if ligne[0] == "L":
        resultat.append(-int(ligne[1:]))
    else:
        resultat.append(int(ligne[1:]))

position_absolue = 50
reponse = 0

for mouvement in resultat:
    ancienne_position = position_absolue
    position_absolue += mouvement

    count = 0

    if mouvement > 0:
        count = (position_absolue // 100) - (ancienne_position // 100)

    elif mouvement < 0:
        count = ((ancienne_position - 1) // 100) - ((position_absolue - 1) // 100)

    reponse += count

print(reponse)
