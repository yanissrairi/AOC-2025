"""
Manim visualization of AOC Day 2 - Repeating Pattern IDs
Run with: manim -pql visualize_patterns.py PatternAnimation

Amélioré avec les best practices Manim 2025:
- Rate functions pour animations fluides
- TransformMatchingTex pour transformations mathématiques
- LaggedStart pour animations en cascade
- Indicate/Circumscribe pour mise en évidence pédagogique
"""
from manim import *
import numpy as np

# Rate functions disponibles dans manim
# smooth, linear, there_and_back, rush_into, rush_from, etc.


# === CONFIGURATION CENTRALISÉE ===
class Config:
    """Constantes pour cohérence visuelle"""
    # Tailles de police
    TITLE_SIZE = 32
    SUBTITLE_SIZE = 24
    BODY_SIZE = 20
    FORMULA_SIZE = 32
    SMALL_SIZE = 16

    # Espacements
    BUFF_LARGE = 0.5
    BUFF_MEDIUM = 0.35
    BUFF_SMALL = 0.2

    # Palette de couleurs cohérente
    PRIMARY = BLUE_C
    SECONDARY = GREEN_C
    ACCENT = YELLOW_C
    INVALID = RED_C
    MUTED = GRAY_B
    HIGHLIGHT = GOLD_C

    # Durées d'animation
    FAST = 0.3
    NORMAL = 0.5
    SLOW = 1.0


# Test data (petit subset pour la visualisation)
TEST_RANGES = [
    (11, 22),
    (95, 115),
    (998, 1012),
]


class PatternAnimation(Scene):
    def construct(self):
        # === INTRO AVEC ANIMATION FLUIDE ===
        title = Text("AOC Day 2 - IDs avec motifs répétés", font_size=Config.TITLE_SIZE)
        title.to_edge(UP, buff=Config.BUFF_MEDIUM)
        self.play(Write(title), rate_func=smooth, run_time=Config.SLOW)

        # Subtitle avec apparition douce
        subtitle = Text(
            "ID invalide = chiffres répétés: 11, 123123, 5555...",
            font_size=Config.SUBTITLE_SIZE,
            color=Config.ACCENT
        )
        subtitle.next_to(title, DOWN, buff=Config.BUFF_MEDIUM)
        self.play(
            FadeIn(subtitle, shift=UP * 0.2),
            rate_func=smooth,
            run_time=Config.NORMAL
        )
        self.wait(0.8)

        # === EXEMPLES AVEC LAGGED START (CASCADE) ===
        examples = VGroup(
            self.create_pattern_example("1", 2, "11"),
            self.create_pattern_example("12", 2, "1212"),
            self.create_pattern_example("123", 2, "123123"),
            self.create_pattern_example("7", 3, "777"),
        )
        examples.arrange(RIGHT, buff=0.8)
        examples.next_to(subtitle, DOWN, buff=Config.BUFF_LARGE)

        # Animation en cascade élégante
        self.play(
            LaggedStart(
                *[FadeIn(ex, shift=DOWN * 0.3) for ex in examples],
                lag_ratio=0.15,
                run_time=1.5
            ),
            rate_func=smooth
        )

        # Highlight rapide de chaque exemple
        for ex in examples:
            self.play(Indicate(ex, color=Config.HIGHLIGHT), run_time=0.25)
        self.wait(0.8)

        # Transition fluide
        self.play(
            FadeOut(examples, shift=DOWN * 0.3),
            FadeOut(subtitle, shift=UP * 0.2),
            rate_func=smooth,
            run_time=Config.NORMAL
        )

        # === ASTUCE DU MULTIPLICATEUR ===
        trick_title = Text("Astuce: Multiplicateurs magiques", font_size=Config.TITLE_SIZE, color=Config.SECONDARY)
        trick_title.next_to(title, DOWN, buff=Config.BUFF_SMALL)
        self.play(
            FadeIn(trick_title, shift=DOWN * 0.2),
            rate_func=smooth,
            run_time=Config.NORMAL
        )

        # LEFT SIDE: Démonstration mathématique avec TransformMatchingTex
        left_title = Text("Comment ça marche?", font_size=Config.SUBTITLE_SIZE, color=Config.ACCENT)
        left_title.shift(LEFT * 3.2 + UP * 0.8)

        # Formules pour transformation progressive
        step1 = MathTex(r"12", r"+", r"12 \times 100", r"+", r"12 \times 10000", font_size=Config.FORMULA_SIZE)
        step1.next_to(left_title, DOWN, buff=Config.BUFF_MEDIUM)

        step2 = MathTex(r"=", r"12", r"\times", r"(1 + 100 + 10000)", font_size=Config.FORMULA_SIZE)
        step2.next_to(step1, DOWN, buff=Config.BUFF_SMALL)

        step3 = MathTex(r"=", r"12", r"\times", r"10101", font_size=36)
        step3.next_to(step2, DOWN, buff=Config.BUFF_SMALL)
        step3[3].set_color(Config.SECONDARY)  # Colore le multiplicateur

        left_group = VGroup(left_title, step1, step2, step3)

        # RIGHT SIDE: Exemples pratiques
        right_title = Text("Exemples:", font_size=Config.SUBTITLE_SIZE, color=Config.ACCENT)
        right_title.shift(RIGHT * 3.5 + UP * 0.8)

        formulas = VGroup(
            MathTex(r"12 \times 101 = 1212", font_size=Config.FORMULA_SIZE),
            MathTex(r"7 \times 111 = 777", font_size=Config.FORMULA_SIZE),
            MathTex(r"5 \times 11 = 55", font_size=Config.FORMULA_SIZE),
        )
        formulas.arrange(DOWN, buff=Config.BUFF_MEDIUM)
        formulas.next_to(right_title, DOWN, buff=Config.BUFF_MEDIUM)

        right_group = VGroup(right_title, formulas)

        # Animate left side avec transitions fluides
        self.play(Write(left_title), rate_func=smooth)
        self.play(Write(step1), run_time=0.8, rate_func=smooth)
        self.play(Write(step2), run_time=0.6, rate_func=smooth)
        self.play(Write(step3), run_time=0.6, rate_func=smooth)

        # Mise en évidence du multiplicateur magique
        magic_box = SurroundingRectangle(step3[3], color=Config.HIGHLIGHT, buff=0.1)
        self.play(Create(magic_box), run_time=Config.FAST)
        self.play(Indicate(step3[3], scale_factor=1.3, color=Config.HIGHLIGHT), run_time=0.4)

        # Animate right side en cascade
        self.play(Write(right_title), rate_func=smooth)
        self.play(
            LaggedStart(
                *[FadeIn(f, shift=LEFT * 0.3) for f in formulas],
                lag_ratio=0.2,
                run_time=1.2
            ),
            rate_func=smooth
        )

        # Separator line animée
        line = Line(UP * 1.2, DOWN * 2.5, color=Config.MUTED, stroke_width=2)
        self.play(Create(line), run_time=Config.FAST, rate_func=smooth)

        self.wait(1.2)

        # Transition fluide vers la démo
        self.play(
            FadeOut(left_group),
            FadeOut(right_group),
            FadeOut(trick_title),
            FadeOut(line),
            FadeOut(magic_box),
            rate_func=smooth,
            run_time=Config.NORMAL
        )

        # Demo with a small range
        self.demo_range(11, 22)

        self.wait(2)

    def create_pattern_example(self, motif, repetitions, result):
        """Create a visual for a pattern example avec style amélioré"""
        group = VGroup()

        # Utilise les couleurs de la config
        motif_text = Text(motif, font_size=28, color=Config.PRIMARY, weight=BOLD)
        times = MathTex(r"\times", font_size=24)
        times.next_to(motif_text, RIGHT, buff=0.1)
        rep_text = Text(str(repetitions), font_size=28, color=Config.SECONDARY, weight=BOLD)
        rep_text.next_to(times, RIGHT, buff=0.1)
        equals = MathTex(r"=", font_size=24)
        equals.next_to(rep_text, RIGHT, buff=0.1)
        result_text = Text(result, font_size=28, color=Config.INVALID, weight=BOLD)
        result_text.next_to(equals, RIGHT, buff=0.1)

        group.add(motif_text, times, rep_text, equals, result_text)
        return group

    def demo_range(self, start, end):
        """Demonstrate finding patterns in a range avec animations avancées"""
        range_title = Text(f"Range [{start}, {end}]", font_size=28, color=Config.PRIMARY)
        range_title.shift(UP * 2)
        self.play(
            FadeIn(range_title, shift=DOWN * 0.2),
            rate_func=smooth,
            run_time=Config.NORMAL
        )

        # Create number line visualization
        numbers = list(range(start, end + 1))
        invalid_ids = {11, 22}  # Known invalid IDs in this range

        # Create boxes for each number avec style amélioré
        num_boxes = VGroup()
        for i, n in enumerate(numbers):
            is_invalid = n in invalid_ids
            color = Config.INVALID if is_invalid else Config.MUTED
            opacity = 1.0 if is_invalid else 0.2

            box = VGroup()
            rect = RoundedRectangle(
                width=0.8, height=0.6,
                corner_radius=0.08,
                fill_color=color,
                fill_opacity=opacity,
                stroke_width=1.5,
                stroke_color=WHITE if is_invalid else GRAY
            )
            label = Text(str(n), font_size=Config.SMALL_SIZE, weight=BOLD if is_invalid else NORMAL)
            label.move_to(rect.get_center())
            box.add(rect, label)
            num_boxes.add(box)

        # Arrange in grid
        num_boxes.arrange_in_grid(rows=2, buff=0.15)
        num_boxes.move_to(ORIGIN)
        num_boxes.scale(0.9)

        # Animation cascade pour l'apparition des nombres
        self.play(
            LaggedStart(
                *[FadeIn(box, shift=UP * 0.15, scale=0.8) for box in num_boxes],
                lag_ratio=0.03,
                run_time=1.8
            ),
            rate_func=smooth
        )

        # Label pour les invalides
        invalid_label = Text("IDs invalides trouvés:", font_size=Config.SUBTITLE_SIZE, color=Config.INVALID)
        invalid_label.next_to(num_boxes, DOWN, buff=Config.BUFF_LARGE)
        self.play(Write(invalid_label), rate_func=smooth)

        # === SCANNER ANIMATION ===
        # Crée un scanner qui parcourt les nombres
        scanner = Rectangle(
            width=0.9, height=0.7,
            stroke_color=Config.ACCENT,
            stroke_width=3,
            fill_opacity=0
        )
        scanner.move_to(num_boxes[0])
        self.play(FadeIn(scanner), run_time=Config.FAST)

        # Scan à travers tous les nombres
        for idx, n in enumerate(numbers):
            target_pos = num_boxes[idx].get_center()

            if n in invalid_ids:
                # Mouvement vers l'ID invalide
                self.play(scanner.animate.move_to(target_pos), run_time=0.12)

                # Flash et effet Circumscribe pour les invalides
                self.play(
                    Circumscribe(num_boxes[idx], color=Config.ACCENT, buff=0.05, time_width=0.5),
                    Flash(target_pos, color=Config.INVALID, flash_radius=0.4, num_lines=12),
                    run_time=0.4
                )

                # Explication
                s = str(n)
                half = len(s) // 2
                motif = s[:half] if half > 0 else s[0]
                reason = Text(
                    f"{n} = {motif} × {len(s)//len(motif)}",
                    font_size=18,
                    color=Config.ACCENT,
                    weight=BOLD
                )

                # Position selon la ligne
                if idx < 6:
                    reason.next_to(num_boxes[idx], UP, buff=0.15)
                else:
                    reason.next_to(num_boxes[idx], DOWN, buff=0.15)

                self.play(FadeIn(reason, shift=UP * 0.1), run_time=Config.FAST)
                self.wait(0.4)
                self.play(FadeOut(reason), run_time=0.2)
            else:
                # Mouvement rapide pour les nombres valides
                self.play(scanner.animate.move_to(target_pos), run_time=0.06)

        # Fin du scan
        self.play(FadeOut(scanner), run_time=Config.FAST)

        # === RÉSUMÉ FINAL ===
        total = sum(invalid_ids)
        summary = Text(
            f"Somme: {' + '.join(map(str, sorted(invalid_ids)))} = {total}",
            font_size=Config.SUBTITLE_SIZE,
            color=Config.SECONDARY
        )
        summary.next_to(invalid_label, DOWN, buff=Config.BUFF_MEDIUM)

        # Animation finale avec effet
        self.play(
            Write(summary),
            rate_func=smooth,
            run_time=Config.NORMAL
        )
        self.play(Indicate(summary, color=Config.HIGHLIGHT), run_time=0.5)


class MultiplierExplanation(Scene):
    """Scene explaining the multiplier optimization avec animations avancées"""

    def construct(self):
        title = Text("Comment fonctionne le multiplicateur?", font_size=Config.TITLE_SIZE)
        title.to_edge(UP)
        self.play(Write(title), rate_func=smooth, run_time=Config.SLOW)

        # === CONSTRUCTION VISUELLE DU PATTERN ===
        motif = Text("12", font_size=48, color=Config.PRIMARY, weight=BOLD)
        motif.shift(UP * 1.5)
        self.play(FadeIn(motif, scale=0.5), rate_func=smooth)

        # Clone avec animation élégante
        copies = VGroup(
            Text("12", font_size=48, color=Config.PRIMARY, weight=BOLD),
            Text("12", font_size=48, color=Config.SECONDARY, weight=BOLD),
            Text("12", font_size=48, color=Config.ACCENT, weight=BOLD),
        )
        copies.arrange(RIGHT, buff=0)
        copies.shift(UP * 0.5)

        # Animation de copie progressive
        self.play(TransformFromCopy(motif, copies[0]), run_time=0.5, rate_func=smooth)
        self.play(
            FadeIn(copies[1], shift=LEFT * 0.3),
            run_time=Config.FAST,
            rate_func=smooth
        )
        self.play(
            FadeIn(copies[2], shift=LEFT * 0.3),
            run_time=Config.FAST,
            rate_func=smooth
        )

        # Résultat avec effet
        result = Text("= 121212", font_size=48, color=Config.INVALID, weight=BOLD)
        result.next_to(copies, RIGHT, buff=0.3)
        self.play(Write(result), rate_func=smooth)
        self.play(Indicate(result, color=Config.HIGHLIGHT), run_time=0.4)
        self.wait(0.4)

        # Transition vers les maths
        self.play(FadeOut(motif), rate_func=smooth)

        # === DÉMONSTRATION MATHÉMATIQUE ===
        math_title = Text("Mathématiquement:", font_size=28, color=Config.ACCENT)
        math_title.shift(DOWN * 0.5)
        self.play(FadeIn(math_title, shift=UP * 0.2), rate_func=smooth)

        # Formules avec mise en page pour TransformMatchingTex
        formula = MathTex(
            r"12", r"\times", r"10000", r"+",
            r"12", r"\times", r"100", r"+",
            r"12", r"\times", r"1",
            font_size=Config.FORMULA_SIZE
        )
        formula.next_to(math_title, DOWN, buff=Config.BUFF_MEDIUM)

        formula2 = MathTex(
            r"=", r"12", r"\times", r"(", r"10000", r"+", r"100", r"+", r"1", r")",
            font_size=Config.FORMULA_SIZE
        )
        formula2.next_to(formula, DOWN, buff=Config.BUFF_SMALL)

        formula3 = MathTex(
            r"=", r"12", r"\times", r"10101",
            font_size=36
        )
        formula3.next_to(formula2, DOWN, buff=Config.BUFF_SMALL)
        formula3[3].set_color(Config.SECONDARY)  # Highlight le multiplicateur

        # Animation des formules
        self.play(Write(formula), run_time=0.8, rate_func=smooth)
        self.wait(0.3)
        self.play(Write(formula2), run_time=0.7, rate_func=smooth)
        self.wait(0.3)
        self.play(Write(formula3), run_time=0.6, rate_func=smooth)

        # Box animée autour du multiplicateur
        box = SurroundingRectangle(formula3[3], color=Config.HIGHLIGHT, buff=0.1, corner_radius=0.05)
        self.play(Create(box), rate_func=smooth)
        self.play(
            Circumscribe(formula3[3], color=Config.HIGHLIGHT, buff=0.15),
            run_time=0.6
        )

        # Conclusion avec effet
        conclusion = Text("10101 = le multiplicateur magique!", font_size=Config.SUBTITLE_SIZE, color=Config.SECONDARY)
        conclusion.to_edge(DOWN, buff=Config.BUFF_LARGE)
        self.play(
            FadeIn(conclusion, shift=UP * 0.3),
            rate_func=smooth
        )
        self.play(Indicate(conclusion, scale_factor=1.1, color=Config.HIGHLIGHT), run_time=0.5)

        self.wait(1.5)


class AlgorithmComparison(Scene):
    """Compare naive vs optimized approach avec visualisation de vitesse"""

    def construct(self):
        title = Text("Naive vs Optimisé", font_size=36, weight=BOLD)
        title.to_edge(UP)
        self.play(Write(title), rate_func=smooth, run_time=Config.SLOW)

        # === APPROCHE NAIVE (GAUCHE) ===
        naive_title = Text("Approche Naive", font_size=Config.SUBTITLE_SIZE, color=Config.INVALID, weight=BOLD)
        naive_title.shift(LEFT * 3.5 + UP * 2)
        self.play(FadeIn(naive_title, shift=DOWN * 0.2), rate_func=smooth)

        naive_steps = VGroup(
            Text("Pour chaque nombre n:", font_size=18),
            Text("  Convertir en string", font_size=Config.SMALL_SIZE, color=Config.MUTED),
            Text("  Tester tous les motifs", font_size=Config.SMALL_SIZE, color=Config.MUTED),
            Text("  Vérifier répétition", font_size=Config.SMALL_SIZE, color=Config.MUTED),
            Text("", font_size=Config.SMALL_SIZE),
            MathTex(r"O(\text{range} \times \text{digits})", font_size=22, color=Config.INVALID),
        )
        naive_steps.arrange(DOWN, aligned_edge=LEFT, buff=0.15)
        naive_steps.next_to(naive_title, DOWN, buff=Config.BUFF_MEDIUM)
        self.play(
            LaggedStart(
                *[FadeIn(s, shift=RIGHT * 0.2) for s in naive_steps],
                lag_ratio=0.1,
                run_time=1.2
            ),
            rate_func=smooth
        )

        # === APPROCHE OPTIMISÉE (DROITE) ===
        opt_title = Text("Approche Optimisée", font_size=Config.SUBTITLE_SIZE, color=Config.SECONDARY, weight=BOLD)
        opt_title.shift(RIGHT * 3 + UP * 2)
        self.play(FadeIn(opt_title, shift=DOWN * 0.2), rate_func=smooth)

        opt_steps = VGroup(
            Text("Pour chaque multiplicateur:", font_size=18),
            Text("  Calculer bornes motif", font_size=Config.SMALL_SIZE, color=Config.MUTED),
            Text("  motif × mult = pattern", font_size=Config.SMALL_SIZE, color=Config.MUTED),
            Text("  Vérifier dans range", font_size=Config.SMALL_SIZE, color=Config.MUTED),
            Text("", font_size=Config.SMALL_SIZE),
            MathTex(r"O(\text{patterns})", font_size=22, color=Config.SECONDARY),
        )
        opt_steps.arrange(DOWN, aligned_edge=LEFT, buff=0.15)
        opt_steps.next_to(opt_title, DOWN, buff=Config.BUFF_MEDIUM)
        self.play(
            LaggedStart(
                *[FadeIn(s, shift=LEFT * 0.2) for s in opt_steps],
                lag_ratio=0.1,
                run_time=1.2
            ),
            rate_func=smooth
        )

        # VS au centre
        vs = Text("VS", font_size=36, color=Config.ACCENT, weight=BOLD)
        vs.move_to(ORIGIN + UP * 0.5)
        self.play(FadeIn(vs, scale=1.5), rate_func=smooth)
        self.play(Indicate(vs, scale_factor=1.2, color=Config.HIGHLIGHT), run_time=0.4)

        # === VISUALISATION DE VITESSE (BARRES DE PROGRESSION) ===
        bar_label = Text("Temps de calcul:", font_size=Config.BODY_SIZE, color=WHITE)
        bar_label.shift(DOWN * 1.3)
        self.play(FadeIn(bar_label), rate_func=smooth)

        # Barre naive (rouge, longue)
        naive_bar_bg = RoundedRectangle(
            width=5, height=0.4,
            corner_radius=0.1,
            fill_color=GRAY_E,
            fill_opacity=0.3,
            stroke_width=0
        )
        naive_bar_bg.shift(DOWN * 1.8 + LEFT * 1.5)

        naive_bar = RoundedRectangle(
            width=0.01, height=0.35,
            corner_radius=0.08,
            fill_color=Config.INVALID,
            fill_opacity=0.9,
            stroke_width=0
        )
        naive_bar.align_to(naive_bar_bg, LEFT)
        naive_bar.shift(DOWN * 1.8 + LEFT * 1.5)

        naive_label = Text("Naive", font_size=14, color=Config.INVALID)
        naive_label.next_to(naive_bar_bg, LEFT, buff=0.2)

        # Barre optimisée (verte, courte)
        opt_bar_bg = RoundedRectangle(
            width=5, height=0.4,
            corner_radius=0.1,
            fill_color=GRAY_E,
            fill_opacity=0.3,
            stroke_width=0
        )
        opt_bar_bg.shift(DOWN * 2.4 + LEFT * 1.5)

        opt_bar = RoundedRectangle(
            width=0.01, height=0.35,
            corner_radius=0.08,
            fill_color=Config.SECONDARY,
            fill_opacity=0.9,
            stroke_width=0
        )
        opt_bar.align_to(opt_bar_bg, LEFT)
        opt_bar.shift(DOWN * 2.4 + LEFT * 1.5)

        opt_label = Text("Optimisé", font_size=14, color=Config.SECONDARY)
        opt_label.next_to(opt_bar_bg, LEFT, buff=0.2)

        # Afficher les backgrounds et labels
        self.play(
            FadeIn(naive_bar_bg), FadeIn(naive_label),
            FadeIn(opt_bar_bg), FadeIn(opt_label),
            run_time=Config.FAST
        )

        # Animation des barres - la naive est 36x plus lente
        # On anime en parallèle mais avec des temps différents
        self.add(naive_bar, opt_bar)

        # Optimisé finit très vite
        self.play(
            opt_bar.animate.stretch_to_fit_width(5 / 36).align_to(opt_bar_bg, LEFT),
            run_time=0.1,
            rate_func=smooth
        )

        # Checkmark pour optimisé
        check = Text("✓", font_size=24, color=Config.SECONDARY)
        check.next_to(opt_bar, RIGHT, buff=0.3)
        self.play(FadeIn(check, scale=1.5), run_time=0.2)

        # Naive continue...
        self.play(
            naive_bar.animate.stretch_to_fit_width(5).align_to(naive_bar_bg, LEFT),
            run_time=2.5,
            rate_func=smooth
        )

        # === RÉSULTAT FINAL ===
        comparison = VGroup(
            Text("2,500,000 tests", font_size=Config.SUBTITLE_SIZE, color=Config.INVALID),
            MathTex(r"\rightarrow", font_size=28),
            Text("~1,000 calculs", font_size=Config.SUBTITLE_SIZE, color=Config.SECONDARY),
        )
        comparison.arrange(RIGHT, buff=0.3)
        comparison.shift(DOWN * 3.2)
        self.play(
            LaggedStart(
                *[FadeIn(c, shift=UP * 0.2) for c in comparison],
                lag_ratio=0.2
            ),
            rate_func=smooth,
            run_time=0.8
        )

        # Speedup avec effet spectaculaire
        speedup = Text("36× plus rapide!", font_size=32, color=Config.HIGHLIGHT, weight=BOLD)
        speedup.next_to(comparison, RIGHT, buff=0.5)
        self.play(
            FadeIn(speedup, scale=0.5),
            rate_func=smooth
        )
        self.play(
            Circumscribe(speedup, color=Config.HIGHLIGHT, buff=0.1),
            Flash(speedup.get_center(), color=Config.ACCENT, flash_radius=0.8, num_lines=16),
            run_time=0.8
        )

        self.wait(1.5)


if __name__ == "__main__":
    print("Run with: manim -pql visualize_patterns.py PatternAnimation")
    print("Other scenes: MultiplierExplanation, AlgorithmComparison")
