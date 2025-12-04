# AOC - Day2 Part 2 - Ultra Optimise (no string ops)
import sys

nom_fichier = sys.argv[1] if len(sys.argv) > 1 else "data2.txt"

with open(nom_fichier) as f:
    data = f.read().strip().splitlines()[0].split(",")

# Pré-calculer les multiplicateurs: motif * mult = pattern répété
# Ex: 12 * 10101 = 121212 (12 répété 3 fois)
def calc_multiplicateur(taille_motif, nb_rep):
    """Calcule le multiplicateur pour répéter un motif nb_rep fois"""
    base = 10 ** taille_motif
    mult = 0
    for _ in range(nb_rep):
        mult = mult * base + 1
    return mult

# Pré-calculer tous les multiplicateurs utiles
multiplicateurs = {}
for longueur in range(2, 14):
    for taille in range(1, longueur):
        if longueur % taille == 0:
            nb_rep = longueur // taille
            if nb_rep >= 2:
                multiplicateurs[(taille, nb_rep)] = calc_multiplicateur(taille, nb_rep)

def patterns_dans_range(start, end):
    """Génère les patterns répétitifs dans [start, end] - SANS string ops"""
    resultats = set()

    # Nombre de digits
    len_start = len(str(start))
    len_end = len(str(end))

    for longueur in range(len_start, len_end + 1):
        for taille_motif in range(1, longueur):
            if longueur % taille_motif != 0:
                continue

            nb_rep = longueur // taille_motif
            if nb_rep < 2:
                continue

            mult = multiplicateurs[(taille_motif, nb_rep)]

            # Bornes du motif
            motif_min = 10 ** (taille_motif - 1) if taille_motif > 1 else 1
            motif_max = 10 ** taille_motif

            # Optimisation: calculer les bornes exactes du motif pour ce range
            # motif * mult >= start => motif >= start / mult
            # motif * mult <= end => motif <= end / mult
            motif_low = max(motif_min, (start + mult - 1) // mult)  # ceil division
            motif_high = min(motif_max - 1, end // mult)

            for m in range(motif_low, motif_high + 1):
                resultats.add(m * mult)

    return resultats

tous_invalides = set()

for donnee in data:
    parts = donnee.split("-")
    start, end = int(parts[0]), int(parts[1])
    tous_invalides.update(patterns_dans_range(start, end))

print(f"Some des IDs invalides : {sum(tous_invalides)}")
