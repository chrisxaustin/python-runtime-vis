import cProfile
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import pstats
import scipy.optimize as opt
import seaborn as sns
from typing import Callable, Any


def profile_batch(function: Callable[[int], Any], name: str, size: int, dataset: pd.DataFrame):
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


def render_plot(dataset: pd.DataFrame):
    plt.clf()
    sns.scatterplot(x='N', y='Time', data=dataset)
    plt.draw()
    plt.pause(0.1)


def curve_n(x, a, b):
    return a * x + b


def curve_logn(x, a, b):
    return a * np.log(x) + b


def curve_nlogn(x, a, b):
    return a * x * np.log(x) + b


def curve_n2(x, a, b):
    return a * x ** 2 + b


initial_guess_n = [1e-7, 1]  # Adjust these as needed
initial_guess_logn = [1e-7, 1]  # Adjust these as needed
initial_guess_nlogn = [1e-7, 1]  # Adjust these as needed
initial_guess_n2 = [1e-10, 1]  # Adjust these as needed


def fit_curve(dataset: pd.DataFrame):
    if len(dataset['N']) < 2:
        return

    x_data = np.array(dataset['N'])
    y_data = np.array(dataset['Time'])
    popt_n, _ = opt.curve_fit(curve_n, x_data, y_data, p0=initial_guess_n)
    popt_logn, _ = opt.curve_fit(curve_logn, x_data, y_data, p0=initial_guess_logn)
    popt_nlogn, _ = opt.curve_fit(curve_nlogn, x_data, y_data, p0=initial_guess_nlogn)
    popt_n2, _ = opt.curve_fit(curve_n2, x_data, y_data, p0=initial_guess_n2)
    plt.plot(x_data, curve_n(x_data, *popt_n), label=f'{popt_n[0]:.9f} * n', color='green')
    plt.plot(x_data, curve_logn(x_data, *popt_logn), label=f'{popt_logn[0]:.9f} * log n', color='blue')
    plt.plot(x_data, curve_nlogn(x_data, *popt_nlogn), label=f'{popt_nlogn[0]:.9f} * n log n', color='yellow')
    plt.plot(x_data, curve_n2(x_data, *popt_n2), label=f'{popt_n2[0]:.9f} * n^2', color='orange')
    print("Coefficients for n log n fit:", popt_nlogn)
    print("Coefficients for n^2 fit:", popt_n2)
    plt.legend()

    plt.draw()
    plt.pause(0.1)


def visualize(function: Callable[[int], Any], name: str, series: list(int)):
    dataset = pd.DataFrame(columns=['N', 'Time'])
    plt.figure()
    plt.ion()
    plt.show()
    plt.xlabel('N')
    plt.ylabel('Time (ms)')
    for size in [1000, 2000, 4000, 8000, 16000, 32000, 64000]:
        profile_batch(function, name, size, dataset)
        fit_curve(dataset)
    plt.ioff()
    plt.show()
