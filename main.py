import random
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
import numpy as np
from tkinter import *

INNER_ITERATION = 10
MAX_ITERATION = 10000

window = Tk()


def compute_result(random_heights):
    heights = [0] * (INNER_ITERATION * 2 + 1)
    for result in random_heights:
        heights[result + INNER_ITERATION] += 1
    return heights


def generate_axes_array(heights):
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


def init_window():
    window.title("Binomial random walk")
    window.geometry("1280x720")
    compute_button = Button(command=get_figure, master=window, height=2, width=10, text="Plot")
    compute_button.pack()
    window.mainloop()


def get_figure():
    heights = compute_result(compute_all())
    xvalues, heights = remove_out_zeros(generate_axes_array(heights), heights)
    y_pos = np.arange(len(xvalues))
    fig = Figure(figsize=(10, 6), dpi=100)
    plt = fig.add_subplot(111)
    plt.set_xticks(y_pos, minor=False)
    plt.set_xticklabels(xvalues, fontdict=None, minor=False)
    plt.bar(y_pos, heights)
    plt.plot(y_pos, heights, color='red')
    canvas = FigureCanvasTkAgg(fig, master=window)
    canvas.draw()
    canvas.get_tk_widget().pack()
    toolbar = NavigationToolbar2Tk(canvas, window)
    toolbar.update()
    canvas.get_tk_widget().pack()


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
    init_window()


if __name__ == '__main__':
    main()
