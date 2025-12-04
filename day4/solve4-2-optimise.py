# AOC - Day4 Part 2 - Optimise (Fixed)
import sys

nom_fichier = sys.argv[1] if len(sys.argv) > 1 else "data4.txt"
with open(nom_fichier) as f:
    lines = f.read().strip().splitlines()

rows = len(lines)
cols = len(lines[0])

# Grid avec padding pour éviter les checks de bords
grid = [[0] * (cols + 2) for _ in range(rows + 2)]
counts = [[0] * (cols + 2) for _ in range(rows + 2)]

# Initialiser la grille
for r in range(rows):
    for c in range(cols):
        if lines[r][c] == "@":
            grid[r + 1][c + 1] = 1

# Calculer TOUS les counts d'abord (sans modifier grid)
for r in range(1, rows + 1):
    for c in range(1, cols + 1):
        if grid[r][c] == 1:
            counts[r][c] = (
                grid[r-1][c-1] + grid[r-1][c] + grid[r-1][c+1] +
                grid[r][c-1]                  + grid[r][c+1] +
                grid[r+1][c-1] + grid[r+1][c] + grid[r+1][c+1]
            )

# PUIS construire la stack initiale
stack = []
for r in range(1, rows + 1):
    for c in range(1, cols + 1):
        if grid[r][c] == 1 and counts[r][c] < 4:
            stack.append((r, c))
            grid[r][c] = 0  # Marquer comme supprimé

# Propagation
deltas = [(-1,-1), (-1,0), (-1,1), (0,-1), (0,1), (1,-1), (1,0), (1,1)]
total = 0

while stack:
    r, c = stack.pop()
    total += 1

    for dr, dc in deltas:
        nr, nc = r + dr, c + dc
        if grid[nr][nc] == 1:
            counts[nr][nc] -= 1
            if counts[nr][nc] < 4:
                stack.append((nr, nc))
                grid[nr][nc] = 0

print(total)
