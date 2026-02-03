from manim import *

# --- Global Styles ---
MAIN_FONT = "Inter" # Ensure this font is installed, or change to "Arial" or "Sans-Serif"

# --- Modern Vibrant Color Palette ---
BG_COLOR = "#0F172A"       
BROWSER_COLOR = "#3B82F6"  
SERVER_COLOR = "#F97316"   
P2P_COLOR = "#2DD4BF"      
TEXT_COLOR = "#FFFFFF"     
ACCENT_RED = "#EF4444"     

class WebRTCExplainerVibrant(Scene):
    def construct(self):
        self.camera.background_color = BG_COLOR

        # --- PART 1: The Hook ---
        
        # Title Text
        title = Text("WebRTC", font_size=80, font=MAIN_FONT, weight=BOLD, color=P2P_COLOR)
        # Fix: Use set_stroke method instead of init argument
        title.set_stroke(color=P2P_COLOR, width=1, opacity=0.5)
        
        subtitle = Text("The backbone of it all.", font_size=32, font=MAIN_FONT, color=TEXT_COLOR)
        subtitle.next_to(title, DOWN, buff=0.5)

        self.play(Write(title), run_time=0.8)
        self.play(FadeIn(subtitle, shift=UP * 0.3), run_time=0.8)
        self.wait(0.5)

        # Move title up
        header_group = VGroup(title, subtitle)
        self.play(
            header_group.animate.scale(0.6).to_edge(UP, buff=0.5),
            run_time=1
        )

        # --- PART 2: The Browsers ---

        browser_a = self.create_styled_browser("Browser A").to_edge(LEFT, buff=2)
        browser_b = self.create_styled_browser("Browser B").to_edge(RIGHT, buff=2)

        self.play(
            GrowFromCenter(browser_a),
            GrowFromCenter(browser_b),
            run_time=0.8
        )

        # --- PART 3: The Problem (Server) ---

        server = self.create_styled_server("Middleman Server").move_to(UP * 0.2)
        
        # FIX: Define DashedLine without opacity first, then set it
        path_a_to_s = DashedLine(browser_a.get_top(), server.get_left(), color=SERVER_COLOR)
        path_a_to_s.set_opacity(0.6)
        
        path_s_to_b = DashedLine(server.get_right(), browser_b.get_top(), color=SERVER_COLOR)
        path_s_to_b.set_opacity(0.6)

        self.play(FadeIn(server, shift=DOWN * 0.5), run_time=0.7)
        self.play(
            Create(path_a_to_s),
            Create(path_s_to_b),
            run_time=1
        )
        self.wait(0.3)
        
        # REJECT the server
        cross = Cross(server, stroke_color=ACCENT_RED, stroke_width=8)
        no_text = Text("NO Middleman!", font=MAIN_FONT, weight=BOLD, color=ACCENT_RED, font_size=28).next_to(server, DOWN)
        
        # Fix: Add background rectangle safely
        no_text.add_background_rectangle(color=BG_COLOR, buff=0.1)
        # Access the background rectangle directly to change opacity if needed
        no_text.background_rectangle.set_fill(opacity=0.8)

        self.play(
            Create(cross),
            Write(no_text),
            FadeOut(path_a_to_s), FadeOut(path_s_to_b),
            browser_a.animate.set_opacity(0.5),
            browser_b.animate.set_opacity(0.5),
            run_time=0.7
        )

        # --- PART 4: The Solution (P2P) ---

        self.play(
            FadeOut(server), FadeOut(cross), FadeOut(no_text),
            browser_a.animate.set_opacity(1),
            browser_b.animate.set_opacity(1),
            run_time=0.5
        )

        # Fix: Create line without opacity in init
        p2p_line = Line(
            browser_a.get_right(), 
            browser_b.get_left(), 
            color=P2P_COLOR, 
            stroke_width=10
        )
        
        # Fix: Apply glow manually
        glow_copy = p2p_line.copy()
        glow_copy.set_stroke(width=20, opacity=0.3)
        p2p_line.add_to_back(glow_copy)

        p2p_label = Text("P2P Direct WebRTC", font=MAIN_FONT, weight=BOLD, font_size=28, color=P2P_COLOR).next_to(p2p_line, UP)

        self.play(
            GrowFromCenter(p2p_line, point_color=P2P_COLOR), 
            run_time=1
        )
        self.play(FadeIn(p2p_label, shift=DOWN*0.2))
        
        # Pulse effect
        self.play(
            ApplyWave(p2p_line, amplitude=0.2, run_time=1),
            Indicate(p2p_label, color=WHITE, scale_factor=1.1)
        )
        
        self.wait(2)


    # --- HELPER FUNCTIONS ---
    
    def create_styled_browser(self, label_text):
        # Fix: Moved fill_opacity to set_fill()
        icon = RoundedRectangle(
            corner_radius=0.3, height=1.8, width=2.5, 
            color=BROWSER_COLOR, 
            stroke_width=4
        )
        icon.set_fill(color=BROWSER_COLOR, opacity=0.2)
        
        # Glow effect
        glow = icon.copy()
        glow.set_stroke(width=8, opacity=0.3)
        
        label = Text(label_text, font=MAIN_FONT, weight=BOLD, font_size=24, color=TEXT_COLOR).next_to(icon, DOWN)
        return VGroup(glow, icon, label)

    def create_styled_server(self, label_text):
        # Fix: Moved fill_opacity to set_fill()
        r1 = Rectangle(height=0.4, width=1.5, color=SERVER_COLOR, stroke_width=3)
        r1.set_fill(color=SERVER_COLOR, opacity=0.3)
        
        r2 = r1.copy().next_to(r1, UP, buff=0.05)
        r3 = r1.copy().next_to(r2, UP, buff=0.05)
        
        lights = VGroup()
        for rack in [r1, r2, r3]:
            # Fix: Moved fill_opacity to set_fill()
            l = Circle(radius=0.05, color=SERVER_COLOR)
            l.set_fill(color=SERVER_COLOR, opacity=1)
            l.move_to(rack.get_right() + LEFT*0.2)
            lights.add(l)

        rack_group = VGroup(r1, r2, r3, lights)
        label = Text(label_text, font=MAIN_FONT, font_size=20, color=SERVER_COLOR).next_to(rack_group, UP)
        return VGroup(rack_group, label)