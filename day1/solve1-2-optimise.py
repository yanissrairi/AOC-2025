# AOC - Day1 Part 2 - Optimise
import sys

nom_fichier = sys.argv[1] if len(sys.argv) > 1 else "data1.txt"

with open(nom_fichier) as f:
    lignes = f.read().strip().splitlines()

pos = 50
reponse = 0

for ligne in lignes:
    mouvement = int(ligne[1:]) if ligne[0] == 'R' else -int(ligne[1:])
    nouvelle_pos = pos + mouvement

    if mouvement > 0:
        reponse += (nouvelle_pos // 100) - (pos // 100)
    elif mouvement < 0:
        reponse += ((pos - 1) // 100) - ((nouvelle_pos - 1) // 100)

    pos = nouvelle_pos

print(reponse)
