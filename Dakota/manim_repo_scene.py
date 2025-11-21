from manim import *

class DakotaArchitecture(Scene):
    def construct(self):
        self.camera.background_color = "#1e1e1e"

        # Colors
        blue = "#3b82f6"
        gold = "#f59e0b"
        white = "#ffffff"
        gray = "#9ca3af"

        # Title
        title = Text("Dakota1890: RL on Historical Text", font_size=48, color=white)
        subtitle = Text("Grammar Extraction → GRPO Training → Generalization", font_size=28, color=gray)
        subtitle.next_to(title, DOWN, buff=0.3)
        header = VGroup(title, subtitle).to_edge(UP, buff=0.5)

        # 1. Flow: Textbook → VLM → Grammar → RL → Model
        # Nodes
        textbook = RoundedRectangle(height=1.2, width=3, color=blue, fill_opacity=0.3, corner_radius=0.2)
        textbook_label = Text("1890 Textbook", font_size=24, color=white).move_to(textbook.get_center())

        vlm = RoundedRectangle(height=1.2, width=3, color=blue, fill_opacity=0.3, corner_radius=0.2)
        vlm_label = Text("VLM Extraction", font_size=24, color=white).move_to(vlm.get_center())

        grammar = RoundedRectangle(height=1.2, width=3, color=blue, fill_opacity=0.3, corner_radius=0.2)
        grammar_label = Text("Grammar Rules", font_size=24, color=white).move_to(grammar.get_center())

        rl = RoundedRectangle(height=1.2, width=3, color=gold, fill_opacity=0.3, corner_radius=0.2)
        rl_label = Text("GRPO Training", font_size=24, color=white).move_to(rl.get_center())

        model = RoundedRectangle(height=1.2, width=3, color=gold, fill_opacity=0.3, corner_radius=0.2)
        model_label = Text("Trained Model", font_size=24, color=white).move_to(model.get_center())

        # Position nodes horizontally
        nodes = VGroup(textbook, vlm, grammar, rl, model).arrange(RIGHT, buff=1.5).shift(DOWN*0.5)

        # Arrows
        arrow1 = Arrow(textbook.get_right(), vlm.get_left(), color=white, buff=0.2)
        arrow2 = Arrow(vlm.get_right(), grammar.get_left(), color=white, buff=0.2)
        arrow3 = Arrow(grammar.get_right(), rl.get_left(), color=white, buff=0.2)
        arrow4 = Arrow(rl.get_right(), model.get_left(), color=white, buff=0.2)

        # VLM details
        vlm_detail = Text("Claude Sonnet 4.5\n92-95% accuracy", font_size=18, color=gray).next_to(vlm, DOWN, buff=0.3)

        # 2. Reward Function visualization
        reward_box = RoundedRectangle(height=2, width=5, color=gold, fill_opacity=0.2, corner_radius=0.3)
        reward_box.to_edge(DL, buff=1)
        reward_title = Text("Compositional Reward", font_size=24, color=white).next_to(reward_box.get_top(), DOWN, buff=0.2).scale(0.9)
        reward_eq = MathTex(
            r"\text{reward} = (0.4\,\text{char} + 0.4\,\text{affix} + 0.2\,\text{sem}) \times \text{diff}",
            font_size=28,
            color=white
        ).move_to(reward_box.get_center())
        reward_group = VGroup(reward_box, reward_title, reward_eq)

        # 3. Generalized Applications
        center_app = Circle(radius=0.8, color=blue, fill_opacity=0.3)
        center_label = Text("Language", font_size=24, color=white).move_to(center_app.get_center())
        center_group = VGroup(center_app, center_label).to_edge(DR, buff=1.5)

        # Application nodes around center
        legal = RoundedRectangle(height=0.8, width=2.5, color=blue, fill_opacity=0.3, corner_radius=0.2)
        legal_label = Text("Legal", font_size=20, color=white).move_to(legal.get_center())
        legal.next_to(center_app, LEFT, buff=1.5)

        bio = RoundedRectangle(height=0.8, width=2.5, color=blue, fill_opacity=0.3, corner_radius=0.2)
        bio_label = Text("Biology", font_size=20, color=white).move_to(bio.get_center())
        bio.next_to(center_app, UP, buff=1.5)

        code = RoundedRectangle(height=0.8, width=2.5, color=blue, fill_opacity=0.3, corner_radius=0.2)
        code_label = Text("Code Migration", font_size=20, color=white).move_to(code.get_center())
        code.next_to(center_app, RIGHT, buff=1.5)

        app_arrows = VGroup(
            Arrow(center_app.get_left(), legal.get_right(), color=white, buff=0.2),
            Arrow(center_app.get_top(), bio.get_bottom(), color=white, buff=0.2),
            Arrow(center_app.get_right(), code.get_left(), color=white, buff=0.2),
        )

        # Application details
        legal_detail = Text("Tax Code → Compliance", font_size=16, color=gray).next_to(legal, DOWN, buff=0.2)
        bio_detail = Text("Papers → Protein rules", font_size=16, color=gray).next_to(bio, LEFT, buff=0.2)
        code_detail = Text("COBOL manuals → Agents", font_size=16, color=gray).next_to(code, DOWN, buff=0.2)

        # Animations
        self.play(FadeIn(header))
        self.wait(0.5)

        # Flow animation
        self.play(
            FadeIn(textbook), FadeIn(textbook_label),
            FadeIn(vlm), FadeIn(vlm_label),
            FadeIn(grammar), FadeIn(grammar_label),
            FadeIn(rl), FadeIn(rl_label),
            FadeIn(model), FadeIn(model_label),
            run_time=1
        )
        self.play(
            Create(arrow1), Create(arrow2), Create(arrow3), Create(arrow4),
            FadeIn(vlm_detail),
            run_time=1
        )
        self.wait(1)

        # Reward function
        self.play(FadeIn(reward_group), run_time=1)
        self.wait(1)

        # Applications expansion
        self.play(
            FadeIn(center_group),
            FadeIn(legal), FadeIn(legal_label), FadeIn(legal_detail),
            FadeIn(bio), FadeIn(bio_label), FadeIn(bio_detail),
            FadeIn(code), FadeIn(code_label), FadeIn(code_detail),
            Create(app_arrows),
            run_time=1.5
        )
        self.wait(2)

        # Highlight curriculum
        curriculum = Text("Curriculum: Easy → Medium → Hard", font_size=24, color=gold).to_edge(DOWN, buff=0.5)
        self.play(Write(curriculum), run_time=1)
        self.wait(2)