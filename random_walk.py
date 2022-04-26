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
        self._dict = None
        self._values = None
        self._heights = None

    def get_dict(self):
        return self._dict

    def get_values(self):
        return self._values

    def get_heights(self):
        return self._heights

    def get_zero_value_index(self):
        for i in range(len(self._values)):
            if self._values[i] == 0:
                return i
        return None

    def get_zero_height(self):
        i = self.get_zero_value_index()
        if not i == None:
            return self._heights[i]
        return 0

    def compute(self):
        dict = self._compute_values(self._compute_stopping_points())
        self._values = list(dict.keys())
        self._heights = list(dict.values())
        self._dict = dict

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


class RandomWalk2D(RandomWalk):

    def __init__(self, inner=10, outer=1000, q=0.5, z=0):
        super().__init__(inner, outer, q, z)

    def get_x_values(self):
        return [x for x, y in self._values]

    def get_y_values(self):
        return [y for x, y in self._values]

    def compute(self):
        first   = super()._compute_stopping_points()
        second  = super()._compute_stopping_points()
        dict = self._compute_values_2d(first, second)
        self._values = list(dict.keys())
        self._heights = list(dict.values())
        self._dict = dict

    def _compute_values_2d(self, first: list, second: list):
        values = {}
        for i in range(len(first)):
            key = (first[i], second[i])
            if key in values:
                values[key] += 1
            else:
                values[key] = 1
        return values