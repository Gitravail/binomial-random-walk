import random
import matplotlib.pyplot as plt
import numpy as np

INNER_ITERATION = 100
MAX_ITERATION = 100000


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


def remove_out_zeros(values, heights):
    while len(heights) and heights[0] == 0:
        values.pop(0)
        heights.pop(0)

    while len(heights) and heights[len(heights)-1] == 0:
        values.pop()
        heights.pop()


def display_result(heights):
    xvalues = generate_axes_array(heights)
    remove_out_zeros(xvalues, heights)
    y_pos = np.arange(len(xvalues))
    plt.xticks(y_pos, xvalues, rotation=90, fontsize=5)
    plt.bar(y_pos, heights)
    plt.show()


def main():
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
    display_result(compute_result(fn))


if __name__ == '__main__':
    main()
