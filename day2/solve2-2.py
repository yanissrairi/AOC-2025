# AOC - Day2 - Yanis Srairi

import sys

nom_fichier = sys.argv[1] if len(sys.argv) > 1 else "input.txt"

with open(nom_fichier) as f:
    data = f.read().strip()
    lignes = data.splitlines()

data = lignes[0].split(",")

doublon = []
for donnee in data:
    range_data = donnee.split("-")
    start = int(range_data[0])
    end = int(range_data[1])

    for i in range(start, end + 1):
        number_to_string = str(i)
        longueur_totale = len(number_to_string)

        # On cherche un motif de taille 1 jusqu'à la moitié de la chaîne
        # Example: pour "123123", len=6, on teste motifs de taille 1, 2, 3.
        est_valide = False

        for taille_motif in range(1, (longueur_totale // 2) + 1):
            # 1. Optimisation : Si la longueur totale n'est pas un multiple
            # de la taille du motif, impossible que ce soit une répétition parfaite.
            if longueur_totale % taille_motif != 0:
                continue

            # 2. On isole le motif candidate (le début de la chaîne)
            motif = number_to_string[:taille_motif]

            # 3. On calcule combien de fois il devrait apparaitre
            nb_repetitions = longueur_totale // taille_motif

            # 4. LE TEST : Est-ce que motif * répétitions redonne la chaîne originale ?
            if motif * nb_repetitions == number_to_string:
                est_valide = True
                break  # On a trouvé une répétition, pas besoin de tester d'autres tailles pour ce nombre

        if est_valide:
            doublon.append(i)

# Utilisation de set() pour être sûr de ne pas compter deux fois le même nombre
# (même si le break ci-dessus l'empêche déjà, c'est une sécurité).
print(f"Some des IDs invalides : {sum(set(doublon))}")
"""for donnee in data:
    range_data = donnee.split("-")
    for i in range(int(range_data[0]), int(range_data[1]) + 1):
        number_to_string = str(i)
        longueur_string = len(number_to_string)
        nombre_de_paire_possible = longueur_string // 2

        sequence = []
        for j in range(1, nombre_de_paire_possible + 1):
            var = []
            for k in range(0, len(number_to_string) + 1, j):
                var.append(k)
            sequence.append(var)

        response = []
        longueur_sequence = 0
        for j in sequence:
            response = []
            longueur_sequence = len(j)
            for k in range(0, longueur_sequence - 1):
                response.append(number_to_string[j[k] : j[k + 1]])
            longueur_liste = len(response)
            if response.count(response[0]) == longueur_liste:
                doublon.append(i)"""
