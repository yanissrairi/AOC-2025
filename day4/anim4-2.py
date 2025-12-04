"""
Manim visualization of the paper removal algorithm (solve4-2-gemini-optimise-v2.py)
Run with: manim -pql visualize_algorithm.py PaperRemovalAnimation

Change DATA_FILE below to use a different input file.
"""
from manim import *
import os

# ============== CONFIGURATION ==============
DATA_FILE = os.environ.get("DATA_FILE", "data4-test.txt")
# ===========================================


class PaperRemovalAnimation(Scene):
    def construct(self):
        # Load data first to calculate cell size
        with open(DATA_FILE) as f:
            lines = f.read().strip().splitlines()

        rows = len(lines)
        cols = len(lines[0])

        # Configuration - auto-scale cell size to fit screen
        # Manim default frame: ~14 units wide, ~8 units tall (with margins)
        MAX_WIDTH = 12.5
        MAX_HEIGHT = 5.5  # Leave more room for title and step text
        CELL_SIZE = min(MAX_WIDTH / cols, MAX_HEIGHT / rows)

        # For very large grids, skip count labels (too small to read)
        SHOW_COUNTS = cols <= 30 and rows <= 30

        PAPER_COLOR = BLUE
        EMPTY_COLOR = GRAY
        REMOVING_COLOR = RED
        LOW_NEIGHBOR_COLOR = YELLOW

        # Title with grid size info
        title = Text(f"Algorithme de suppression - grille {rows}x{cols}", font_size=24)
        title.to_edge(UP, buff=0.2)
        self.play(Write(title))

        # Explanation text area
        explanation = Text("", font_size=20)
        explanation.to_edge(DOWN)

        # Create visual grid
        grid_group = VGroup()
        squares = [[None for _ in range(cols)] for _ in range(rows)]
        count_labels = [[None for _ in range(cols)] for _ in range(rows)]

        # Data structures (mirroring the algorithm)
        grid = [[0] * (cols + 2) for _ in range(rows + 2)]
        counts = [[0] * (cols + 2) for _ in range(rows + 2)]
        deltas = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]

        # Build visual grid
        for r in range(rows):
            for c in range(cols):
                is_paper = lines[r][c] == "@"
                color = PAPER_COLOR if is_paper else EMPTY_COLOR
                opacity = 1.0 if is_paper else 0.2

                square = Square(
                    side_length=CELL_SIZE,
                    fill_color=color,
                    fill_opacity=opacity,
                    stroke_width=1
                )
                square.move_to(
                    RIGHT * (c - cols/2 + 0.5) * CELL_SIZE +
                    DOWN * (r - rows/2 + 0.5) * CELL_SIZE
                )
                squares[r][c] = square
                grid_group.add(square)

                # Initialize algorithm data
                if is_paper:
                    grid[r+1][c+1] = 1

        # Show initial grid (faster for large grids)
        grid_anim_time = 1.0 if rows > 50 else 2.0
        self.play(
            FadeIn(grid_group, lag_ratio=0.005 if rows > 50 else 0.02),
            run_time=grid_anim_time
        )

        # Step 1: Explain the problem
        step1 = Text("Etape 1: Grille initiale - @ = papier", font_size=20, color=YELLOW)
        step1.to_edge(DOWN, buff=0.2)
        self.play(Write(step1))
        self.wait(1)

        # Step 2: Calculate neighbor counts
        step2 = Text("Etape 2: Calculer le nombre de voisins pour chaque papier", font_size=20, color=YELLOW)
        step2.to_edge(DOWN, buff=0.2)
        self.play(Transform(step1, step2))

        # Calculate and display neighbor counts
        count_group = VGroup()
        for r in range(1, rows + 1):
            for c in range(1, cols + 1):
                if grid[r][c] == 1:
                    n_count = sum(grid[r + dr][c + dc] for dr, dc in deltas)
                    counts[r][c] = n_count

                    # Visual: show count on each paper (only for small grids)
                    if SHOW_COUNTS:
                        label = Text(str(n_count), font_size=14, color=WHITE)
                        label.move_to(squares[r-1][c-1].get_center())
                        count_labels[r-1][c-1] = label
                        count_group.add(label)

        if SHOW_COUNTS:
            self.play(FadeIn(count_group, lag_ratio=0.02), run_time=1.5)
            self.wait(1)
        else:
            self.wait(0.5)

        # Step 3: Mark papers with < 4 neighbors
        step3 = Text("Etape 3: Papiers avec < 4 voisins (jaune) seront supprimes", font_size=20, color=YELLOW)
        step3.to_edge(DOWN, buff=0.2)
        self.play(Transform(step1, step3))

        stack = []
        highlight_anims = []

        for r in range(1, rows + 1):
            for c in range(1, cols + 1):
                if grid[r][c] == 1 and counts[r][c] < 4:
                    stack.append((r, c))
                    grid[r][c] = 0  # Mark as queued
                    highlight_anims.append(
                        squares[r-1][c-1].animate.set_fill(LOW_NEIGHBOR_COLOR, opacity=1)
                    )

        if highlight_anims:
            self.play(*highlight_anims, run_time=1)
        self.wait(1)

        # Step 4: Propagation loop
        step4 = Text("Etape 4: Propagation - supprimer et mettre a jour", font_size=20, color=YELLOW)
        step4.to_edge(DOWN, buff=0.2)
        self.play(Transform(step1, step4))

        # Counter display
        counter_text = Text("Papiers supprimes: 0", font_size=24, color=GREEN)
        counter_text.to_corner(UR)
        self.play(FadeIn(counter_text))

        total_removed = 0
        step_count = 0

        # Timing config based on grid size
        LARGE_GRID = rows > 50 or cols > 50
        ANIM_SPEED = 0.15 if LARGE_GRID else 0.5
        WAVE_BATCH = 5 if LARGE_GRID else 1  # Group multiple waves for large grids

        # Process in batches for visual clarity
        wave_count = 0
        while stack:
            step_count += 1
            wave_count += 1

            # Take current batch
            current_batch = stack.copy()
            stack.clear()

            # For large grids, combine highlight + remove in one step
            if LARGE_GRID:
                # Direct to red (removing)
                remove_anims = [
                    squares[r-1][c-1].animate.set_fill(REMOVING_COLOR, opacity=0.8)
                    for r, c in current_batch
                ]
                if remove_anims:
                    self.play(*remove_anims, run_time=ANIM_SPEED)
            else:
                # Animate removal of current batch
                remove_anims = []
                for r, c in current_batch:
                    remove_anims.append(
                        squares[r-1][c-1].animate.set_fill(REMOVING_COLOR, opacity=0.8)
                    )
                    if count_labels[r-1][c-1]:
                        remove_anims.append(FadeOut(count_labels[r-1][c-1]))

                if remove_anims:
                    self.play(*remove_anims, run_time=ANIM_SPEED)

            # Fade out removed papers
            fadeout_anims = [
                squares[r-1][c-1].animate.set_fill(GRAY, opacity=0.1)
                for r, c in current_batch
            ]

            if fadeout_anims:
                self.play(*fadeout_anims, run_time=ANIM_SPEED * 0.6)

            total_removed += len(current_batch)

            # Update counter (less frequently for large grids)
            if not LARGE_GRID or wave_count % WAVE_BATCH == 0 or not stack:
                new_counter = Text(f"Papiers supprimes: {total_removed}", font_size=24, color=GREEN)
                new_counter.to_corner(UR)
                self.play(Transform(counter_text, new_counter), run_time=ANIM_SPEED * 0.6)

            # Update neighbors and find new papers to remove
            new_low_neighbors = []
            update_anims = []

            for r, c in current_batch:
                for dr, dc in deltas:
                    nr, nc = r + dr, c + dc

                    if 1 <= nr <= rows and 1 <= nc <= cols:
                        if grid[nr][nc] == 1:
                            counts[nr][nc] -= 1

                            # Update visual count (only for small grids)
                            if SHOW_COUNTS and count_labels[nr-1][nc-1]:
                                old_label = count_labels[nr-1][nc-1]
                                new_label = Text(
                                    str(counts[nr][nc]),
                                    font_size=14,
                                    color=RED if counts[nr][nc] < 4 else WHITE
                                )
                                new_label.move_to(old_label.get_center())
                                update_anims.append(Transform(old_label, new_label))

                            # Check if now below threshold
                            if counts[nr][nc] == 3:
                                stack.append((nr, nc))
                                grid[nr][nc] = 0
                                new_low_neighbors.append((nr, nc))

            if update_anims:
                self.play(*update_anims, run_time=ANIM_SPEED * 0.8)

            # Highlight new papers that will be removed
            if new_low_neighbors and not LARGE_GRID:
                highlight_new = [
                    squares[r-1][c-1].animate.set_fill(LOW_NEIGHBOR_COLOR, opacity=1)
                    for r, c in new_low_neighbors
                ]
                self.play(*highlight_new, run_time=ANIM_SPEED * 0.6)

        # Final result
        final_text = Text(
            f"Resultat final: {total_removed} papiers supprimes",
            font_size=24,
            color=GREEN
        )
        final_text.to_edge(DOWN, buff=0.2)
        self.play(Transform(step1, final_text))

        # Highlight remaining papers
        remaining = []
        for r in range(rows):
            for c in range(cols):
                if squares[r][c].fill_opacity > 0.5:
                    remaining.append(squares[r][c])

        if remaining:
            self.play(*[
                sq.animate.set_fill(GREEN, opacity=1)
                for sq in remaining
            ], run_time=1)

        self.wait(2)


class AlgorithmExplanation(Scene):
    """Scene explaining the algorithm step by step"""

    def construct(self):
        # Title
        title = Text("Algorithme de suppression en cascade", font_size=36)
        title.to_edge(UP)
        self.play(Write(title))

        # Algorithm steps
        steps = VGroup(
            Text("1. Charger la grille de papiers (@)", font_size=24),
            Text("2. Compter les voisins de chaque papier (8 directions)", font_size=24),
            Text("3. Papiers avec < 4 voisins -> file de suppression", font_size=24),
            Text("4. Boucle de propagation:", font_size=24),
            Text("   - Retirer un papier de la file", font_size=22, color=GRAY),
            Text("   - Decrementer le compteur de ses voisins", font_size=22, color=GRAY),
            Text("   - Si voisin tombe a 3 -> ajouter a la file", font_size=22, color=GRAY),
            Text("5. Compter le total supprime", font_size=24),
        )
        steps.arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        steps.next_to(title, DOWN, buff=0.5)

        for step in steps:
            self.play(Write(step), run_time=0.8)
            self.wait(0.3)

        self.wait(2)

        # Key insight
        insight = Text(
            "Complexite: O(n) grace a la propagation locale",
            font_size=28,
            color=YELLOW
        )
        insight.to_edge(DOWN)
        self.play(Write(insight))
        self.wait(2)


class NeighborDemo(Scene):
    """Demo showing how neighbors are counted"""

    def construct(self):
        CELL_SIZE = 0.8

        title = Text("Comptage des 8 voisins", font_size=32)
        title.to_edge(UP)
        self.play(Write(title))

        # Create 3x3 grid
        grid = VGroup()
        squares = []

        for r in range(3):
            row = []
            for c in range(3):
                sq = Square(
                    side_length=CELL_SIZE,
                    fill_color=BLUE if (r, c) != (1, 1) else GREEN,
                    fill_opacity=0.8,
                    stroke_width=2
                )
                sq.move_to(RIGHT * (c - 1) * CELL_SIZE + DOWN * (r - 1) * CELL_SIZE)
                grid.add(sq)
                row.append(sq)
            squares.append(row)

        self.play(FadeIn(grid))

        # Center label
        center_label = Text("?", font_size=24)
        center_label.move_to(squares[1][1].get_center())
        self.play(Write(center_label))

        # Highlight neighbors one by one
        deltas = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
        count = 0

        for i, (dr, dc) in enumerate(deltas):
            nr, nc = 1 + dr, 1 + dc
            count += 1

            self.play(
                squares[nr][nc].animate.set_stroke(YELLOW, width=4),
                run_time=0.3
            )

            new_label = Text(str(count), font_size=24)
            new_label.move_to(squares[1][1].get_center())
            self.play(Transform(center_label, new_label), run_time=0.2)

        # Final explanation
        result = Text("8 voisins -> ce papier reste (>= 4)", font_size=24, color=GREEN)
        result.to_edge(DOWN)
        self.play(Write(result))

        self.wait(2)


if __name__ == "__main__":
    # For testing: python visualize_algorithm.py
    print("Run with: manim -pql visualize_algorithm.py PaperRemovalAnimation")
    print("Or for high quality: manim -pqh visualize_algorithm.py PaperRemovalAnimation")
