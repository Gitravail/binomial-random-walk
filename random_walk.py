from array import array
import random


class RandomWalk:

    def __init__(self, inner=10, outer=1000, q=0.5, z=0):
        """
        Initialise the random walk class
        :param inner: number of moves during a repetition
        :param outer: number of repetitions
        :param q: probability trigger (probability the attacker finds the next block)
        :param z: start offset (number of attacker's block behind)
        """
        self._inner = inner
        self._outer = outer
        self._q = q
        self._z = z
        self._values = None
        self._heights = None

    def getValues(self):
        return self._values

    def getHeights(self):
        return self._heights

    def compute(self):
        dict = self._compute_values(self._compute_stopping_points())
        self._values = list(dict.keys())
        self._heights = list(dict.values())
        return dict

    def _compute_values(self, stopping_points: list):
        """
        Generate x-axis values dictionnary with their reached times number
        :param stopping_points: unsorted stopping points result for each outer run
        :return: dictionnary of stop point -> number time reached
        """
        values = {}
        stopping_points.sort()
        for point in stopping_points:
            if point in values:
                values[point] += 1
            else:
                values[point] = 1
        return values

    def _compute_stopping_points(self):
        """
        Compute all the random walks values
        :return: array of every repetition end position
        """
        stopping_points = []
        for i in range(self._outer):
            stopping_points.append(self._compute_k())
        return stopping_points

    def _compute_outer(self):
        """
        Compute all the random walks values
        :return: array of every repetition end position
        """
        fn = []
        for i in range(self._outer):
            fn.append(self._compute_k())
        return fn

    def _compute_k(self):
        """
        Compute a single 1D random walk
        :return: the random walk x coordinate
        """
        k = -self._z
        for i in range(self._inner):
            if random.uniform(0, 1) <= self._q:
                k += 1
            else:
                k -= 1
        return k
