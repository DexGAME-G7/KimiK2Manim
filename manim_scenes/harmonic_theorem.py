from manim import *
import numpy as np


class HarmonicDivisionTheorem(Scene):
    """
    45-second animation demonstrating the Harmonic Division Theorem.

    Mathematical Concept:
    Points A, C, D, B are in harmonic division if (A,B;C,D) = -1,
    where (A,B;C,D) is the cross-ratio: (AC·BD)/(BC·AD) = -1

    Visual Design:
    - Color-coded points: A (BLUE), C (GOLD), D (RED), B (GREEN)
    - Step-by-step LaTeX equation reveals
    - Smooth animations with glowing highlights
    - Elegant gradient background
    """

    def construct(self):
        # Set background gradient
        self.camera.background_color = "#001122"

        # [0-5s] Introduction & Setup
        self.intro_sequence()

        # [5-15s] Construct the Harmonic Division
        line, points, labels = self.construct_harmonic_division()

        # [15-28s] Demonstrate the Cross-Ratio
        self.demonstrate_cross_ratio(line, points, labels)

        # [28-40s] Visual Proof & Geometric Insight
        self.visual_proof(line, points, labels)

        # [40-45s] Conclusion
        self.conclusion()

    def intro_sequence(self):
        """[0-5s] Title and introduction."""
        title = Text("The Harmonic Division Theorem", font_size=54, color=GOLD)
        title.to_edge(UP, buff=0.5)

        subtitle = Text(
            "A geometric relationship in four collinear points",
            font_size=28,
            color=WHITE
        ).next_to(title, DOWN)

        self.play(Write(title), run_time=2)
        self.play(FadeIn(subtitle, shift=UP), run_time=1)
        self.wait(1)
        self.play(FadeOut(title), FadeOut(subtitle), run_time=1)

    def construct_harmonic_division(self):
        """[5-15s] Draw the geometric setup."""
        # Create horizontal line
        line = Line(LEFT * 5.5, RIGHT * 5.5, color=WHITE, stroke_width=2)

        # Define points with harmonic division
        # For simplicity: A at -3.5, C at -1, B at 3.5, D at 7 (external)
        A_pos = LEFT * 3.5
        C_pos = LEFT * 1
        B_pos = RIGHT * 3.5
        D_pos = RIGHT * 5.5  # Outside the segment AB

        # Create points with glowing halos
        A_core = Dot(A_pos, color=BLUE, radius=0.1)
        A_halo = Circle(radius=0.25, color=BLUE, stroke_width=2, stroke_opacity=0.5).move_to(A_pos)
        A = VGroup(A_halo, A_core)

        C_core = Dot(C_pos, color=GOLD, radius=0.1)
        C_halo = Circle(radius=0.25, color=GOLD, stroke_width=2, stroke_opacity=0.5).move_to(C_pos)
        C = VGroup(C_halo, C_core)

        B_core = Dot(B_pos, color=GREEN, radius=0.1)
        B_halo = Circle(radius=0.25, color=GREEN, stroke_width=2, stroke_opacity=0.5).move_to(B_pos)
        B = VGroup(B_halo, B_core)

        D_core = Dot(D_pos, color=RED, radius=0.1)
        D_halo = Circle(radius=0.25, color=RED, stroke_width=2, stroke_opacity=0.5).move_to(D_pos)
        D = VGroup(D_halo, D_core)

        points = {"A": A, "C": C, "D": D, "B": B}

        # Labels
        A_label = MathTex("A", color=BLUE, font_size=48).next_to(A, DOWN, buff=0.3)
        C_label = MathTex("C", color=GOLD, font_size=48).next_to(C, DOWN, buff=0.3)
        B_label = MathTex("B", color=GREEN, font_size=48).next_to(B, DOWN, buff=0.3)
        D_label = MathTex("D", color=RED, font_size=48).next_to(D, DOWN, buff=0.3)

        labels = {"A": A_label, "C": C_label, "D": D_label, "B": B_label}

        # Animate construction
        self.play(Create(line), run_time=1)
        self.play(
            FadeIn(A), FadeIn(C), FadeIn(B), FadeIn(D),
            run_time=1.5
        )
        self.play(
            Write(A_label), Write(C_label), Write(B_label), Write(D_label),
            run_time=1.5
        )

        # Show segments with labels
        AC_line_segment = Line(A_pos, C_pos, color=BLUE_C, stroke_width=8)
        CB_line_segment = Line(C_pos, B_pos, color=GOLD_C, stroke_width=8)

        AC_text = Text("AC", font_size=32, color=BLUE_C).next_to(AC_line_segment, UP, buff=0.2)
        CB_text = Text("CB", font_size=32, color=GOLD_C).next_to(CB_line_segment, UP, buff=0.2)

        self.play(
            Create(AC_line_segment), Write(AC_text),
            Create(CB_line_segment), Write(CB_text),
            run_time=2
        )

        # Display first equation
        eq1 = MathTex(
            r"\frac{AC}{CB}", "=", r"\frac{AD}{DB}",
            font_size=42
        ).to_corner(UL, buff=0.5)
        eq1[0].set_color(BLUE_C)
        eq1[2].set_color(RED_C)

        self.play(Write(eq1), run_time=2)
        self.wait(1)

        # Clean up segments
        self.play(
            FadeOut(AC_line_segment), FadeOut(AC_text),
            FadeOut(CB_line_segment), FadeOut(CB_text),
            run_time=0.5
        )

        return line, points, labels

    def demonstrate_cross_ratio(self, line, points, labels):
        """[15-28s] Show cross-ratio calculation."""
        # Highlight all four points
        self.play(
            Indicate(points["A"], color=BLUE, scale_factor=1.3),
            Indicate(points["C"], color=GOLD, scale_factor=1.3),
            Indicate(points["D"], color=RED, scale_factor=1.3),
            Indicate(points["B"], color=GREEN, scale_factor=1.3),
            run_time=1.5
        )

        # Cross-ratio definition
        cross_ratio_def = MathTex(
            r"(A, B; C, D)", "=", r"\frac{AC \cdot BD}{BC \cdot AD}",
            font_size=42
        ).to_edge(UP, buff=0.5)
        cross_ratio_def[0].set_color(YELLOW)

        self.play(Write(cross_ratio_def), run_time=2)
        self.wait(1)

        # Step-by-step calculation
        step1 = MathTex(
            r"= \frac{AC \cdot BD}{BC \cdot AD}",
            font_size=38
        ).next_to(cross_ratio_def, DOWN, buff=0.4)

        self.play(Write(step1), run_time=1.5)

        # Show the harmonic condition
        step2 = MathTex(
            r"= -1",
            font_size=48,
            color=GOLD
        ).next_to(step1, RIGHT, buff=0.5)

        self.play(
            Write(step2),
            Circumscribe(step2, color=YELLOW, fade_out=True, run_time=1.5),
            run_time=2
        )
        self.wait(1)

        # Visualize segments with colored lines
        A_pos = points["A"].get_center()
        C_pos = points["C"].get_center()
        D_pos = points["D"].get_center()
        B_pos = points["B"].get_center()

        AC_line = Line(A_pos, C_pos, color=BLUE, stroke_width=6)
        BD_line = Line(B_pos, D_pos, color=GREEN, stroke_width=6)
        BC_line = Line(B_pos, C_pos, color=GOLD, stroke_width=6)
        AD_line = Line(A_pos, D_pos, color=RED, stroke_width=6)

        # Show numerator segments
        numerator_label = Text("Numerator: AC · BD", font_size=28, color=BLUE).to_corner(UR, buff=0.5)
        self.play(
            Create(AC_line), Create(BD_line),
            FadeIn(numerator_label),
            run_time=2
        )
        self.wait(1)

        # Show denominator segments
        denominator_label = Text("Denominator: BC · AD", font_size=28, color=RED).next_to(numerator_label, DOWN)
        self.play(
            FadeOut(AC_line), FadeOut(BD_line),
            Create(BC_line), Create(AD_line),
            FadeIn(denominator_label),
            run_time=2
        )
        self.wait(1)

        # Clean up
        self.play(
            FadeOut(BC_line), FadeOut(AD_line),
            FadeOut(numerator_label), FadeOut(denominator_label),
            FadeOut(cross_ratio_def), FadeOut(step1), FadeOut(step2),
            run_time=1
        )

    def visual_proof(self, line, points, labels):
        """[28-40s] Geometric insight."""
        # Draw circle through A and B
        A_pos = points["A"].get_center()
        B_pos = points["B"].get_center()
        center = (A_pos + B_pos) / 2
        radius = np.linalg.norm(B_pos - center)

        circle = Circle(
            radius=radius,
            color=BLUE_C,
            stroke_width=2,
            stroke_opacity=0.7
        ).move_to(center)

        circle_label = Text("Circle through A and B", font_size=28, color=BLUE_C).to_corner(UR, buff=0.5)

        self.play(
            Create(circle),
            FadeIn(circle_label),
            run_time=2
        )
        self.wait(1)

        # Highlight harmonic conjugates
        conjugate_text = Text(
            "C and D are harmonic conjugates",
            font_size=32,
            color=GOLD
        ).next_to(circle_label, DOWN, buff=0.3)

        self.play(
            Write(conjugate_text),
            Indicate(points["C"], color=GOLD, scale_factor=1.5),
            Indicate(points["D"], color=RED, scale_factor=1.5),
            run_time=2
        )
        self.wait(1)

        # Complete theorem statement
        theorem = MathTex(
            r"\text{If } \frac{AC}{CB} = \frac{AD}{DB}, \text{ then } (A,B;C,D) = -1",
            font_size=36
        ).to_edge(DOWN, buff=0.5)
        theorem.set_color_by_tex("(A,B;C,D) = -1", GOLD)

        self.play(Write(theorem), run_time=3)
        self.wait(2)

        # Clean up for conclusion
        self.play(
            FadeOut(circle), FadeOut(circle_label),
            FadeOut(conjugate_text), FadeOut(theorem),
            run_time=1
        )

    def conclusion(self):
        """[40-45s] Final statement."""
        # Fade out all existing elements
        self.play(*[FadeOut(mob) for mob in self.mobjects], run_time=1)

        # Final boxed theorem
        final_theorem = MathTex(
            r"\boxed{\text{Harmonic Division: } (A,B;C,D) = -1}",
            font_size=52,
            color=GOLD
        ).move_to(ORIGIN)

        self.play(
            Write(final_theorem),
            final_theorem.animate.set_color(YELLOW),
            run_time=2
        )
        self.wait(1.5)

        # Elegant fade out
        self.play(FadeOut(final_theorem), run_time=1.5)
