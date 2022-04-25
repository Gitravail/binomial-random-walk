# Author : Raphael Tournafond

# imports
import math
import random
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
import numpy as np
from tkinter import *
import matplotlib
from random_walk import RandomWalk
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
    slider_frame = Frame(right_frame)
    button_frame = Frame(right_frame)
    inner = Scale(slider_frame, from_=10, to=100, orient=HORIZONTAL)
    outer = Scale(slider_frame, from_=1000, to=100000, resolution=1000, orient=HORIZONTAL)
    attacker_frame = Frame(right_frame)
    q = Scale(attacker_frame, from_=0.00, to=1, resolution=0.02, orient=HORIZONTAL)
    z = Scale(attacker_frame, from_=10, to=0, orient=HORIZONTAL)
    # current dimension (1D or 2D)
    dimension = IntVar()
    dimension_check = Checkbutton(button_frame, text="2D", variable=dimension, onvalue=1,
                                  offvalue=0, width=20, height=5)

    def __init__(self):
        """
        Init app
        """
        super().__init__()

        # build the window and inner frames
        self.window.title("Binomial random walk")
        self.window.geometry("1280x720")
        self.dimension_check.pack(side=LEFT)
        self.right_frame.pack(side=RIGHT)
        self.slider_frame.pack()
        self.attacker_frame.pack()
        self.button_frame.pack(side=BOTTOM)

        # build the control panel
        outer_label = Label(self.slider_frame, text="REPEAT")
        inner_label = Label(self.slider_frame, text="N")
        self.outer.pack(side=RIGHT, padx=5, pady=5)
        outer_label.pack(side=RIGHT)
        self.inner.pack(side=RIGHT)
        inner_label.pack(side=RIGHT)
        q_label = Label(self.attacker_frame, text="q")
        self.q.set(0.5)
        z_label = Label(self.attacker_frame, text="             z")
        self.z.set(0)
        self.z.pack(side=RIGHT)
        z_label.pack(side=RIGHT)
        self.q.pack(side=RIGHT)
        q_label.pack(side=RIGHT)
        compute_button = Button(command=self.draw, master=self.button_frame, height=2, width=10, text="PLOT")
        compute_button.pack(side=RIGHT)

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
            x, y = compute_x_y_values_2d(inner, outer, q, z)
            d = compute_d_2d(x, y)
            mx, my, mz = compute_matrix_2d(x, y, d)
            self.draw_2d(mx, my, mz)
        # if 1D
        else:
            # heights = compute_result(compute_all(inner, outer, q, z), inner)
            # x_values, heights = remove_out_zeros(generate_axes_array(inner), heights)
            # self.draw_1d(x_values, heights)
            rw = RandomWalk(inner, outer, q, z)
            rw.compute()
            self.draw_1d(rw.getValues(), rw.getHeights())

        # reset previous plot and redraw
        self.canvas.get_tk_widget().destroy()
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.window)
        self.canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)
        self.canvas.draw()

        # reset toolbar
        self.toolbar.destroy()
        self.toolbar = NavigationToolbar2Tk(self.canvas, self.window)
        self.toolbar.update()

    def draw_1d(self, x_values, heights):
        """
        Draw the 1D plot
        :param x_values: array of position number
        :param heights: array of the height on each position
        :return: plot
        """
        # draw bars
        plt = self.fig.add_subplot(111)
        y_pos = np.arange(len(x_values))
        plt.set_xticks(y_pos, minor=False)
        plt.set_xticklabels(x_values, fontdict=None, minor=False)
        plt.bar(y_pos, heights)
        # add interpolated curve to the plot
        # smooth_x, smooth_y = smooth_curve(y_pos, heights)
        # plt.plot(smooth_x, smooth_y, color='red')

    def draw_2d(self, x, y, z):
        """
        Draw the 2D plot
        :param x: x coordinate array
        :param y: y coordinate array
        :param z: array of heights on coordinate (x, y)
        :return: plot
        """
        # draw wireframe
        plt = self.fig.add_subplot(111, projection='3d')
        plt.plot_wireframe(x, y, z)


# 1 dimension ----------------------------------------------

def smooth_curve(y_pos, heights):
    """
    Compute the interpolated curve
    :param y_pos: array of graph positions for each height
    :param heights: heights array
    :return: arrays of smoothed y positions and heights
    """
    # define x as 200 equally spaced values between the min and max of original x
    y_pos_smooth = np.linspace(y_pos.min(), y_pos.max(), 200)

    # define spline
    spl = make_interp_spline(y_pos, heights, k=3)
    heights_smooth = spl(y_pos_smooth)

    return y_pos_smooth, heights_smooth


def compute_result(random_heights, inner):
    """
    Put the heights result according to the sorted coordinates
    :param random_heights: unsorted heights result for each outer run
    :param inner: number of inner repetitions
    :return: summed heights in sorted array
    """
    heights = [0] * (inner * 2 + 1)
    for result in random_heights:
        heights[result + inner] += 1
    return heights


def generate_axes_array(inner):
    """
    Generate x-axis array
    :param inner: number of inner loop moves
    :return: array of x values
    """
    x_values = []
    for i in range(-inner, inner + 1):
        x_values.append(i)
    return x_values


def remove_out_zeros(values_with_zeros, heights_with_zeros):
    """
    Clean out never reached values
    :param values_with_zeros: values before remove the one never reached
    :param heights_with_zeros: heights containing never reached values (height = 0 === never reached)
    :return: cleaned array of x values and heights >= 0
    """
    heights = []
    values = []
    i = 0
    for height in heights_with_zeros:
        if height != 0:  # if value reached
            values.append(values_with_zeros[i])
            heights.append(height)
        i += 1
    return values, heights


def compute_all(inner, outer, q, z):
    """
    Compute all the random walks values
    :param inner: number of moves during a repetition
    :param outer: number of repetitions
    :param q: probability trigger (probability the attacker finds the next block)
    :param z: start offset (number of attacker's block behind)
    :return: array of every repetition end position
    """
    fn = []
    for i in range(outer):
        fn.append(compute_k(inner, q, z))
    return fn


def compute_k(inner, q, z):
    """
    Compute a single 1D random walk
    :param inner: number of inner tries
    :param q: probability trigger (probability the attacker finds the next block)
    :param z: start offset (number of attacker's block behind)
    :return: end result after inner tries from start
    """
    k = -z
    for i in range(inner):
        if random.uniform(0, 1) <= q:
            k += 1
        else:
            k -= 1
    return k


# 2 dimensions

def compute_x_y_values_2d(inner, outer, q, z):
    """
    Compute all 2D random walks
    :param inner: number of moves during a repetition
    :param outer: number of repetitions
    :param q: probability trigger (probability the attacker finds the next block)
    :param z: start offset (number of attacker's block behind)
    :return: "2D" array of every repetition end position
    """
    x = []
    y = []
    for i in range(outer):
        # compute two random walks that will be superposed to generate a 2D walk
        x.append(compute_k(inner, q, z))
        y.append(compute_k(inner, q, z))
    return x, y


def compute_d_2d(x, y):
    """
    Compute a dictionary that will store the number of times a specific coordinate is reached at the end of a walk
    :param x: x-axis positions
    :param y: y-axis positions
    :return: dictionary associating (x, y) --> height (number of time reached)
    """
    d = {}
    for i in range(len(x)):
        key = (x[i], y[i])
        if key in d:
            d[key] += 1
        else:
            d[key] = 1
    return d


def compute_matrix_2d(x, y, d):
    """
    Compute the x, y, z matrices
    :param x: raw x-axis unsorted positions
    :param y: raw y-axis unsorted positions
    :param d: unsorted dictionary
    :return: ordered and sorted x, y and z matrices (see examples)
    """
    # clean lists
    # example : x = [1, -2, 3]; y = [-6, 4]
    x = sorted(list(set(x)))
    y = sorted(list(set(y)))

    # create x matrix
    # [[1, -2, 3], [1, -2, 3]]
    mx = []
    for i in range(len(y)):
        mx.append(x)
    mx = np.matrix(mx)

    # create y matrix
    # [[-6, -6, -6], [4, 4, 4]]
    my = []
    for i in range(len(y)):
        my.append([y[i]] * len(x))
    my = np.matrix(my)

    # create z matrix
    # get matrix size
    ys = mx.shape[0]
    xs = mx.shape[1]
    # fill a matrix with zeros (not reached)
    mz = np.zeros((ys, xs))
    for i in range(ys):
        for j in range(xs):
            mxi = mx.item((i, j))
            myi = my.item((i, j))
            # if coordinate has been reached
            if (mxi, myi) in d:
                # add it to the matrix
                mz.itemset((i, j), d.get((mxi, myi)))
    return mx, my, mz


# Attacker -----------------------------------------------

def attacker_success_probability(q, z):
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
