import cdf
import random_by_cdf as cdf_rand
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm as norm_distribution
from scipy.stats import gamms as gamma_distribution

def draw_expCDF_by_rand(input_lambda):
    exp_rand = cdf_rand.F_rand_factory(cdf.Exp_factory(input_lambda))
    draw_CDF_by_randCDF(exp_rand, "Exponential CDF, l = " + str(input_lambda))

def draw_gammaCDF_by_rand(a = 0.9):
#    gamma_cdf = lambda x:gamma_distribution.cdf(x,
    pass

def draw_GaussCDF_by_rand(mu = 1.0, sigma = 0.5):
    gauss_cdf = lambda x:norm_distribution.cdf(x, mu, sigma)
    gauss_rand = cdf_rand.F_rand_factory(gauss_cdf)
    draw_CDF_by_randCDF(gauss_rand, "Gauss CDF, mu = " + str(mu) + ", sigma = " + str(sigma))
    
def draw_CDF_by_randCDF(randCDF, plot_title = "Some CDF", figure_title = "CDF"):
    x, y = tabulate_CDF_by_randCDF(randCDF, False)
    # build plots
    plt.plot(x, y, label = plot_title)
    plt.xlabel("x label")
    plt.ylabel("y label")
    plt.title(figure_title)
    plt.legend()
    plt.show()

def tabulate_CDF_by_randCDF(rand_cdf, is_cdf = True, statistic_volume = 100000, x_max = 10, y_max_scale = 10, delta = 0.1):
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

if __name__ == "__main__":
    #draw_expCDF_by_rand(0.5)
    draw_GaussCDF_by_rand(3.0, 1.0)
    print("Finish test Random Value with defined CDF!")

