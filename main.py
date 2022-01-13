import random
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
import numpy as np
from tkinter import *
import matplotlib
from scipy.interpolate import make_interp_spline, BSpline

matplotlib.use('TkAgg')

INNER_ITERATION = 10
MAX_ITERATION = 10000


class App:
    window = Tk()
    fig = Figure(figsize=(10, 6), dpi=300)
    canvas = FigureCanvasTkAgg(fig, master=window)
    toolbar = NavigationToolbar2Tk(canvas, window)

    def __init__(self):
        self.window.title("Binomial random walk")
        self.window.geometry("1280x720")
        compute_button = Button(command=self.draw, master=self.window, height=2, width=10, text="Plot")
        compute_button.pack()
        self.window.mainloop()

    def draw(self):
        heights = compute_result(compute_all())
        xvalues, heights = remove_out_zeros(generate_axes_array(), heights)
        y_pos = np.arange(len(xvalues))

        self.fig.clear()
        self.fig = Figure(figsize=(10, 6), dpi=100)

        plt = self.fig.add_subplot(111)
        plt.set_xticks(y_pos, minor=False)
        plt.set_xticklabels(xvalues, fontdict=None, minor=False)
        plt.bar(y_pos, heights)
        smooth_x, smooth_y = smooth_curve(y_pos, heights)
        plt.plot(smooth_x, smooth_y, color='red')

        self.canvas.get_tk_widget().destroy()
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.window)
        self.canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)
        self.canvas.draw()

        self.toolbar.destroy()
        self.toolbar = NavigationToolbar2Tk(self.canvas, self.window)
        self.toolbar.update()


def smooth_curve(y_pos, heights):
    # define x as 200 equally spaced values between the min and max of original x
    y_pos_smooth = np.linspace(y_pos.min(), y_pos.max(), 200)

    # define spline
    spl = make_interp_spline(y_pos, heights, k=3)
    heights_smooth = spl(y_pos_smooth)

    return y_pos_smooth, heights_smooth


def compute_result(random_heights):
    heights = [0] * (INNER_ITERATION * 2 + 1)
    for result in random_heights:
        heights[result + INNER_ITERATION] += 1
    return heights


def generate_axes_array():
    xvalues = []
    for i in range(-INNER_ITERATION, INNER_ITERATION + 1):
        xvalues.append(i)
    return xvalues


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


def compute_all():
    fn = []
    for i in range(MAX_ITERATION):
        k = 0
        for j in range(INNER_ITERATION):
            if random.getrandbits(1):
                k += 1
            else:
                k -= 1
            j += 1
        fn.append(k)
    return fn


def main():
    App()


if __name__ == '__main__':
    main()
