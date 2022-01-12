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


def display_result(heights):
    xvalues, heights = remove_out_zeros(generate_axes_array(heights), heights)
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
