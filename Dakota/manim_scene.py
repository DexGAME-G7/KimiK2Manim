from manim import *
import json, random, math, itertools as it

class DakotaLinguisticMap(Scene):
    """
    A poetic cartography of the Dakota grammar ruleset (1890 CE).
    Each rule is a star, each example a firefly, each connection a river of light.
    """
    def construct(self):
        # ---------------------------------------------------- 0. Load the cosmos
        with open("Dakota/grammar_full.json", encoding="utf-8") as f:
            cosmos = json.load(f)
        rules = cosmos["rules"][:18]          # first constellation
        stats = cosmos["statistics"]

        # ---------------------------------------------------- 1. Title & legend
        title = Text("Dakota Linguistic Map ‑ 1890", font="Minion Pro", color=YELLOW)
        subtitle = Text("A cartography of grammar rules", font="Minion Pro", color=GREY_A).scale(.5)
        subtitle.next_to(title, DOWN)
        legend = VGroup(
            Dot(color=BLUE, radius=.05), Text("rule", font="Minion Pro", color=WHITE).scale(.3),
            Dot(color=GREEN, radius=.04), Text("example", font="Minion Pro", color=WHITE).scale(.3),
            Dot(color=RED, radius=.03), Text("constraint", font="Minion Pro", color=WHITE).scale(.3)
        ).arrange(RIGHT, buff=.2).to_edge(DOWN, buff=.3)
        self.play(FadeIn(title, subtitle, legend), run_time=2)
        self.wait()

        # ---------------------------------------------------- 2. Aggregate halo
        halo = self.halo_of_stats(stats).scale(1.2).next_to(title, DOWN, buff=.6)
        self.play(LaggedStart(*[FadeIn(m, shift=UP) for m in halo], lag_ratio=.1))
        self.wait()

        # ---------------------------------------------------- 3. Constellation graph
        vertices, edges, layout = self.build_constellation(rules)
        g = Graph(vertices, edges, layout=layout,
                  vertex_config=self.vertex_style(rules),
                  edge_config={"stroke_opacity":.25, "stroke_width":1})
        g.scale_to_fit_width(config.frame_width*.9).shift(.5*DOWN)
        self.play(FadeOut(title, subtitle, halo), FadeIn(g), run_time=2)
        self.wait()

        # ---------------------------------------------------- 4. Zoom‑in river
        chosen = random.choice(rules)
        self.zoom_on_rule(g, chosen, rules)
        self.wait(3)

    # ------------------------------------------------ helpers
    def halo_of_stats(self, stats):
        """Golden rings whose radius encodes magnitude."""
        keys = ["total_rules", "total_examples", "total_interlinear"]
        colors = [YELLOW, TEAL, MAROON]
        maxv = max(stats[k] for k in keys)
        rings = VGroup()
        for k, col in zip(keys, colors):
            r = math.sqrt(stats[k]/maxv)*2
            c = Circle(radius=r, color=col, stroke_width=2)
            label = Text(f"{k.replace('_',' ')}: {stats[k]}", font="Minion Pro", color=col).scale(.25).move_to(c)
            rings.add(VGroup(c, label))
        rings.arrange(RIGHT, buff=.5)
        return rings

    def build_constellation(self, rules):
        """Star map: rules are stars, shared words are rivers."""
        vertices = [r["rule_id"] for r in rules]
        layout = {rid: np.array([random.uniform(-4,4), random.uniform(-3,3), 0])
                  for rid in vertices}
        # edges: shared dakota words
        edges = []
        for i, r1 in enumerate(rules):
            for j, r2 in enumerate(rules):
                if i<j and set(r1["dakota_pattern"].split()) & set(r2["dakota_pattern"].split()):
                    edges.append((r1["rule_id"], r2["rule_id"]))
        return vertices, edges, layout

    def vertex_style(self, rules):
        def style(rid):
            r = next(r for r in rules if r["rule_id"]==rid)
            col = {"morphology":BLUE, "syntax":GREEN, "phonology":RED}.get(r["rule_type"], GREY)
            return {"radius":.08, "color":col, "stroke_width":2, "fill_opacity":.9}
        return {rid: style(rid) for rid in [r["rule_id"] for r in rules]}

    def zoom_on_rule(self, graph, rule, all_rules):
        """Fly into one star, let its examples bloom like fireflies."""
        rid = rule["rule_id"]
        star = graph.vertices[rid]
        self.play(star.animate.scale(3).set_color(WHITE), run_time=1.5)

        # fireflies
        fireflies = VGroup(*[
            Text(ex["dakota"], font="Minion Pro", color=GREEN).scale(.35)
            for ex in rule["positive_examples"][:3]
        ])
        for ff in fireflies:
            ff.move_to(star.get_center())
            ff.save_state()
            ff.generate_target()
            ff.target.shift(random.uniform(-2,2)*RIGHT + random.uniform(-1,1)*UP)
            ff.target.set_opacity(0)

        # gloss rivers
        glosses = VGroup(*[
            Text(ex["gloss"], font="Minion Pro", color=YELLOW_A).scale(.25).next_to(ff, DOWN, buff=.1)
            for ff, ex in zip(fireflies, rule["positive_examples"][:3])
        ])

        self.play(LaggedStart(*[
            AnimationGroup(Restore(ff), FadeIn(g), run_time=2)
            for ff, g in zip(fireflies, glosses)
        ], lag_ratio=.3))
        self.play(LaggedStart(*[
            MoveToTarget(ff, rate_func=there_and_back_with_pause) for ff in fireflies
        ]), FadeOut(glosses))