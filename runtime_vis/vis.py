import cProfile
import pstats
import warnings
from typing import Callable, Any, Iterable, List

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import scipy.optimize as opt
import seaborn as sns

from runtime_vis.curves import fit_n, fit_logn, fit_nlogn, fit_n2, named_curves


class Vis:
    def __init__(self, fit: List[str] = None):
        self.times = []

        self.curves = named_curves.values()

    def profile_batch(self, function: Callable[[int], Any], size: int, dataset: pd.DataFrame) -> float:
        p = cProfile.Profile()
        p.enable()
        function(size)
        p.create_stats()
        stats = pstats.Stats(p)
        time = 0
        for stat in stats.stats.items():
            if stat[1][3] > time:
                time = stat[1][3]
        p.disable()

        dataset.loc[len(dataset)] = [size, time]
        self.render_plot(dataset)
        self.times.append((size, time))

        return time

    def render_plot(self, dataset: pd.DataFrame):
        plt.clf()
        sns.scatterplot(x='N', y='Time', data=dataset)
        plt.draw()
        plt.pause(0.1)

    def fit_curve(self, dataset: pd.DataFrame) -> (str, float):
        if len(dataset['N']) < 2:
            return None, 0.0

        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            x_data = np.array(dataset['N'])
            y_data = np.array(dataset['Time'])
            best_label = "unknown"
            best_fit = None
            candidates = []

            for curve in self.curves:
                popt, _ = opt.curve_fit(curve.callable, x_data, y_data, p0=curve.initial_guess)
                # plt.plot(x_data, curve.callable(x_data, *popt), label=f'{popt[0]:.9f} * {curve.name}', color=curve.color)
                # calculate how close it fits
                predicted = curve.callable(x_data[-1], *popt)
                fit_quality = abs(predicted / y_data[-1])
                confidence = 100 - abs(100 - 100 * fit_quality)
                candidates.append((curve, popt, confidence))
                if best_fit is None or confidence > best_fit:
                    best_fit = confidence
                    best_label = curve.name
            candidates = sorted(candidates, key=lambda x: x[2], reverse=True)
            for candidate in candidates[0:3]:
                curve = candidate[0]
                popt = candidate[1]
                plt.plot(x_data, curve.callable(x_data, *popt), label=f'{curve.name:5} : {candidate[2]:.2f}%', color=curve.color)
            plt.legend()
            plt.draw()
            plt.pause(0.1)
            return best_label, best_fit

    def visualize(
        self,
        function: Callable[[int], Any],
        series: Iterable[int],
        performance_callback: Callable[[int, float, str, float], Any] = None,
        keep_open: bool = True
    ) -> List[tuple[int, int]]:
        """
        Visualizes the performance of the provided function.
        :param function: a function that takes a N parameter
        :param series: the values of N to pass to the function
        :param performance_callback: a function that will accept an integer size, float time, string complexity, float fit %
        """
        dataset = pd.DataFrame(columns=['N', 'Time'])
        plt.figure()
        plt.ion()
        plt.show()
        plt.xlabel('N')
        plt.ylabel('Time (ms)')
        for size in series:
            time = self.profile_batch(function, size, dataset)
            complexity, accuracy = self.fit_curve(dataset)
            if performance_callback:
                performance_callback(size, time, complexity, accuracy)

        if keep_open:
            plt.ioff()
            plt.show()
