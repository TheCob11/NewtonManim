from manim import *
f: np.polynomial.Polynomial = np.polynomial.Polynomial.fromroots([-1, 2.5, 7.5]) * 0.1
fp: np.polynomial.Polynomial = f.deriv()
x0: float = 1
class Newton(Scene):
    def construct(self) -> None:
        newton_steps: int = 4

        # value ndarrays
        x_vals = np.empty(newton_steps)
        x_vals[0] = x0
        f_vals = np.empty(newton_steps - 1)
        fp_vals = np.empty(newton_steps - 1)

        step_colors = (RED, ORANGE, YELLOW, GREEN)

        # value displays
        x_val_disp: VGroup = VGroup()
        f_val_disp: VGroup = VGroup()
        fp_val_disp: VGroup = VGroup()
        vals_disp: VGroup = VGroup(x_val_disp, f_val_disp, fp_val_disp)
        # box to display values in
        box: Rectangle = Rectangle().next_to(config.top + config.right_side, LEFT)

        #plot stuff
        plot_axes: Axes = Axes(
            x_range=[-3, 8, 0.5],
            y_range = [-11, 11, 0.5],
            x_length=round(config.frame_width) - 2 - 2,
            tips = False,
        ).next_to(config.left_side, RIGHT)
        plot_curve: ParametricFunction = plot_axes.plot(f)
        #plot goodies displays
        x_point_disp: VGroup = VGroup()
        dashes_disp: VGroup = VGroup()
        f_point_disp: VGroup = VGroup()
        fp_line_disp: VGroup = VGroup()

        for i in range(newton_steps - 1):
            #value ndarray updates
            f_vals[i] = f(x_vals[i])
            fp_vals[i] = fp(x_vals[i])
            x_vals[i+1] = x_vals[i] - f_vals[i]/fp_vals[i]

            #value display updates
            x_val_disp += Variable(x_vals[i], f"x_{i}")\
                .set_color(step_colors[i])\
                .next_to(box if i==0 else fp_val_disp[i-1], DOWN)
            f_val_disp += Variable(f_vals[i], f"f_{i}")\
                .set_color(step_colors[i])\
                .next_to(x_val_disp[i], DOWN)
            fp_val_disp += Variable(fp_vals[i], f"f'_{i}")\
                .set_color(step_colors[i])\
                .next_to(f_val_disp[i], DOWN)

            #plot goodies display updates
            x_point_disp += Dot(plot_axes.coords_to_point(x_vals[i], 0), color=step_colors[i])
            f_point_disp += Dot(plot_axes.coords_to_point(x_vals[i], f_vals[i]), color=step_colors[i])
            dashes_disp += DashedLine(plot_axes.coords_to_point(x_vals[i], 0),
                                      plot_axes.coords_to_point(x_vals[i], f_vals[i]),
                                      color=step_colors[i])
            fp_line_disp += plot_axes.plot(lambda x: fp_vals[i] * (x - x_vals[i]) + f_vals[i], color=step_colors[i])

        #display last x_val(hopefully root)
        x_val_disp += Variable(x_vals[-1], f"x_{newton_steps}")\
            .set_color(step_colors[-1])\
            .next_to(fp_val_disp[-1], DOWN)
        x_point_disp += Dot(plot_axes.coords_to_point(x_vals[-1], 0), color=step_colors[-1])

        #make the box actually do what its supposed to do
        box.surround(vals_disp, stretch=True, buff=SMALL_BUFF)

        #animation playing
        #animate plot
        self.play(Create(plot_axes))
        self.play(Create(plot_curve))
        #animate box
        self.play(Create(box))
        #animate newton steps
        for i in range(newton_steps - 1):
            #show x stuff
            self.play(Create(x_val_disp[i]))
            self.play(Create(x_point_disp[i]))
            self.wait()
            #show f(x) stuff
            self.play(Create(f_val_disp[i]))
            self.play(Create(dashes_disp[i]), Create(f_point_disp[i]))
            self.wait()
            #show f'(x) stuff
            self.play(Create(fp_val_disp[i]))
            self.play(Create(fp_line_disp[i]))
            self.wait()
        #show last x(hopefully root)
        self.play(Create(x_val_disp[-1]))
        self.play(Create(x_point_disp[-1]))
        #bask in glory
        self.wait(3)
      
