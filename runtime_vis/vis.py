import cProfile
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import pstats
import scipy.optimize as opt
import seaborn as sns
import warnings
from typing import Callable, Any, Iterable, List

from runtime_vis.curves import fit_n, fit_logn, fit_nlogn, fit_n2, fit_n3, named_curves


class Vis:
    def __init__(self, fit: List[str] = None):
        self.times = []

        if fit:
            self.curves = []
            for name in fit:
                if name in named_curves:
                    self.curves.append(named_curves[name])
        else:
            self.curves = [
                fit_n,
                fit_logn,
                fit_nlogn,
                fit_n2,
            ]


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
        self.times.append((size,time))

        return time

    def render_plot(self, dataset: pd.DataFrame):
        plt.clf()
        sns.scatterplot(x='N', y='Time', data=dataset)
        plt.draw()
        plt.pause(0.1)

    def fit_curve(self, dataset: pd.DataFrame):
        if len(dataset['N']) < 2:
            return

        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            x_data = np.array(dataset['N'])
            y_data = np.array(dataset['Time'])
            for curve in self.curves:
                popt, _ = opt.curve_fit(curve.callable, x_data, y_data, p0=curve.initial_guess)
                plt.plot(x_data, curve.callable(x_data, *popt), label=f'{popt[0]:.9f} * {curve.name}', color=curve.color)
                # print("Coefficients for n log n fit:", popt)
                # print("Coefficients for n^2 fit:", popt)
            plt.legend()
            plt.draw()
            plt.pause(0.1)

    def visualize(
        self,
        function: Callable[[int], Any],
        series: Iterable[int],
        performance_callback: Callable[[int,float], Any] = None
    ) -> List[tuple[int,int]]:
        """
        Visualizes the performance of the provided function.
        :param function: a function that takes a N parameter
        :param series: the values of N to pass to the function
        :param performance_callback: a function that will accept an integer size and a float time
        """
        dataset = pd.DataFrame(columns=['N', 'Time'])
        plt.figure()
        plt.ion()
        plt.show()
        plt.xlabel('N')
        plt.ylabel('Time (ms)')
        for size in series:
            time = self.profile_batch(function, size, dataset)
            if performance_callback:
                performance_callback(size, time)
            self.fit_curve(dataset)
        plt.ioff()
        plt.show()
