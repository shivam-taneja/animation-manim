from manim import *

# --- Global Styles ---
MAIN_FONT = "Inter"

# --- Palette ---
BG_COLOR = "#0F172A"
NODE_COLOR = "#38BDF8"
SEC_COLOR = "#FBBF24"
DB_COLOR = "#F471B5"
SUCCESS_COLOR = "#34D399"
FAIL_COLOR = "#F87171"
TEXT_COLOR = "#F8FAFC"
GRAY_COLOR = "#64748B"

class SagaStory(Scene):
    def construct(self):
        self.camera.background_color = BG_COLOR

        # --- Status Bar Helper ---
        status_line = Text("", font=MAIN_FONT, font_size=22, color=TEXT_COLOR)
        status_line.to_edge(DOWN, buff=0.4)
        self.add(status_line)

        # --- INTRO: Title ---
        title = Text("Saga Choreography", font=MAIN_FONT, weight=BOLD, font_size=48, color=NODE_COLOR)
        subtitle = Text("Decentralized Transaction Management", font=MAIN_FONT, font_size=20, color=GRAY_COLOR)
        subtitle.next_to(title, DOWN)
        
        self.play(FadeIn(title, shift=UP*0.3), run_time=0.5)
        self.play(FadeIn(subtitle), run_time=0.4)
        self.wait(0.3)
        self.play(
            FadeOut(subtitle),
            title.animate.scale(0.5).to_corner(UL, buff=0.3),
            run_time=0.5
        )

        # --- SETUP: Services Architecture ---
        # Booking Service (Left)
        booking_box = RoundedRectangle(height=1.8, width=2.8, corner_radius=0.15, color=NODE_COLOR, stroke_width=3, fill_opacity=0.1)
        booking_lbl = Text("Booking\nService", font=MAIN_FONT, font_size=18, color=NODE_COLOR).move_to(booking_box)
        booking_icon = Text("📅", font_size=28).next_to(booking_lbl, UP, buff=0.15)
        booking_svc = VGroup(booking_box, booking_lbl, booking_icon).shift(LEFT * 3.5 + UP * 0.3)

        # Discount Service (Right)
        discount_box = RoundedRectangle(height=1.8, width=2.8, corner_radius=0.15, color=SEC_COLOR, stroke_width=3, fill_opacity=0.1)
        discount_lbl = Text("Discount\nService", font=MAIN_FONT, font_size=18, color=SEC_COLOR).move_to(discount_box)
        discount_icon = Text("%", font_size=32).next_to(discount_lbl, UP, buff=0.15)
        discount_svc = VGroup(discount_box, discount_lbl, discount_icon).shift(RIGHT * 3.5 + UP * 0.3)

        self.play(
            FadeIn(booking_svc, shift=RIGHT*0.5),
            FadeIn(discount_svc, shift=LEFT*0.5),
            run_time=0.6
        )

        # "No Global Transaction" label
        no_global = Text("No Global Transaction ⚠️", font=MAIN_FONT, font_size=16, color=FAIL_COLOR, slant=ITALIC)
        no_global.move_to(UP * 2)
        self.play(FadeIn(no_global, shift=DOWN*0.2), run_time=0.5)
        self.wait(0.3)

        # --- REDIS: The Quota Tracker ---
        # Redis visualization
        redis_outline = VGroup(
            Ellipse(width=1.3, height=0.45, color=DB_COLOR, stroke_width=3),
            Line(LEFT*0.65, LEFT*0.65 + DOWN*0.9, color=DB_COLOR, stroke_width=3),
            Line(RIGHT*0.65, RIGHT*0.65 + DOWN*0.9, color=DB_COLOR, stroke_width=3),
            Arc(radius=0.65, start_angle=PI, angle=PI, color=DB_COLOR, stroke_width=3).stretch(0.35, 1).shift(DOWN*0.9)
        ).shift(DOWN * 2.2)
        
        redis_lbl = Text("Redis", font=MAIN_FONT, font_size=16, color=DB_COLOR, weight=BOLD).next_to(redis_outline, LEFT, buff=0.3)
        redis_quota_lbl = Text("Quota:", font=MAIN_FONT, font_size=14, color=GRAY_COLOR).move_to(redis_outline).shift(UP*0.15)
        redis_val = Text("1", font=MAIN_FONT, font_size=36, color=SUCCESS_COLOR, weight=BOLD).move_to(redis_outline).shift(DOWN*0.2)
        redis_grp = VGroup(redis_outline, redis_lbl, redis_quota_lbl, redis_val)
        
        self.play(FadeIn(redis_grp, shift=UP*0.3), run_time=0.6)
        self.wait(0.3)

        # --- THE RACE: Two Users ---
        # User A (Success - Green theme)
        user_a_circle = Circle(radius=0.35, color=SUCCESS_COLOR, fill_opacity=0.2, stroke_width=3)
        user_a_txt = Text("A", font_size=20, color=SUCCESS_COLOR, weight=BOLD)
        user_a = VGroup(user_a_circle, user_a_txt).move_to(LEFT * 3.5 + UP * 2.5)

        # User B (Will fail - Red theme)
        user_b_circle = Circle(radius=0.35, color=FAIL_COLOR, fill_opacity=0.2, stroke_width=3)
        user_b_txt = Text("B", font_size=20, color=FAIL_COLOR, weight=BOLD)
        user_b = VGroup(user_b_circle, user_b_txt).move_to(RIGHT * 3.5 + UP * 2.5)
        
        self.play(
            FadeIn(user_a, scale=0.5),
            FadeIn(user_b, scale=0.5),
            run_time=0.5
        )
        self.play(FadeOut(no_global), run_time=0.3)

        # --- STEP 1: Both hit Booking Service ---
        arrow_a_to_booking = Arrow(user_a.get_bottom(), booking_box.get_top() + LEFT*0.3, color=SUCCESS_COLOR, buff=0.1, stroke_width=4)
        arrow_b_to_booking = Arrow(user_b.get_bottom(), booking_box.get_top() + RIGHT*0.3, color=FAIL_COLOR, buff=0.1, stroke_width=4)
        
        self.play(
            GrowArrow(arrow_a_to_booking),
            GrowArrow(arrow_b_to_booking),
            run_time=0.5
        )

        # Booking accepts both locally (pending state)
        self.play(
            FadeOut(booking_icon),
            FadeOut(booking_lbl),
            run_time=0.3
        )
        
        pending_a = Text("A: Pending", font=MAIN_FONT, font_size=16, color=SUCCESS_COLOR).move_to(booking_box).shift(UP*0.3)
        pending_b = Text("B: Pending", font=MAIN_FONT, font_size=16, color=FAIL_COLOR).move_to(booking_box).shift(DOWN*0.3)
        
        self.play(
            FadeIn(pending_a, shift=DOWN*0.2),
            FadeIn(pending_b, shift=DOWN*0.2),
            run_time=0.4
        )
        self.wait(0.2)

        # --- STEP 2: Event Emission (Choreography!) ---
        event_arrow = CurvedArrow(
            booking_box.get_right() + UP*0.3,
            discount_box.get_left() + UP*0.3,
            angle=-TAU/5,
            color=TEXT_COLOR,
            stroke_width=3
        )
        event_lbl = Text("OrderCreated", font=MAIN_FONT, font_size=15, color=TEXT_COLOR, slant=ITALIC)
        event_lbl.next_to(event_arrow, UP, buff=0.1)
        
        self.play(Create(event_arrow), Write(event_lbl), run_time=0.6)
        self.play(FadeOut(arrow_a_to_booking), FadeOut(arrow_b_to_booking), run_time=0.3)

        # --- STEP 3: THE CRITICAL MOMENT - Redis Check ---

        # Both services try to claim
        check_a = DashedLine(discount_box.get_bottom() + LEFT*0.5, redis_grp.get_top() + LEFT*0.3, color=SUCCESS_COLOR, stroke_width=3)
        check_b = DashedLine(discount_box.get_bottom() + RIGHT*0.5, redis_grp.get_top() + RIGHT*0.3, color=FAIL_COLOR, stroke_width=3)
        
        self.play(Create(check_a), Create(check_b), run_time=0.5)
        
        # User A wins the race!
        self.play(
            Indicate(redis_val, color=SUCCESS_COLOR, scale_factor=1.3),
            check_a.animate.set_stroke(width=5),
            run_time=0.5
        )
        
        # Redis goes to 0
        redis_zero = Text("0", font=MAIN_FONT, font_size=36, color=FAIL_COLOR, weight=BOLD).move_to(redis_val)
        self.play(Transform(redis_val, redis_zero), run_time=0.4)
        self.wait(0.2)

        # User B fails
        self.play(
            Flash(redis_val, color=FAIL_COLOR, flash_radius=0.5),
            check_b.animate.set_stroke(width=5),
            run_time=0.5
        )
        
        x_mark = Text("❌", font_size=40, color=FAIL_COLOR).next_to(discount_box, RIGHT, buff=0.3)
        self.play(FadeIn(x_mark, scale=0.3), run_time=0.4)
        self.wait(0.3)
        
        self.play(FadeOut(check_a), FadeOut(check_b), FadeOut(x_mark), run_time=0.3)

        # --- STEP 4: THE SAGA - Rollback/Compensation ---

        # Failure event back to Booking
        rollback_arrow = CurvedArrow(
            discount_box.get_left() + DOWN*0.3,
            booking_box.get_right() + DOWN*0.3,
            angle=-TAU/5,
            color=FAIL_COLOR,
            stroke_width=4
        )
        rollback_lbl = Text("DiscountFailed", font=MAIN_FONT, font_size=15, color=FAIL_COLOR, weight=BOLD, slant=ITALIC)
        rollback_lbl.next_to(rollback_arrow, DOWN, buff=0.1)
        
        self.play(Create(rollback_arrow), Write(rollback_lbl), run_time=0.6)

        # Booking compensates (rolls back User B)
        
        cross_b = Line(pending_b.get_corner(UL), pending_b.get_corner(DR), color=FAIL_COLOR, stroke_width=4)
        cross_b2 = Line(pending_b.get_corner(UR), pending_b.get_corner(DL), color=FAIL_COLOR, stroke_width=4)
        
        self.play(
            Create(cross_b),
            Create(cross_b2),
            run_time=0.4
        )
        
        cancelled = Text("CANCELLED", font=MAIN_FONT, font_size=13, color=FAIL_COLOR, weight=BOLD)
        cancelled.move_to(pending_b)
        self.play(FadeOut(pending_b), FadeIn(cancelled), run_time=0.3)

        # User A confirmed
        
        check_mark = Text("✓", font_size=24, color=SUCCESS_COLOR, weight=BOLD).next_to(pending_a, RIGHT, buff=0.2)
        confirmed = Text("CONFIRMED", font=MAIN_FONT, font_size=13, color=SUCCESS_COLOR, weight=BOLD)
        confirmed.next_to(pending_a, DOWN, buff=0.2)
        
        self.play(
            FadeIn(check_mark, scale=0.5),
            FadeIn(confirmed, shift=UP*0.1),
            run_time=0.5
        )
        self.wait(0.4)

        # --- FINALE: Key Insight ---
        self.play(
            FadeOut(event_arrow), FadeOut(event_lbl),
            FadeOut(rollback_arrow), FadeOut(rollback_lbl),
            FadeOut(redis_grp),
            FadeOut(user_a), FadeOut(user_b),
            run_time=0.5
        )

        # Highlight the key services with their outcomes
        a_box = SurroundingRectangle(VGroup(pending_a, check_mark, confirmed), color=SUCCESS_COLOR, buff=0.15, corner_radius=0.1)
        b_box = SurroundingRectangle(VGroup(cancelled, cross_b, cross_b2), color=FAIL_COLOR, buff=0.15, corner_radius=0.1)
        
        self.play(Create(a_box), Create(b_box), run_time=0.5)
        self.wait(0.3)

        final_msg = VGroup(
            Text("Saga: Each service handles its own rollback", font=MAIN_FONT, font_size=24, color=TEXT_COLOR),
            Text("No central coordinator needed", font=MAIN_FONT, font_size=20, color=GRAY_COLOR)
        ).arrange(DOWN, buff=0.2)
        final_msg.to_edge(DOWN, buff=0.5)
        
        self.play(Transform(status_line, final_msg), run_time=0.5)
        self.wait(1.5)