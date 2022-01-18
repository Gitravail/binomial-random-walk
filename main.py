import random
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
import numpy as np
from tkinter import *
import matplotlib
from scipy.interpolate import make_interp_spline

matplotlib.use('TkAgg')


class App(Frame):
    window = Tk()
    fig = Figure(figsize=(10, 6), dpi=300)
    canvas = FigureCanvasTkAgg(fig, master=window)
    toolbar = NavigationToolbar2Tk(canvas, window)
    dimension = IntVar()
    right_frame = Frame(window)
    slider_frame = Frame(right_frame)
    button_frame = Frame(right_frame)
    inner = Scale(slider_frame, from_=10, to=100, orient=HORIZONTAL)
    outer = Scale(slider_frame, from_=1000, to=100000, resolution=1000, orient=HORIZONTAL)
    dimension_check = Checkbutton(button_frame, text="2D", variable=dimension, onvalue=1,
                                  offvalue=0, width=20, height=5)

    def __init__(self):
        super().__init__()

        self.window.title("Binomial random walk")
        self.window.geometry("1280x720")
        self.dimension_check.pack(side=LEFT)
        self.right_frame.pack(side=RIGHT)
        self.slider_frame.pack()
        self.button_frame.pack(side=BOTTOM)

        outer_label = Label(self.slider_frame, text="REPEAT")
        inner_label = Label(self.slider_frame, text="N")
        self.outer.pack(side=RIGHT, padx=5, pady=5)
        outer_label.pack(side=RIGHT)
        self.inner.pack(side=RIGHT)
        inner_label.pack(side=RIGHT)

        compute_button = Button(command=self.draw, master=self.button_frame, height=2, width=10, text="PLOT")
        compute_button.pack(side=RIGHT)

        self.window.mainloop()

    def draw(self):
        inner = self.inner.get()
        outer = self.outer.get()
        heights = compute_result(compute_all(inner, outer), inner)
        x_values, heights = remove_out_zeros(generate_axes_array(inner), heights)
        y_pos = np.arange(len(x_values))

        self.fig.clear()
        self.fig = Figure(figsize=(10, 6), dpi=100)

        plt = self.fig.add_subplot(111)
        plt.set_xticks(y_pos, minor=False)
        plt.set_xticklabels(x_values, fontdict=None, minor=False)
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


def compute_result(random_heights, inner):
    heights = [0] * (inner * 2 + 1)
    for result in random_heights:
        heights[result + inner] += 1
    return heights


def generate_axes_array(inner):
    x_values = []
    for i in range(-inner, inner + 1):
        x_values.append(i)
    return x_values


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


def compute_all(inner, outer):
    fn = []
    for i in range(outer):
        k = 0
        for j in range(inner):
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
