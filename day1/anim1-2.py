"""
Manim visualization of AOC Day 1 - Safe Dial Problem
Run with: manim -pql visualize_dial.py DialAnimation
"""
from manim import *
import numpy as np
import os

DATA_FILE = os.environ.get("DATA_FILE", "data1-test.txt")


class DialAnimation(Scene):
    def construct(self):
        # Load data
        with open(DATA_FILE) as f:
            lignes = f.read().strip().splitlines()

        # Parse movements
        mouvements = []
        for ligne in lignes:
            if ligne[0] == 'R':
                mouvements.append((ligne, int(ligne[1:])))
            else:
                mouvements.append((ligne, -int(ligne[1:])))

        # Title
        title = Text("AOC Day 1 - Cadran du Coffre-fort", font_size=32)
        title.to_edge(UP, buff=0.3)
        self.play(Write(title))

        # Create dial
        DIAL_RADIUS = 2.5
        dial_circle = Circle(radius=DIAL_RADIUS, color=WHITE, stroke_width=3)
        dial_circle.shift(LEFT * 2)

        # Create number labels around dial (0-99)
        # Only show every 10th number to avoid clutter
        number_labels = VGroup()
        for i in range(0, 100, 10):
            angle = (90 - i * 3.6) * DEGREES  # 0 at top, going clockwise
            color = RED if i == 0 else WHITE
            label = Text(str(i), font_size=18, color=color)
            label.move_to(dial_circle.get_center() + (DIAL_RADIUS + 0.3) * np.array([
                np.cos(angle), np.sin(angle), 0
            ]))
            number_labels.add(label)

        # Mark for 0 (special dot - highlighted)
        zero_angle = 90 * DEGREES
        zero_mark = Dot(
            dial_circle.get_center() + DIAL_RADIUS * np.array([np.cos(zero_angle), np.sin(zero_angle), 0]),
            color=RED,
            radius=0.1
        )

        # Dynamic position label (shown only for non-multiples of 10)
        current_pos_label = None

        # Create pointer (arrow)
        def get_pointer_angle(position):
            """Convert dial position (0-99) to angle in radians"""
            return (90 - position * 3.6) * DEGREES

        pointer_length = DIAL_RADIUS - 0.3
        initial_pos = 50
        initial_angle = get_pointer_angle(initial_pos)

        pointer = Arrow(
            dial_circle.get_center(),
            dial_circle.get_center() + pointer_length * np.array([
                np.cos(initial_angle), np.sin(initial_angle), 0
            ]),
            color=YELLOW,
            buff=0,
            stroke_width=6,
            max_tip_length_to_length_ratio=0.2
        )

        # Position display
        pos_label = Text(f"Position: {initial_pos}", font_size=24, color=YELLOW)
        pos_label.to_edge(RIGHT).shift(UP * 2 + LEFT * 0.5)

        # Zero counter
        zero_counter = Text("Passages par 0: 0", font_size=24, color=RED)
        zero_counter.next_to(pos_label, DOWN, buff=0.5)

        # Current instruction display
        instr_label = Text("Instruction: -", font_size=24, color=BLUE)
        instr_label.next_to(zero_counter, DOWN, buff=0.5)

        # Helper to create position label on dial
        def create_dial_pos_label(position):
            display_pos = position % 100
            if display_pos < 0:
                display_pos += 100
            angle = get_pointer_angle(display_pos)
            label = Text(str(display_pos), font_size=16, color=YELLOW)
            label.move_to(dial_circle.get_center() + (DIAL_RADIUS + 0.35) * np.array([
                np.cos(angle), np.sin(angle), 0
            ]))
            return label, display_pos

        # Show dial
        self.play(
            Create(dial_circle),
            FadeIn(number_labels),
            FadeIn(zero_mark),
            Create(pointer),
            Write(pos_label),
            Write(zero_counter),
            Write(instr_label),
            run_time=2
        )
        self.wait(0.5)

        # Algorithm state
        pos = 50
        total_zeros = 0
        dial_pos_label = None  # Dynamic label on dial for non-multiples of 10

        # Process each movement
        for instruction, mouvement in mouvements:
            nouvelle_pos = pos + mouvement

            # Calculate zeros crossed
            if mouvement > 0:
                zeros_crossed = (nouvelle_pos // 100) - (pos // 100)
            elif mouvement < 0:
                zeros_crossed = ((pos - 1) // 100) - ((nouvelle_pos - 1) // 100)
            else:
                zeros_crossed = 0

            # Update instruction label
            direction = "Droite" if mouvement > 0 else "Gauche"
            new_instr = Text(f"Instruction: {instruction} ({direction})", font_size=24, color=BLUE)
            new_instr.next_to(zero_counter, DOWN, buff=0.5)

            # Remove previous dial position label if exists
            if dial_pos_label is not None:
                self.play(
                    Transform(instr_label, new_instr),
                    FadeOut(dial_pos_label),
                    run_time=0.3
                )
                dial_pos_label = None
            else:
                self.play(Transform(instr_label, new_instr), run_time=0.3)

            # Calculate rotation angle
            # Each position is 3.6 degrees (360/100)
            rotation_angle = -mouvement * 3.6 * DEGREES  # Negative because clockwise is positive movement

            # Animate pointer rotation
            self.play(
                Rotate(pointer, rotation_angle, about_point=dial_circle.get_center()),
                run_time=max(0.5, min(2, abs(mouvement) / 50))  # Scale time with movement size
            )

            # Flash if we crossed zero
            if zeros_crossed > 0:
                total_zeros += zeros_crossed

                # Big flash text in center of screen
                flash_text = Text(f"+{zeros_crossed}!", font_size=72, color=RED, weight=BOLD)
                flash_text.move_to(ORIGIN)

                # Flash circle around zero mark
                flash_ring = Circle(radius=0.4, color=RED, stroke_width=8)
                flash_ring.move_to(zero_mark.get_center())

                self.play(
                    FadeIn(flash_text, scale=0.5),
                    Create(flash_ring),
                    run_time=0.3
                )
                self.play(
                    FadeOut(flash_text, scale=1.5),
                    FadeOut(flash_ring),
                    run_time=0.4
                )

            # Update position (mod 100 for display)
            pos = nouvelle_pos
            display_pos = pos % 100
            if display_pos < 0:
                display_pos += 100

            # Update labels
            new_pos_label = Text(f"Position: {display_pos}", font_size=24, color=YELLOW)
            new_pos_label.to_edge(RIGHT).shift(UP * 2 + LEFT * 0.5)

            new_zero_counter = Text(f"Passages par 0: {total_zeros}", font_size=24, color=RED)
            new_zero_counter.next_to(new_pos_label, DOWN, buff=0.5)

            # Show position on dial if not a multiple of 10
            if display_pos % 10 != 0:
                dial_pos_label, _ = create_dial_pos_label(display_pos)
                self.play(
                    Transform(pos_label, new_pos_label),
                    Transform(zero_counter, new_zero_counter),
                    FadeIn(dial_pos_label),
                    run_time=0.3
                )
            else:
                self.play(
                    Transform(pos_label, new_pos_label),
                    Transform(zero_counter, new_zero_counter),
                    run_time=0.3
                )

            self.wait(0.3)

        # Final result
        final_box = SurroundingRectangle(zero_counter, color=GREEN, buff=0.2)
        result_text = Text(f"Resultat: {total_zeros}", font_size=36, color=GREEN)
        result_text.to_edge(DOWN, buff=0.5)

        self.play(
            Create(final_box),
            Write(result_text),
            run_time=1
        )
        self.wait(2)


class AlgorithmExplanation(Scene):
    """Scene explaining the optimization trick"""

    def construct(self):
        title = Text("Astuce d'optimisation", font_size=36)
        title.to_edge(UP)
        self.play(Write(title))

        # Naive approach
        naive = VGroup(
            Text("Approche naive: O(n * distance)", font_size=24, color=RED),
            Text("Simuler chaque clic un par un", font_size=20),
            Text("for i in range(distance): pos += 1", font_size=18, font="monospace"),
        )
        naive.arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        naive.shift(UP * 1.5)

        self.play(Write(naive), run_time=1.5)
        self.wait(1)

        # Optimized approach
        optim = VGroup(
            Text("Approche optimisee: O(n)", font_size=24, color=GREEN),
            Text("Calculer mathematiquement les passages par 0", font_size=20),
            Text("zeros = (new_pos // 100) - (pos // 100)", font_size=18, font="monospace"),
        )
        optim.arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        optim.shift(DOWN * 1)

        self.play(Write(optim), run_time=1.5)
        self.wait(1)

        # Example
        example = VGroup(
            Text("Exemple: pos=50, mouvement=+150", font_size=22, color=YELLOW),
            Text("new_pos = 200", font_size=20),
            Text("zeros = (200 // 100) - (50 // 100) = 2 - 0 = 2", font_size=18, font="monospace"),
        )
        example.arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        example.to_edge(DOWN, buff=0.8)

        self.play(Write(example), run_time=1.5)
        self.wait(2)


if __name__ == "__main__":
    print("Run with: manim -pql visualize_dial.py DialAnimation")
