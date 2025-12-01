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

for i in resultat:
    position_absolue = (position_absolue + i) % 100

    if position_absolue == 0:
        reponse += 1


print(reponse)
