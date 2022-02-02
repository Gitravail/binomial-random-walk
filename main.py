# Author : Raphael Tournafond

# imports
import random
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
import numpy as np
from tkinter import *
import matplotlib
from scipy.interpolate import make_interp_spline

matplotlib.use('TkAgg')


# App class that manage the overall app logic
class App(Frame):
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
    # current dimension (1D or 2D)
    dimension = IntVar()
    dimension_check = Checkbutton(button_frame, text="2D", variable=dimension, onvalue=1,
                                  offvalue=0, width=20, height=5)

    def __init__(self):
        super().__init__()

        # build the window and inner frames
        self.window.title("Binomial random walk")
        self.window.geometry("1280x720")
        self.dimension_check.pack(side=LEFT)
        self.right_frame.pack(side=RIGHT)
        self.slider_frame.pack()
        self.button_frame.pack(side=BOTTOM)

        # build the control panel
        outer_label = Label(self.slider_frame, text="REPEAT")
        inner_label = Label(self.slider_frame, text="N")
        self.outer.pack(side=RIGHT, padx=5, pady=5)
        outer_label.pack(side=RIGHT)
        self.inner.pack(side=RIGHT)
        inner_label.pack(side=RIGHT)
        compute_button = Button(command=self.draw, master=self.button_frame, height=2, width=10, text="PLOT")
        compute_button.pack(side=RIGHT)

        self.window.mainloop()

    # method started when clicking the plot button
    def draw(self):
        # get sliders values
        inner = self.inner.get()
        outer = self.outer.get()

        # reset figure
        self.fig.clear()
        self.fig = Figure(figsize=(10, 6), dpi=100)

        # if 2D
        if self.dimension.get():
            x, y = compute_x_y_values_2d(inner, outer)
            d = compute_d_2d(x, y)
            mx, my, mz = compute_matrix_2d(x, y, d)
            self.draw_2d(mx, my, mz)
        # if 1D
        else:
            heights = compute_result(compute_all(inner, outer), inner)
            x_values, heights = remove_out_zeros(generate_axes_array(inner), heights)
            y_pos = np.arange(len(x_values))
            self.draw_1d(y_pos, x_values, heights)

        # reset previous plot and redraw
        self.canvas.get_tk_widget().destroy()
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.window)
        self.canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)
        self.canvas.draw()

        # reset toolbar
        self.toolbar.destroy()
        self.toolbar = NavigationToolbar2Tk(self.canvas, self.window)
        self.toolbar.update()

    # draw the 1D plot
    def draw_1d(self, y_pos, x_values, heights):
        # draw bars
        plt = self.fig.add_subplot(111)
        plt.set_xticks(y_pos, minor=False)
        plt.set_xticklabels(x_values, fontdict=None, minor=False)
        plt.bar(y_pos, heights)
        # add interpolated curve to the plot
        smooth_x, smooth_y = smooth_curve(y_pos, heights)
        plt.plot(smooth_x, smooth_y, color='red')

    # draw the 2D plot
    def draw_2d(self, x, y, z):
        # draw wireframe
        plt = self.fig.add_subplot(111, projection='3d')
        plt.plot_wireframe(x, y, z)


# 1 dimension

# compute the interpolated curve
def smooth_curve(y_pos, heights):
    # define x as 200 equally spaced values between the min and max of original x
    y_pos_smooth = np.linspace(y_pos.min(), y_pos.max(), 200)

    # define spline
    spl = make_interp_spline(y_pos, heights, k=3)
    heights_smooth = spl(y_pos_smooth)

    return y_pos_smooth, heights_smooth


# put the heights result according to the sorted coordinates
def compute_result(random_heights, inner):
    heights = [0] * (inner * 2 + 1)
    for result in random_heights:
        heights[result + inner] += 1
    return heights


# generate x axis array
def generate_axes_array(inner):
    x_values = []
    for i in range(-inner, inner + 1):
        x_values.append(i)
    return x_values


# clean out never reached values
def remove_out_zeros(values_with_zeros, heights_with_zeros):
    heights = []
    values = []
    i = 0
    for height in heights_with_zeros:
        if height != 0:
            values.append(values_with_zeros[i])
            heights.append(height)
        i += 1
    return values, heights


# compute all the random walks values
def compute_all(inner, outer):
    fn = []
    for i in range(outer):
        fn.append(compute_k(inner))
    return fn


# compute a single 1D random walk
def compute_k(inner):
    k = 0
    for i in range(inner):
        if random.getrandbits(1):
            k += 1
        else:
            k -= 1
    return k


# 2 dimensions

# compute all 2D random walks
def compute_x_y_values_2d(inner, outer):
    x = []
    y = []
    for i in range(outer):
        # compute two random walks that will be superposed to generate a 2D walk
        x.append(compute_k(inner))
        y.append(compute_k(inner))
    return x, y


# compute a dictionary that will store the number of times a specific coordinate is reached at the end of a walk
def compute_d_2d(x, y):
    d = {}
    for i in range(len(x)):
        key = (x[i], y[i])
        if key in d:
            d[key] += 1
        else:
            d[key] = 1
    return d


# compute the x, y, z matrices
def compute_matrix_2d(x, y, d):
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


def main():
    App()


if __name__ == '__main__':
    main()
