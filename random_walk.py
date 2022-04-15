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
        self.inner = inner
        self.outer = outer
        self.q = q
        self.z = z

    def compute_heights(self):
        return self.inner

    def compute_outer(self):
        """
        Compute all the random walks values
        :return: array of every repetition end position
        """
        fn = []
        for i in range(self.outer):
            fn.append(self.compute_k())
        return fn

    def compute_k(self):
        """
        Compute a single 1D random walk
        :return: the random walk x coordinate
        """
        k = -self.z
        for i in range(self.inner):
            if random.uniform(0, 1) <= self.q:
                k += 1
            else:
                k -= 1
        return k
