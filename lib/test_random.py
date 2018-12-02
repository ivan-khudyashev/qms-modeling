import commons
import plot_core
from cdf import CDF_factory as build_cdf
from random_by_cdf import F_rand_factory as gen_rand_f

def expCDF_draw_test(cnt_test, l):
    rand_exp = gen_rand_f(build_cdf(commons.CDF_type.EXPONENTIAL, {"lambda_p": l}))
    x_cdf, y_cdf = plot_core.tabulate_CDF_by_randCDF(rand_exp, cnt_test)
    x_pdf, y_pdf = plot_core.tabulate_CDF_by_randCDF(rand_exp, cnt_test, False)
    plots = [{"x": x_cdf, "y": y_cdf, "title": "CDF"}, {"x": x_pdf, "y": y_pdf, "title": "PDF"}]
    plot_core.draw_plots(plots, "Exponential Distr with l = " + str(l))

if __name__ == "__main__":
    #draw_expCDF_by_rand(0.5)
    #draw_GaussCDF_by_rand(3.0, 1.0)
    draw_gammaCDF_by_rand(9.0, 0.0, 0.5)
    print("Finish test Random Value with defined CDF!")

