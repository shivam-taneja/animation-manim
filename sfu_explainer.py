from manim import *

# --- Global Styles ---
MAIN_FONT = "Inter"

# --- "Modern Tech" Professional Palette ---
# No cheap neon. Deep, rich, and clean colors.
BG_COLOR = "#0F172A"       # Deep Slate (The same base you liked)
NODE_COLOR = "#38BDF8"     # Sky Blue (The Users)
SFU_COLOR = "#FBBF24"      # Warm Amber/Gold (The Traffic Controller)
CHAOS_COLOR = "#F471B5"    # Soft Rose (The "Shouting" lines - distinct but not aggressive)
CLEAN_COLOR = "#34D399"    # Emerald Green (The "Efficient" lines)
TEXT_COLOR = "#F8FAFC"     # Off-White

class SFUExplainer(Scene):
    def construct(self):
        self.camera.background_color = BG_COLOR

        # --- PART 1: The Concept ("SFU / Traffic Controller") ---
        
        # 1. Title
        title = Text("SFU", font=MAIN_FONT, weight=BOLD, font_size=70, color=SFU_COLOR)
        subtitle = Text("Selective Forwarding Unit", font=MAIN_FONT, font_size=30, color=TEXT_COLOR)
        subtitle.next_to(title, DOWN, buff=0.3)
        
        self.play(Write(title), FadeIn(subtitle, shift=UP*0.2), run_time=1)
        self.wait(0.5)
        
        # Move Title away to Top Left
        header = VGroup(title, subtitle)
        self.play(header.animate.scale(0.5).to_corner(UL), run_time=0.8)

        # 2. The Metaphor Text
        metaphor_text = Text("The Traffic Controller", font=MAIN_FONT, color=SFU_COLOR, font_size=36)
        metaphor_text.to_edge(UP)
        self.play(Write(metaphor_text))

        # --- PART 2: The "Before" - Mesh Chaos ("Everyone Shouting") ---

        # Create 5 Users arranged in a circle
        users = VGroup()
        radius = 2.5
        for i in range(5):
            # Create a user icon (Circle with a letter)
            dot = Circle(radius=0.3, color=NODE_COLOR, fill_opacity=0).set_fill(color=NODE_COLOR, opacity=0.2)
            dot.set_stroke(width=4)
            label = Text(str(i+1), font=MAIN_FONT, font_size=20, color=TEXT_COLOR).move_to(dot.center())
            user = VGroup(dot, label)
            
            # Position in a circle
            angle = i * (2 * PI / 5) + PI/2
            user.move_to(np.array([np.cos(angle)*radius, np.sin(angle)*radius, 0]))
            users.add(user)

        self.play(FadeIn(users, scale=0.8))

        # Create the Chaos Lines (Full Mesh)
        chaos_lines = VGroup()
        for i in range(len(users)):
            for j in range(i + 1, len(users)):
                line = Line(users[i].get_center(), users[j].get_center(), color=CHAOS_COLOR)
                line.set_stroke(width=2, opacity=0.6)
                chaos_lines.add(line)

        # Animate "Shouting"
        chaos_label = Text("Mesh Network: Chaos", font=MAIN_FONT, font_size=24, color=CHAOS_COLOR)
        chaos_label.next_to(users, DOWN, buff=0.5)

        self.play(Create(chaos_lines, lag_ratio=0.1), run_time=1.5)
        self.play(FadeIn(chaos_label, shift=UP*0.2))
        
        # Wiggle the lines to show "Shouting/Noise"
        self.play(
            *[line.animate.put_start_and_end_on(
                line.get_start() + np.random.randn(3)*0.05, 
                line.get_end() + np.random.randn(3)*0.05
            ) for line in chaos_lines],
            run_time=0.5,
            rate_func=there_and_back
        )
        self.wait(0.5)

        # --- PART 3: The Solution - SFU ("One Central Spot") ---

        # 1. Clear the mess
        self.play(
            FadeOut(chaos_lines), 
            FadeOut(chaos_label),
            FadeOut(metaphor_text),
            run_time=0.8
        )

        # 2. Introduce the SFU (Central Node)
        sfu_box = RoundedRectangle(corner_radius=0.2, height=1.2, width=1.2, color=SFU_COLOR, stroke_width=6)
        sfu_box.set_fill(color=SFU_COLOR, opacity=0.15)
        sfu_text = Text("SFU", font=MAIN_FONT, weight=BOLD, font_size=24, color=SFU_COLOR).move_to(sfu_box.center())
        sfu_node = VGroup(sfu_box, sfu_text)

        self.play(GrowFromCenter(sfu_node), run_time=0.8)

        # 3. Animate "Sending Video to Central Spot" (Uploads)
        upload_lines = VGroup()
        for user in users:
            # Line from User to SFU
            l = Line(user.get_center(), sfu_node.get_center(), color=CLEAN_COLOR)
            # Dashed to show direction (optional, but solid looks cleaner here)
            l.set_stroke(width=3, opacity=0.5)
            upload_lines.add(l)

        self.play(Create(upload_lines), run_time=1)
        
        # Pulse the SFU to show it receiving data
        self.play(Indicate(sfu_node, color=WHITE, scale_factor=1.1))

        # 4. Animate "Distributing to everyone else" (Downloads)
        # We just flash the existing lines brighter to imply 2-way traffic is now handled efficiently
        self.play(
            upload_lines.animate.set_stroke(width=6, opacity=0.8, color=CLEAN_COLOR),
            run_time=0.8
        )

        # --- PART 4: Bandwidth Savings ---

        # Visual cleanup
        final_text = Text("Huge Bandwidth Saved", font=MAIN_FONT, weight=BOLD, font_size=32, color=CLEAN_COLOR)
        final_text.add_background_rectangle(color=BG_COLOR, buff=0.2, opacity=0.9)
        final_text.move_to(DOWN * 2.5)

        # Show a comparison graphic? No, let's keep it simple as per script.
        # Just emphasize the clean star topology vs the mess we saw earlier.
        
        self.play(Write(final_text), run_time=0.8)
        
        # Subtle "Flow" animation on the clean lines
        self.play(
            ApplyWave(upload_lines, amplitude=0.1),
            run_time=1.5
        )

        self.wait(2)