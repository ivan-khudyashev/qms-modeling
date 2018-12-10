import numpy as np
#Local imports
import path_correction
from lib.io_module import load_gi_gi_inf_params as gigiinf_load
from lib.qms_gi_gi_inf import experiment_series_qms as exp_series
import lib.plot_module as plot_module
import lib.commons as commons

"""
def qms_experiment_type1():
    #T = [1, 5, 10, 25, 50]
    T = [0.1, 1.0, 3.0, 5.0]
    gamma = [1.0, 0.5, 0.25]
    input_lambda = 0.8
    input_flow_F = Exponential_Flow_Factory(input_lambda)
    T_len = len(T)
    # define Gauss CDF with _params_{mu, sigma}
    mu = 0.0
    sigma = 1.0
    gauss_cdf = lambda x: norm_distribution.cdf(x, mu, sigma)
    cnt = 10
    for next_gamma in gamma:
        print("gamma = ", next_gamma)
        cur_i = 0
        res = []
        B = B_rand_factory(B_factory(next_gamma))
        for nextT in T:
            cur_i = cur_i + 1
            print(cur_i, " from ", T_len)
            res.append(experiment_series_qms(cnt, nextT, input_flow_F, B, gass_cdf))
        print("----------")
        print("T = ", T)
        print(res)
        print("----------")
"""

def gi_gi_inf_plottest():
    gi_gi_inf_params = gigiinf_load()
    input_flow = gi_gi_inf_params["input_flow"]
    service_func = gi_gi_inf_params["service_func"]
    gauss_cdf = gi_gi_inf_params["gauss_cdf"]
    x_max = 10.0
    cnt_tests = int(1e6)
    x_in, y_in = plot_module.tabulate_CDF_by_randCDF(input_flow, cnt_tests, False, x_max, 1.0)
    x_serv, y_serv = plot_module.tabulate_CDF_by_randCDF(service_func, cnt_tests, False, x_max, 1.0)
    x_gauss = np.linspace(0.0, 5.0, 300)
    plots = [
        {"x": x_in, "y": y_in, "title": "Input flow PDF"},
        {"x": x_serv, "y": y_serv, "title": "Serviced function"},
        {"x": x_gauss, "y": np.array([gauss_cdf(x) for x in x_gauss]), "title": "Gauss approx base"}
    ]
    plot_module.draw_plots(plots, "Experiments")

def gi_gi_inf_onetest():
    gi_gi_inf_params = gigiinf_load()
    input_flow = gi_gi_inf_params["input_flow"]
    service_func = gi_gi_inf_params["service_func"]
    T = gi_gi_inf_params["T"]
    gauss_cdf = gi_gi_inf_params["gauss_cdf"]
    r = exp_series(input_flow, service_func, T, gauss_cdf, int(1e4))
    plots = [
        {"x": r["x_P_i1"], "y": r["y_P_i1"], "title": "QMS series test frequences"},
        {"x": r["x_P_i"], "y": r["y_P_i"], "title": "Discrette Gauss Approximation"}
    ]
    plot_module.draw_plots(plots, "Experiment params here. Kolmogorov distance = " + str(r["kolmogorov_distance"]), True, "img/figure.jpg")

if __name__ == "__main__":
    #gi_gi_inf_plottest()
    gi_gi_inf_onetest()
    print("Finish modeling!")

