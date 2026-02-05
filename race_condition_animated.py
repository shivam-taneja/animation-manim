from manim import *

class RaceConditionAnimated(Scene):
    def construct(self):
        # Color palette - vibrant but not neon
        BG_COLOR = "#0f1419"
        PRIMARY = "#3b82f6"      # Vibrant blue
        SECONDARY = "#10b981"    # Vibrant green
        ACCENT = "#ef4444"       # Vibrant red
        WARNING = "#f59e0b"      # Vibrant orange
        PURPLE = "#8b5cf6"       # Vibrant purple
        TEXT_COLOR = "#f3f4f6"
        
        self.camera.background_color = BG_COLOR
        
        # Add subtle animated background - moving grid lines
        bg_lines = VGroup()
        for i in range(-8, 9, 2):
            # Vertical lines
            v_line = Line(
                start=[i, -5, 0],
                end=[i, 5, 0],
                stroke_width=0.5,
                stroke_opacity=0.08,
                color=PRIMARY
            )
            bg_lines.add(v_line)
            # Horizontal lines
            h_line = Line(
                start=[-14, i/2, 0],
                end=[14, i/2, 0],
                stroke_width=0.5,
                stroke_opacity=0.08,
                color=PRIMARY
            )
            bg_lines.add(h_line)
        
        # Add subtle pulsing circles in background
        bg_circles = VGroup()
        for pos in [(4, 2, 0), (-5, -1.5, 0), (3, -2.5, 0), (-4, 1.8, 0)]:
            circle = Circle(radius=1.5, stroke_width=1, stroke_opacity=0.06, color=SECONDARY)
            circle.move_to(pos)
            bg_circles.add(circle)
        
        self.add(bg_lines, bg_circles)
        
        # Add gentle drift to background
        def update_bg(mob, dt):
            mob.shift(RIGHT * 0.008 * dt + DOWN * 0.005 * dt)
            # Reset if moved too far
            if mob.get_center()[0] > 1:
                mob.shift(LEFT * 2)
            if mob.get_center()[1] < -1:
                mob.shift(UP * 2)
        
        bg_lines.add_updater(update_bg)
        
        # Pulsing animation for circles
        def pulse_circles(mob, dt):
            scale_factor = 1 + 0.03 * np.sin(self.renderer.time * 0.8)
            for circle in mob:
                circle.scale(scale_factor / circle.width * 3)  # Normalize scale
        
        bg_circles.add_updater(pulse_circles)
        
        # Animated title with particles
        title = Text("Race Condition Problem", font_size=44, color=TEXT_COLOR, weight=BOLD)
        title.to_edge(UP, buff=0.4)
        
        self.play(
            Write(title, run_time=0.8),
            Flash(title, color=PRIMARY, line_length=0.3, num_lines=20, flash_radius=1.5, run_time=0.8)
        )
        self.wait(0.3)
        
        # --- Scene 1: The Problem with dynamic visuals ---
        
        # Counter with glowing effect
        counter_bg = Circle(radius=0.8, color=PRIMARY, fill_opacity=0.2, stroke_width=3)
        counter_value = Text("3", font_size=52, color=PRIMARY).move_to(counter_bg.get_center())
        counter_label = Text("COUNTER", font_size=20, color=TEXT_COLOR).next_to(counter_bg, UP, buff=0.2)
        counter_group = VGroup(counter_bg, counter_value, counter_label)
        counter_group.move_to(UP * 2.2)
        
        limit_bg = RoundedRectangle(width=2, height=0.6, corner_radius=0.2, color=SECONDARY, fill_opacity=0.2, stroke_width=2)
        limit_text = Text("LIMIT: 5", font_size=22, color=SECONDARY).move_to(limit_bg.get_center())
        limit_group = VGroup(limit_bg, limit_text).next_to(counter_group, DOWN, buff=0.4)
        
        self.play(
            GrowFromCenter(counter_bg),
            FadeIn(counter_value, scale=0.5),
            Write(counter_label),
            run_time=0.7
        )
        self.play(FadeIn(limit_group, shift=UP*0.2), run_time=0.5)
        self.wait(0.2)
        
        # Two requests appear with motion
        req1_bg = RoundedRectangle(width=2.8, height=1.2, corner_radius=0.15, color=PRIMARY, fill_opacity=0.25, stroke_width=4)
        req1_label = Text("Request 1", font_size=26, color=TEXT_COLOR, weight=BOLD)
        req1_icon = Text("→", font_size=36, color=PRIMARY).next_to(req1_label, LEFT, buff=0.2)
        req1_content = VGroup(req1_icon, req1_label).move_to(req1_bg.get_center())
        req1_group = VGroup(req1_bg, req1_content)
        req1_group.move_to(LEFT * 4 + DOWN * 0.8)  # Moved down to avoid overlap
        
        req2_bg = RoundedRectangle(width=2.8, height=1.2, corner_radius=0.15, color=SECONDARY, fill_opacity=0.25, stroke_width=4)
        req2_label = Text("Request 2", font_size=26, color=TEXT_COLOR, weight=BOLD)
        req2_icon = Text("→", font_size=36, color=SECONDARY).next_to(req2_label, LEFT, buff=0.2)
        req2_content = VGroup(req2_icon, req2_label).move_to(req2_bg.get_center())
        req2_group = VGroup(req2_bg, req2_content)
        req2_group.move_to(RIGHT * 4 + DOWN * 0.8)  # Moved down to avoid overlap
        
        # Requests slide in
        self.play(
            req1_group.animate.shift(RIGHT * 0).set_opacity(1),
            FadeIn(req1_group, shift=RIGHT*0.5),
            run_time=0.6
        )
        self.play(
            req2_group.animate.shift(LEFT * 0).set_opacity(1),
            FadeIn(req2_group, shift=LEFT*0.5),
            run_time=0.6
        )
        self.wait(0.2)
        
        # Request 1 starts - show action with particle effect
        action1 = Text("INCREMENT", font_size=20, color=PRIMARY, weight=BOLD)
        action1.next_to(req1_group, DOWN, buff=0.4)  # Increased buffer
        
        self.play(
            Write(action1),
            req1_bg.animate.set_color(WARNING),
            run_time=0.5
        )
        
        # Animate line from request to counter
        line1 = Line(req1_group.get_top(), counter_group.get_bottom(), color=PRIMARY, stroke_width=3)
        self.play(Create(line1), run_time=0.3)
        
        # Counter increments with flash
        new_value_4 = Text("4", font_size=52, color=PRIMARY).move_to(counter_bg.get_center())
        self.play(
            Transform(counter_value, new_value_4),
            Flash(counter_bg, color=PRIMARY, num_lines=12),
            counter_bg.animate.scale(1.15).set_color(WARNING),
            run_time=0.5
        )
        self.play(counter_bg.animate.scale(1/1.15).set_color(PRIMARY), run_time=0.3)
        self.play(FadeOut(line1), run_time=0.2)
        self.wait(0.15)
        
        # THE GAP - dramatic visualization
        gap_box = Rectangle(width=12, height=1.5, color=WARNING, fill_opacity=0.3, stroke_width=0)
        gap_box.move_to(UP * 0.5)  # Adjusted position
        gap_text = Text("THE GAP", font_size=36, color=WARNING, weight=BOLD).move_to(gap_box.get_center())
        
        self.play(
            FadeIn(gap_box, scale=1.2),
            Write(gap_text),
            run_time=0.6
        )
        
        # Danger arrows pointing to gap
        arrow1 = Arrow(LEFT * 2.5 + DOWN * 1, gap_box.get_bottom() + LEFT*1, color=WARNING, stroke_width=5)
        arrow2 = Arrow(RIGHT * 2.5 + DOWN * 1, gap_box.get_bottom() + RIGHT*1, color=WARNING, stroke_width=5)
        self.play(Create(arrow1), Create(arrow2), run_time=0.4)
        self.wait(0.2)
        
        # Request 2 sneaks in during the gap!
        action2 = Text("SNEAK IN!", font_size=20, color=ACCENT, weight=BOLD)
        action2.next_to(req2_group, DOWN, buff=0.4)  # Increased buffer
        
        self.play(
            Write(action2),
            req2_bg.animate.set_color(ACCENT),
            req2_group.animate.shift(UP*0.1),
            run_time=0.5
        )
        self.play(req2_group.animate.shift(DOWN*0.1), run_time=0.2)
        
        # Request 2 also increments
        line2 = Line(req2_group.get_top(), counter_group.get_bottom(), color=SECONDARY, stroke_width=3)
        self.play(Create(line2), run_time=0.3)
        
        new_value_5 = Text("5", font_size=52, color=SECONDARY).move_to(counter_bg.get_center())
        self.play(
            Transform(counter_value, new_value_5),
            Flash(counter_bg, color=SECONDARY, num_lines=12),
            counter_bg.animate.scale(1.15).set_color(ACCENT),
            run_time=0.5
        )
        self.play(counter_bg.animate.scale(1/1.15), run_time=0.3)
        self.play(FadeOut(line2), run_time=0.2)
        self.wait(0.15)
        
        # Request 1 checks (too late!) and increments again
        action1_check = Text("CHECK & GO!", font_size=20, color=ACCENT, weight=BOLD)
        action1_check.move_to(action1.get_center())
        self.play(Transform(action1, action1_check), run_time=0.4)
        
        # Both pass - DISASTER
        new_value_6 = Text("6", font_size=52, color=ACCENT).move_to(counter_bg.get_center())
        self.play(
            Transform(counter_value, new_value_6),
            counter_bg.animate.set_color(ACCENT),
            Flash(counter_bg, color=ACCENT, num_lines=20, line_length=0.6),
            run_time=0.6
        )
        
        # Explosion of error
        error_text = Text("LIMIT BROKEN!", font_size=38, color=ACCENT, weight=BOLD)
        error_text.move_to(DOWN * 2.5)
        
        cross1 = Line(error_text.get_corner(UL), error_text.get_corner(DR), color=ACCENT, stroke_width=6)
        cross2 = Line(error_text.get_corner(UR), error_text.get_corner(DL), color=ACCENT, stroke_width=6)
        
        self.play(
            Write(error_text),
            Create(cross1),
            Create(cross2),
            Flash(error_text, color=ACCENT, num_lines=16, line_length=0.8),
            run_time=0.8
        )
        self.wait(0.6)
        
        # Dramatic clear with wipe effect
        self.play(
            *[FadeOut(mob, shift=DOWN*0.5) for mob in self.mobjects],
            run_time=0.9
        )
        self.wait(0.4)
        
        # --- Scene 2: The Solution with dramatic visuals ---
        
        solution_title = Text("Atomic Operation Solution", font_size=44, color=SECONDARY, weight=BOLD)
        solution_title.to_edge(UP, buff=0.4)
        
        self.play(
            Write(solution_title),
            Flash(solution_title, color=SECONDARY, num_lines=20, flash_radius=1.5),
            run_time=0.9
        )
        self.wait(0.3)
        
        # Counter setup
        counter_bg2 = Circle(radius=0.8, color=PRIMARY, fill_opacity=0.2, stroke_width=3)
        counter_value2 = Text("4", font_size=52, color=PRIMARY).move_to(counter_bg2.get_center())
        counter_label2 = Text("COUNTER", font_size=20, color=TEXT_COLOR).next_to(counter_bg2, UP, buff=0.2)
        counter_group2 = VGroup(counter_bg2, counter_value2, counter_label2)
        counter_group2.move_to(UP * 2.5)
        
        limit_bg2 = RoundedRectangle(width=2, height=0.6, corner_radius=0.2, color=SECONDARY, fill_opacity=0.2, stroke_width=2)
        limit_text2 = Text("LIMIT: 5", font_size=22, color=SECONDARY).move_to(limit_bg2.get_center())
        limit_group2 = VGroup(limit_bg2, limit_text2).next_to(counter_group2, DOWN, buff=0.4)
        
        self.play(
            GrowFromCenter(counter_bg2),
            FadeIn(counter_value2, scale=0.5),
            Write(counter_label2),
            FadeIn(limit_group2, shift=UP*0.2),
            run_time=0.8
        )
        self.wait(0.2)
        
        # Powerful atomic block with shield aesthetic
        atomic_outer = RoundedRectangle(width=7, height=4, corner_radius=0.25, color=SECONDARY, fill_opacity=0.1, stroke_width=5)
        atomic_outer.move_to(DOWN * 0.5)
        
        # Lua script label with icon
        lua_icon = Text("*", font_size=40, color=SECONDARY, weight=BOLD)
        lua_label = Text("LUA SCRIPT", font_size=28, color=SECONDARY, weight=BOLD)
        atomic_badge = Text("ATOMIC", font_size=20, color=WARNING, weight=BOLD)
        lua_title = VGroup(lua_icon, lua_label, atomic_badge).arrange(RIGHT, buff=0.2)
        lua_title.next_to(atomic_outer, UP, buff=0.3)
        
        self.play(
            Create(atomic_outer),
            FadeIn(lua_title, shift=UP*0.2),
            Flash(atomic_outer, color=SECONDARY, num_lines=16),
            run_time=0.9
        )
        self.wait(0.2)
        
        # Three unified steps with connecting lines
        step_boxes = VGroup()
        step_labels = ["1. INCREMENT", "2. CHECK LIMIT", "3. ROLLBACK"]
        colors = [PRIMARY, WARNING, SECONDARY]
        
        for i, (label, color) in enumerate(zip(step_labels, colors)):
            box = RoundedRectangle(width=5, height=0.7, corner_radius=0.1, color=color, fill_opacity=0.25, stroke_width=3)
            text = Text(label, font_size=22, color=TEXT_COLOR, weight=BOLD).move_to(box.get_center())
            group = VGroup(box, text)
            step_boxes.add(group)
        
        step_boxes.arrange(DOWN, buff=0.25).move_to(atomic_outer.get_center())
        
        # Connecting lines between steps
        connections = VGroup()
        for i in range(len(step_boxes) - 1):
            line = Line(
                step_boxes[i].get_bottom(),
                step_boxes[i+1].get_top(),
                color=SECONDARY,
                stroke_width=3
            )
            connections.add(line)
        
        # Animate all steps appearing together
        self.play(
            LaggedStart(
                *[FadeIn(step, shift=RIGHT*0.3) for step in step_boxes],
                lag_ratio=0.15
            ),
            run_time=1.0
        )
        self.play(Create(connections), run_time=0.5)
        self.wait(0.3)
        
        # "No gaps" with shield
        shield = Circle(radius=0.5, color=SECONDARY, fill_opacity=0.3, stroke_width=5)
        shield.next_to(atomic_outer, DOWN, buff=0.5)
        shield_check = Text("OK", font_size=32, color=SECONDARY, weight=BOLD).move_to(shield.get_center())
        no_gaps = Text("NO GAPS | NO RACE", font_size=28, color=SECONDARY, weight=BOLD)
        no_gaps.next_to(shield, RIGHT, buff=0.4)
        
        self.play(
            GrowFromCenter(shield),
            Write(shield_check),
            Write(no_gaps),
            Flash(shield, color=SECONDARY, num_lines=12),
            run_time=0.8
        )
        self.wait(0.3)
        
        # Execute the atomic operation with sequential highlights
        # Step 1: Increment
        self.play(
            step_boxes[0].animate.scale(1.1),
            step_boxes[0][0].animate.set_fill(opacity=0.5),
            Flash(step_boxes[0], color=PRIMARY, num_lines=8),
            run_time=0.5
        )
        new_value2_5 = Text("5", font_size=52, color=PRIMARY).move_to(counter_bg2.get_center())
        self.play(
            Transform(counter_value2, new_value2_5),
            Flash(counter_bg2, color=PRIMARY, num_lines=10),
            run_time=0.5
        )
        self.play(step_boxes[0].animate.scale(1/1.1), step_boxes[0][0].animate.set_fill(opacity=0.25), run_time=0.3)
        self.wait(0.2)
        
        # Step 2: Check
        self.play(
            step_boxes[1].animate.scale(1.1),
            step_boxes[1][0].animate.set_fill(opacity=0.5),
            Flash(step_boxes[1], color=WARNING, num_lines=8),
            counter_bg2.animate.set_color(WARNING),
            run_time=0.5
        )
        self.play(step_boxes[1].animate.scale(1/1.1), step_boxes[1][0].animate.set_fill(opacity=0.25), run_time=0.3)
        self.wait(0.2)
        
        # Step 3: Rollback!
        self.play(
            step_boxes[2].animate.scale(1.1),
            step_boxes[2][0].animate.set_fill(opacity=0.5),
            Flash(step_boxes[2], color=SECONDARY, num_lines=8),
            run_time=0.5
        )
        new_value2_4 = Text("4", font_size=52, color=SECONDARY).move_to(counter_bg2.get_center())
        self.play(
            Transform(counter_value2, new_value2_4),
            counter_bg2.animate.set_color(SECONDARY),
            Flash(counter_bg2, color=SECONDARY, num_lines=16, line_length=0.5),
            run_time=0.7
        )
        self.play(step_boxes[2].animate.scale(1/1.1), step_boxes[2][0].animate.set_fill(opacity=0.25), run_time=0.3)
        self.wait(0.3)
        
        # Victory message
        victory = Text("STATE PROTECTED!", font_size=36, color=SECONDARY, weight=BOLD)
        victory.move_to(DOWN * 3.2)
        
        self.play(
            Write(victory),
            Flash(victory, color=SECONDARY, num_lines=20, flash_radius=1.2),
            run_time=0.8
        )
        self.wait(0.8)
        
        # Fade out with style
        self.play(
            *[FadeOut(mob, shift=UP*0.3, scale=0.9) for mob in self.mobjects],
            run_time=1.0
        )
        self.wait(0.3)