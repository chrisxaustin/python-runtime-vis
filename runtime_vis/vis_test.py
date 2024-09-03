import unittest
from random import randint

import matplotlib.pyplot as plt

from vis import Vis


def insertion_sort(arr: list[int]) -> list[int]:
    for i in range(1, len(arr)):
        for j in range(i, 0, -1):
            if arr[j] < arr[j - 1]:
                arr[j], arr[j - 1] = arr[j - 1], arr[j]
            else:
                break
    return arr


def batch(n: int):
    numbers = [randint(-100, n) for _ in range(n)]
    insertion_sort(numbers)


def observe(size, time, complexity, confidence, results):
    print(f"{size}\t{time:0.2f}\t{complexity}\t{confidence:0.2f}%")
    results.append((size, time, complexity, confidence))


class VisTest(unittest.TestCase):
    def test_something(self):
        results = []
        vis = Vis()
        vis.visualize(
            batch,
            [100, 1000, 2000, 4000],
            performance_callback=lambda size, time, complexity, confidence: observe(size, time, complexity, confidence, results),
            keep_open=False
        )
        plt.close()
        self.assertEqual('n2', results[-1][2])
        self.assertGreater(results[-1][3], 99.5)


if __name__ == '__main__':
    unittest.main()
