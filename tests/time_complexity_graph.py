import os
import sys
import copy

current_script_path = os.path.dirname(os.path.abspath(__file__))
root_directory = os.path.abspath(os.path.join(current_script_path, ".."))  # Go up one level
sys.path.append(root_directory)

from manim import *
from manim.utils.utils import add_func2plane, draw_point_in_function


class BarChartDFS_BFS(Scene):
    def construct(self):
        values = [0.109, 0.110, 0.162, 0.535, 1.490, 11.298, 110.229, 334.997, 1963.761, 8875.124, 11895.126]
        bar_chart_dfs = BarChart( 
            values=values,
            bar_names=["(10V, 20A)", "(50V, 100A)", "(100V, 200A)", "(250V, 500A)", 
                       "(500V, 750A)", "(1.25kV, 2.5kA)", "(3.5kV, 7kA)", 
                       "(6.25kV, 12.5kA)", "(15kV, 30kA)","(31.25kV, 62.5kA)", "(50kV, 62.5kA)"],
            y_range=[0, 12000, 1000], 
            x_length=12, 
            y_length=6, 
            axis_config={'numbers_to_exclude': [0, 2]}, 
            x_axis_config={'color': '#F7f7f7', "font_size": 16}, 
            y_axis_config={'color': '#F7f7f7', "font_size": 24},
            tips = True 
        ) 
        label_axis_y = bar_chart_dfs.get_y_axis_label(label=Text('Tiempo de ejecucion (s)', font='White Chalk'))
        label_axis_y.scale(0.35)
        label_axis_y.next_to(bar_chart_dfs,  1.25 * LEFT + 0.75 * UP)
        label_axis_x = bar_chart_dfs.get_x_axis_label(label=Text('Numero de vertices (n) + Numero de aristas (m)', font='White Chalk'))
        label_axis_x.scale(0.35)
        label_axis_x.next_to(bar_chart_dfs, DOWN)
        c_bar_lbls = bar_chart_dfs.get_bar_labels(font_size=20)
        bars = bar_chart_dfs.bars
        self.add(bar_chart_dfs, label_axis_x, label_axis_y, c_bar_lbls, bars)
        self.play(DrawBorderThenFill(bar_chart_dfs, run_time = 5))
        self.wait(2)

                # Create plane
        plane = add_plane(x_range = [0, 130000, 10000], y_range = [0, 12000, 1000], 
                          y_length=6, x_length=12, faded_line_ratio=0, 
                          background_line_style={"stroke_color": '#F7f7f7',"stroke_width": 1,"stroke_opacity": 0})
        
        # Add plane function
        value_tracker = ValueTracker(0)
        eq = lambda n: 0.1078 * n -484.8186
        func_obj, func_lab = add_func2plane(plane, eq, "f(n) = 0.1009{n} -520.4959", value_tracker)
        func_lab.move_to(2*UP)

        # Convert points_coordinates to points on the plane
        points_coordinates = [
            [30, 0.109, 0],
            [150, 0.110, 0],
            [300, 0.162, 0],
            [750, 0.535, 0],
            [1250, 1.490, 0],
            [3750, 11.298, 0],
            [10500, 110.229, 0],
            [18750, 334.997, 0],
            [45000, 1963.761, 0],
            [93750, 8875.124, 0],
            [112500, 11895.126, 0]
        ]
        labels = ["(10V, 20A)", "(50V, 100A)", "(100V, 200A)", 
                  "(250V, 500A)", "(500V, 750A)", "(1.25kV, 2.5kA)", 
                  "(3.5kV, 7kA)", "(6.25kV, 12.5kA)", "(15kV, 30kA)",
                  "(31.25kV, 62.5kA)", "(50kV, 62.5kA)"]
        points_on_plane = [plane.c2p(coordinates[0], coordinates[1]) for coordinates in points_coordinates]

        points = [LabeledDot(point=pt, radius=0.1, color=RED, label=Text(lb, font='White Chalk', font_size=12, color='#F7f7f7')) for pt, lb in zip(points_on_plane, labels)]

        # Animate
        bars_copy = bars.copy()
        self.play(Transform(bar_chart_dfs, plane))
        self.play(AnimationGroup(*[FadeIn(point) for point in points], 
                  *[label.animate.next_to(pt, UP, buff=0.25) for label, pt in zip(c_bar_lbls, points)], 
                  *[bar.animate.set_x(pt.get_x()) for bar, pt in zip(bars, points)],
                  *[bar.animate.set_x(pt.get_x()) for bar, pt in zip(bars_copy, points)]))
        self.add(func_obj)
        self.play(Write(func_lab), value_tracker.animate.set_value(115000), run_time=5 , rate_func=linear)
        self.wait(2)



if __name__ == "__main__":
    config.pixel_height = 1080  # Set the pixel height of the output video 2160
    config.pixel_width = 1920  # Set the pixel width of the output video 3840
    config.media_dir = "F:\\TheRabbitHole\\VlogDeUnNerd\\animations-code\\video-11"
    scene = BarChartDFS_BFS()
    scene.render(preview=True)