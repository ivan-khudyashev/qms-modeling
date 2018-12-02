import numpy as np
import matplotlib.pyplot as plt
import random_by_cdf as cdf_rand
import commons
from cdf import CDF_factory

def 

def draw_expCDF_by_rand(input_lambda):
    exp_rand = cdf_rand.F_rand_factory(cdf.Exp_factory(input_lambda))
    draw_CDF_by_randCDF(exp_rand, "Exponential CDF, l = " + str(input_lambda))

def draw_gammaCDF_by_rand(a = 0.9, loc = 0.0, scale = 1.0):
    """PDF (Probability Density Function) for gamma-distribution defined as
    PDF(x) = x^(a - 1) * e^(-x/thetta) / ( Г(a) * thetta^a )
    There is more common case with shift
    PDF(x) = (x - shift)^(a - 1) * e^(-(x - shift)/thetta) / ( Г(a) * thetta^a )
    In scipy.stats.gamma this parameters define as:
    a := a
    loc := shift
    scale := thetta
    CDF has according parameters
    """
    gamma_cdf = lambda x:gamma_distribution.cdf(x, a, loc, scale)
    gamma_rand = cdf_rand.F_rand_factory(gamma_cdf)
    draw_PDF_by_randCDF(gamma_rand, "Gamma CDF, a = " + str(a) + ",thetta = " + str(scale))

def draw_GaussCDF_by_rand(mu = 1.0, sigma = 0.5):
    gauss_cdf = lambda x:norm_distribution.cdf(x, mu, sigma)
    gauss_rand = cdf_rand.F_rand_factory(gauss_cdf)
    draw_CDF_by_randCDF(gauss_rand, "Gauss CDF, mu = " + str(mu) + ", sigma = " + str(sigma))
    
def draw_CDF_by_randCDF(randCDF, plot_title = "Some CDF", figure_title = "CDF"):
    x, y = tabulate_CDF_by_randCDF(randCDF)
    # build plots
    plt.plot(x, y, label = plot_title)
    plt.xlabel("x label")
    plt.ylabel("y label")
    plt.title(figure_title)
    plt.legend()
    plt.show()

def draw_PDF_by_randCDF(randCDF, plot_title = "Some CDF", figure_title = "CDF"):
    x, y = tabulate_CDF_by_randCDF(randCDF, False)
    plt.plot(x, y, label = plot_title)
    plt.xlabel("x label")
    plt.ylabel("y label")
    plt.title(figure_title)
    plt.legend()
    plt.show()

def tabulate_CDF_by_randCDF(rand_cdf, statistic_volume = 100000, is_cdf = True, x_max = 20, y_max_scale = 10, delta = 0.1):
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

if __name__ == "__main__":
    #draw_expCDF_by_rand(0.5)
    #draw_GaussCDF_by_rand(3.0, 1.0)
    draw_gammaCDF_by_rand(9.0, 0.0, 0.5)
    print("Finish test Random Value with defined CDF!")

