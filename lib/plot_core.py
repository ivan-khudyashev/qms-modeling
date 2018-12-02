import numpy as np
import matplotlib.pyplot as plt

def tabulate_CDF_by_randCDF(rand_cdf, statistic_volume = 100000, is_cdf, x_max = 20, y_max_scale = 10, delta = 0.1):
    """Tabulate input rand_cdf CDF and build dots (x, y) for plotting inputed CDF
    """
    def found_interval(rand_val, delta, points_count):
        found_border = delta
        found_index = 0
        while found_index < points_count:
            if rand_val < found_border:
                break
            found_border += delta
            found_index += 1
        if found_index >= points_count:
            found_index = points_count - 1
        return found_index

    if statistic_volume < 1:
        return None
    # Initial values for defining plots
    y_scale_koef = float(y_max_scale) / float(statistic_volume)
    points_count = int(x_max / delta)
    x = np.linspace(0, x_max, points_count)
    y= np.zeros(points_count, dtype = float)
    # experiments to get statistic for plots
    for i in range(0, statistic_volume + 1):
        r_val = rand_cdf()
        y[found_interval(r_val, delta, points_count)] += y_scale_koef
    # Accumulate statistic for definint CDF
    #  since CDF(x) = P{X < x}, hence all previous intervals must added to all
    #  next intervals
    if is_cdf:
        for i in range(1, points_count):
            y[i] += y[i - 1]
    return (x, y)

def find_x_max(cdf_func, epsilon = 1e-3, delta_x = 3.0):
    x_max = 0.0
    #TODO: make more intellectual increment
    while cdf_func(x_max) < 1.0 - epsilon:
        x_max += delta_x
    return x_max

def draw_plots(plots, figure_title):
    """Build grafics with all inputed plots
    
    Parameters
    ----------
    plots : list
        List of dictionaries describing one plot
        elem : dict
        {
            x : numpy.array
                Arguments of X-axis
            y : numpy.array
            title : str
                title of plot
        }
    """
    if not isinstance(plots, list):
        #TODO: throw exception
        return None
    for next_plot in plots:
        if not isinstance(next_plot, dict):
            #TODO: throw exception
            return None
        plt.plot(next_plot["x"], next_plot["y"], label = next_plot["title"])
    plt.xlabel("x label")
    plt.ylabel("y label")
    plt.title(figure_title)
    plt.legend()
    plt.show()
