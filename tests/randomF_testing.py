# Local imports
import path_correction
import lib.commons as commons
import lib.plot_module as plot_module
from lib.cdf import CDF_factory as build_cdf
from lib.random_by_cdf import F_rand_factory as gen_rand_f

def gen_exp_cdf(l):
    return build_cdf(commons.CDF_type.EXPONENTIAL, {"lambda_p": l})

def gen_norm_cdf(mu, sigma):
    return build_cdf(commons.CDF_type.GAUSS, {"mu": mu, "sigma": sigma})

def CDF_draw_test(cdf_f, cnt_test, common_title):
    rand_exp = gen_rand_f(cdf_f)
    x_max = plot_module.find_x_max(cdf_f)
    x_cdf, y_cdf = plot_module.tabulate_CDF_by_randCDF(rand_exp, cnt_test, True, x_max, 1.0)
    x_pdf, y_pdf = plot_module.tabulate_CDF_by_randCDF(rand_exp, cnt_test, False, x_max, 1.0)
    plots = [{"x": x_cdf, "y": y_cdf, "title": "CDF"}, {"x": x_pdf, "y": y_pdf, "title": "PDF"}]
    plot_module.draw_plots(plots, common_title)

def test_x_max(cdf_f):
    x_max = plot_module.find_x_max(cdf_f)
    print("x_max = ", x_max)

if __name__ == "__main__":
    l = 0.5
    #test_x_max(gen_exp_cdf(l))
    CDF_draw_test(gen_exp_cdf(l), 100000, "Exponential with l = " + str(l))
    #mu = 1.0
    #sigma = 0.1
    #CDF_draw_test(gen_norm_cdf(mu, sigma), 100000, "Gauss with mu = " + str(mu) + ", sigma = " + str(sigma))
    print("Finish test Random Value with defined CDF!")

