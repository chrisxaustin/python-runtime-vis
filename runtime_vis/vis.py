import cProfile
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import pstats
import scipy.optimize as opt
import seaborn as sns
import warnings
from typing import Callable, Any, Iterable

from runtime_vis.curves import curve_n, curve_logn, curve_nlogn


class Vis:
    def __init__(self):
        self.initial_guess = {
            'n': [1e-7, 1],
            'logn': [1e-7, 1],
            'nlogn': [1e-7, 1],
            'n2': [1e-10, 1],
        }
        self.curves = [
            curve_n,
            curve_logn,
            curve_nlogn,
            curve_n2,
        ]

    def profile_batch(self, function: Callable[[int], Any], name: str, size: int, dataset: pd.DataFrame):
        p = cProfile.Profile()
        p.enable()
        function(size)
        p.create_stats()
        stats = pstats.Stats(p)
        for stat in stats.stats.items():
            if stat[0][2] == name:
                time = stat[1][3]
                row = {'N': size, 'Time': time}
                dataset.loc[len(dataset)] = [size, time]
                render_plot(dataset)
                break
        p.disable()
        print(f"{size}\t{time:4.2f}")

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
                popt, _ = opt.curve_fit(curve.callable, x_data, y_data, p0=initial_guess)
                plt.plot(x_data, curve.callable(x_data, *popt_n), label=f'{popt[0]:.9f} * {curve.name}', color=curve.color)
            # print("Coefficients for n log n fit:", popt_nlogn)
            # print("Coefficients for n^2 fit:", popt_n2)
            plt.legend()
            plt.draw()
            plt.pause(0.1)

    def visualize(
        self,
        function: Callable[[int], Any],
        name: str,
        series: Iterable[int]
    ):
        dataset = pd.DataFrame(columns=['N', 'Time'])
        plt.figure()
        plt.ion()
        plt.show()
        plt.xlabel('N')
        plt.ylabel('Time (ms)')
        for size in series:
            self.profile_batch(function, name, size, dataset)
            self.fit_curve(dataset)
        plt.ioff()
        plt.show()
