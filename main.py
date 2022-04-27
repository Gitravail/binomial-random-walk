# Author : Raphael Tournafond

# imports
import math
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.pyplot import fill, text
import numpy as np
from tkinter import *
import matplotlib
from random_walk import RandomWalk, RandomWalk2D
from scipy.interpolate import make_interp_spline

matplotlib.use('TkAgg')


class App(Frame):
    """
    App class that manage the overall app logic
    """
    window = Tk()  # main window
    # plot area
    fig = Figure(figsize=(10, 6), dpi=300)
    canvas = FigureCanvasTkAgg(fig, master=window)
    toolbar = NavigationToolbar2Tk(canvas, window)
    # control panel
    right_frame = Frame(window)
    inner = Scale(right_frame, from_=10, to=100, orient=HORIZONTAL, length=300)
    outer = Scale(right_frame, from_=1000, to=100000, resolution=1000, orient=HORIZONTAL, length=300)
    q = Scale(right_frame, from_=0, to=0.5, resolution=0.01, orient=HORIZONTAL, length=300)
    z = Scale(right_frame, from_=100, to=0, resolution=1, orient=HORIZONTAL, length=300)
    # success probability labels
    title = Label(right_frame, text="Success probability results (only in 1D)")
    validation = Label(right_frame, text="With chain validation")
    theory = Label(right_frame, text="Theory")
    observation = Label(right_frame, text="Obesrvation")
    # current dimension (1D or 2D)
    dimension = IntVar()
    dimension_check = Checkbutton(right_frame, text="2D", variable=dimension, onvalue=1,
                                  offvalue=0, width=20, height=5)

    def __init__(self):
        """
        Init app
        """
        super().__init__()

        # build the window and inner frames
        self.window.title("Binomial random walk")
        self.window.geometry("1280x720")
        self.right_frame.pack(side=RIGHT)

        # build the control panel
        outer_label = Label(self.right_frame, text="REPEAT")
        self.outer.set(100000)
        inner_label = Label(self.right_frame, text="N")
        self.inner.set(100)
        q_label = Label(self.right_frame, text="q")
        self.q.set(0.3)
        z_label = Label(self.right_frame, text="z")
        self.z.set(5)
        compute_button = Button(command=self.draw, master=self.right_frame, height=2, width=10, text="PLOT")

        # Grid
        inner_label.grid(row=0, column=0, sticky=W, pady=2)
        self.inner.grid(row=0, column=1, sticky=W, pady=2)
        outer_label.grid(row=1, column=0, sticky=W, pady=2)
        self.outer.grid(row=1, column=1, sticky=W, pady=2)
        q_label.grid(row=2, column=0, sticky=W, pady=2)
        self.q.grid(row=2, column=1, sticky=W, pady=2)
        z_label.grid(row=3, column=0, sticky=W, pady=2)
        self.z.grid(row=3, column=1, sticky=W, pady=2)
        self.title.grid(row=4, column=0, sticky=EW, pady=2, columnspan=2)
        self.validation.grid(row=5, column=0, sticky=W, pady=2, columnspan=2)
        self.theory.grid(row=6, column=0, sticky=W, pady=2, columnspan=2)
        self.observation.grid(row=7, column=0, sticky=W, pady=2, columnspan=2)
        self.dimension_check.grid(row=8, column=0, sticky=EW, pady=2)
        compute_button.grid(row=9, column=1, sticky=W, pady=2, rowspan=2)

        self.window.mainloop()

    def draw(self):
        """
        Draw window
        :return: plot
        """
        # get sliders values
        inner = self.inner.get()
        outer = self.outer.get()
        q = self.q.get()
        z = self.z.get()

        # reset figure
        self.fig.clear()
        self.fig = Figure(figsize=(10, 6), dpi=100)

        # if 2D
        if self.dimension.get():
            rw = RandomWalk2D(inner, outer, q, z)
            rw.compute()
            self.draw_2d(rw)
            # update success probability labels
            self.validation.config(text="With chain validation")
            self.theory.config(text="Theory")
            self.observation.config(text="Observation")
        # if 1D
        else:
            rw = RandomWalk(inner, outer, q, z)
            rw.compute()
            self.draw_1d(rw)
            # update success probability labels
            self.validation.config(text="With chain validation: " + str(attacker_success_probability(q, z)))
            self.theory.config(text="Theory: " + str((q/(1-q))**z))
            self.observation.config(text="Observation: " + str(rw.get_success()))


        # kill instance
        del rw

        # reset previous plot and redraw
        self.canvas.get_tk_widget().destroy()
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.window)
        self.canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)
        self.canvas.draw()

        # reset toolbar
        self.toolbar.destroy()
        self.toolbar = NavigationToolbar2Tk(self.canvas, self.window)
        self.toolbar.update()

    def draw_1d(self, rw: RandomWalk):
        """
        Draw the 1D plot
        :param rw: RandomWalk Object
        :return: plot
        """
        # draw bars
        values = rw.get_values()
        heights = rw.get_heights()
        plt = self.fig.add_subplot(111)
        y_pos = np.arange(len(values))
        plt.set_xticks(y_pos, minor=False)
        plt.set_xticklabels(values, fontdict=None, minor=False)
        plt.bar(y_pos, heights)
        # add interpolated curve to the plot
        smooth_x, smooth_y = smooth_curve(y_pos, heights)
        plt.plot(smooth_x, smooth_y, color='black')
        # add catch up limit
        i = rw.get_zero_or_above_value_index()
        if not i == None:
            plt.bar(y_pos[i:], heights[i:], color='red')

    def draw_2d(self, rw: RandomWalk2D):
        """
        Draw the 2D plot
        :param rw: RandomWalk2D Object
        :return: plot
        """
        x, y, z = rw.get_matrix()
        # draw wireframe
        plt = self.fig.add_subplot(111, projection='3d')
        z1 = rw.get_below_zero_matrix()
        plt.plot_wireframe(x, y, z1)
        # add catch up limit
        z2 = rw.get_above_zero_matrix()
        z2 = expand_matrix(z2, z)
        plt.plot_wireframe(x, y, z2, color="red")

def smooth_curve(y_pos: list, heights: list):
    """
    Compute the interpolated curve
    :param y_pos: array of graph positions for each height
    :param heights: heights array
    :return: arrays of smoothed y positions and heights
    """
    if len(y_pos) >= 4:
        # define x as 200 equally spaced values between the min and max of original x
        y_pos_smooth = np.linspace(y_pos.min(), y_pos.max(), 200)

        # define spline
        spl = make_interp_spline(y_pos, heights, k=3)
        heights_smooth = spl(y_pos_smooth)
        return y_pos_smooth, heights_smooth
    return y_pos, heights

def expand_matrix(m: np.ndarray, base: np.ndarray):
    """
    Expand matrix values according to a base matrix
    :param m: the matrix to expand
    :param base: the base matrix values are taken from (both should be same size)
    :return: the expanded matrix
    """
    ys = m.shape[0]
    xs = m.shape[1]
    if ys == base.shape[0] and xs == base.shape[1]:
        for i in range(ys):
                for j in range(xs):
                    cell = m.item((i, j))
                    if not math.isnan(cell):
                        # TOP
                        tuple = (i-1,j)
                        if i > 0 and math.isnan(m.item(tuple)) and base.item(tuple) != 0:
                            m.itemset(tuple, base.item(tuple))
                        # RIGHT
                        tuple = (i,j+1)
                        if j < xs-1 and math.isnan(m.item(tuple)) and base.item(tuple) != 0:
                            m.itemset(tuple, base.item(tuple))
                        # BOTTOM
                        tuple = (i+1,j)
                        if i < ys-1 and math.isnan(m.item(tuple)) and base.item(tuple) != 0:
                            m.itemset(tuple, base.item(tuple))
                        # LEFT
                        tuple = (i,j-1)
                        if j > 0 and math.isnan(m.item(tuple)) and base.item(tuple) != 0:
                            m.itemset(tuple, base.item(tuple))
    return m



# Attacker -----------------------------------------------

def attacker_success_probability(q: float, z: int):
    """
    Compute the probability of an attacker to create a longer trusted chain
    :param q: probability the attacker finds the next block
    :param z: number of blocks behind
    :return: probability the attacker will ever catch up from z blocks behind
    """
    p = 1.0 - q
    lam = z * (q / p)
    s = 1.0
    init_poisson = math.exp(-lam)
    for k in range(z + 1):
        poisson = init_poisson  # attacker potential progress at step k
        for i in range(1, k + 1):
            poisson *= lam / i
        s -= poisson * (1 - math.pow(q / p, z - k))
    return s


def main():
    """
    Main function
    :return: app
    """
    App()


if __name__ == '__main__':
    main()
