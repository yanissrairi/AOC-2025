# AOC - Day4 - Yanis Srairi

import sys

nom_fichier = sys.argv[1] if len(sys.argv) > 1 else "input.txt"

with open(nom_fichier) as f:
    data = f.read().strip()
    lignes = data.splitlines()

matrice = []

# Transformation en matrice 0 1
for ligne in lignes:
    nouvelle_ligne = []
    for emplacement in ligne:
        if emplacement == ".":
            nouvelle_ligne.append(0)
        else:
            nouvelle_ligne.append(1)
    matrice.append(nouvelle_ligne)

nombre_ligne = len(matrice)
nombre_colonne = len(matrice[0])
answer = 0

for i in range(nombre_ligne):
    for j in range(nombre_colonne):
        count = 0
        if matrice[i][j] == 1:
            if i == 0 and j == 0:
                count = sum(
                    [matrice[i + 1][j], matrice[i][j + 1], matrice[i + 1][j + 1]]
                )
            elif i == nombre_ligne - 1 and j == 0:
                count = sum(
                    [
                        matrice[i - 1][j],
                        matrice[i - 1][j + 1],
                        matrice[i][j + 1],
                    ]
                )
            elif i == 0 and j == nombre_ligne - 1:
                count = sum(
                    [
                        matrice[i][j - 1],
                        matrice[i + 1][j - 1],
                        matrice[i + 1][j],
                    ]
                )
            elif i == nombre_ligne - 1 and j == nombre_colonne - 1:
                count = sum(
                    [
                        matrice[i][j - 1],
                        matrice[i - 1][j - 1],
                        matrice[i - 1][j],
                    ]
                )
            elif i == 0:
                count = sum(
                    [
                        matrice[i][j - 1],
                        matrice[i + 1][j - 1],
                        matrice[i + 1][j],
                        matrice[i][j + 1],
                        matrice[i + 1][j + 1],
                    ]
                )
            elif j == 0:
                count = sum(
                    [
                        matrice[i - 1][j],
                        matrice[i - 1][j + 1],
                        matrice[i][j + 1],
                        matrice[i + 1][j],
                        matrice[i + 1][j + 1],
                    ]
                )
            elif i == nombre_ligne - 1:
                count = sum(
                    [
                        matrice[i][j - 1],
                        matrice[i - 1][j - 1],
                        matrice[i - 1][j],
                        matrice[i - 1][j + 1],
                        matrice[i][j + 1],
                    ]
                )
            elif j == nombre_colonne - 1:
                count = sum(
                    [
                        matrice[i - 1][j],
                        matrice[i - 1][j - 1],
                        matrice[i][j - 1],
                        matrice[i + 1][j - 1],
                        matrice[i + 1][j],
                    ]
                )
            else:
                count = sum(
                    [
                        matrice[i - 1][j - 1],
                        matrice[i - 1][j],
                        matrice[i - 1][j + 1],
                        matrice[i][j - 1],
                        matrice[i][j + 1],
                        matrice[i + 1][j - 1],
                        matrice[i + 1][j],
                        matrice[i + 1][j + 1],
                    ]
                )
            if count < 4:
                answer += 1
                print(f"{i},{j} = {count} | {answer}")
print(answer)
