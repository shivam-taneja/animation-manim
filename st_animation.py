from manim import *
import random
import numpy as np

class STReveal(Scene):
    def construct(self):
        # Vibrant gradient background (cyberpunk vibes)
        self.camera.background_color = "#0a0e27"
        
        # Create main "ST" with cyberpunk font style
        s = Text("S", font="Arial Black", weight=BOLD).scale(3.5)
        t = Text("T", font="Arial Black", weight=BOLD).scale(3.5)
        
        # Initial glitch colors
        s.set_color_by_gradient("#ff006e", "#8338ec")
        t.set_color_by_gradient("#3a86ff", "#06ffa5")
        
        st = VGroup(s, t).arrange(RIGHT, buff=0.2)
        st.move_to(ORIGIN)
        
        # Neon glow circles (particle effect)
        circles = VGroup(*[
            Circle(radius=0.15, color=random.choice(["#ff006e", "#8338ec", "#3a86ff", "#06ffa5"]), 
                   fill_opacity=0.8, stroke_width=0)
            .move_to([
                np.random.uniform(-4, 4),
                np.random.uniform(-4, 4),
                0
            ])
            for _ in range(25)
        ])
        
        # Rotating hexagon (tech frame)
        hexagon = RegularPolygon(n=6, color="#06ffa5", stroke_width=4, fill_opacity=0)
        hexagon.scale(2.8).rotate(PI/6)
        
        # Binary code rain (matrix style)
        binary_texts = VGroup(*[
            Text(
                "".join([str(np.random.randint(0, 2)) for _ in range(3)]),
                font="Courier New",
                color="#06ffa5",
                font_size=20
            ).move_to([np.random.uniform(-5, 5), np.random.uniform(-3, 4), 0])
            .set_opacity(0.4)
            for _ in range(15)
        ])
        
        # Glitch lines
        glitch_lines = VGroup(*[
            Line(
                start=[-6, y, 0],
                end=[6, y, 0],
                color="#ff006e",
                stroke_width=2
            ).set_opacity(0)
            for y in np.linspace(-3, 3, 8)
        ])
        
        # === ANIMATION SEQUENCE ===
        
        # 1. Binary rain appears
        self.add(binary_texts)
        self.play(
            binary_texts.animate.shift(DOWN * 2).set_opacity(0.2),
            run_time=1,
            rate_func=linear
        )
        
        # 2. Particles explode inward
        self.add(circles)
        self.play(
            *[circle.animate.move_to(ORIGIN).set_opacity(0) for circle in circles],
            run_time=0.8,
            rate_func=rush_into
        )
        
        # 3. Letters burst in with glitch effect
        s_glitch = s.copy().set_color("#ff006e").shift(LEFT*0.1)
        t_glitch = t.copy().set_color("#3a86ff").shift(RIGHT*0.1)
        
        self.add(s_glitch, t_glitch)
        self.play(
            FadeIn(s, scale=1.5),
            FadeIn(t, scale=1.5),
            run_time=0.3
        )
        self.remove(s_glitch, t_glitch)
        
        # 4. Hexagon scan effect
        self.play(
            Create(hexagon),
            run_time=0.8,
            rate_func=smooth
        )
        
        # 5. Hexagon rotates continuously while letters pulse
        self.play(
            Rotate(hexagon, angle=2*PI, rate_func=linear),
            st.animate.scale(1.15).set_opacity(0.9),
            run_time=1.2
        )
        
        # 6. Glitch effect - random horizontal lines flash
        for line in glitch_lines[:4]:
            self.add(line)
            line.set_opacity(0.8)
            self.wait(0.05)
            self.remove(line)
        
        # 7. Color shift explosion
        self.play(
            s.animate.set_color_by_gradient("#06ffa5", "#ffbe0b"),
            t.animate.set_color_by_gradient("#ff006e", "#8338ec"),
            hexagon.animate.set_color("#ffbe0b"),
            run_time=0.5
        )
        
        # 8. Scale back and rotate
        self.play(
            st.animate.scale(1/1.15),
            Rotate(hexagon, angle=-PI, rate_func=smooth),
            run_time=0.6
        )
        
        # 9. Final glitch burst
        self.play(
            *[Flash(letter, color="#06ffa5", line_length=0.3) for letter in [s, t]],
            run_time=0.4
        )
        
        # 10. Hold the epic frame
        self.wait(0.4)
        
        # 11. Particles explode outward
        new_circles = VGroup(*[
            Circle(radius=0.1, color=random.choice(["#ff006e", "#06ffa5"]), 
                   fill_opacity=0.9, stroke_width=0)
            .move_to(ORIGIN)
            for _ in range(20)
        ])
        self.add(new_circles)
        self.play(
            *[circle.animate.shift(
                [np.random.uniform(-5, 5), np.random.uniform(-5, 5), 0]
            ).set_opacity(0) for circle in new_circles],
            FadeOut(st),
            FadeOut(hexagon),
            FadeOut(binary_texts),
            run_time=0.7,
            rate_func=rush_from
        )