import random
import matplotlib.pyplot as plt
import numpy as np

INNER_ITERATION = 9
MAX_ITERATION = 100000


def compute_result(non_computed_result):
    computed_result = [0] * (INNER_ITERATION * 2 + 1)
    for current in non_computed_result:
        computed_result[current + INNER_ITERATION] += 1
    return computed_result


def generate_axes_array():
    result = []
    for i in range(-INNER_ITERATION, INNER_ITERATION + 1):
        result.append(i)
    return result


def display_result(computed_result):
    possible_values = generate_axes_array()
    results = computed_result
    y_pos = np.arange(len(possible_values))
    plt.xticks(y_pos, possible_values)
    plt.bar(y_pos, results)
    plt.show()


def main():
    result = []
    for i in range(MAX_ITERATION):
        k = 0
        for j in range(INNER_ITERATION):
            if random.getrandbits(1):
                k += 1
            else:
                k -= 1
            j += 1
        result.append(k)
    display_result(compute_result(result))


if __name__ == '__main__':
    main()
