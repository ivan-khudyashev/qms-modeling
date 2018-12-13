import numpy as np
#Local imports
import path_correction
from lib.io_module import load_gi_gi_inf_params as gigiinf_load
from lib.qms_gi_gi_inf import experiment_series_qms as exp_series
import lib.plot_module as plot_module
import lib.commons as commons

def gi_gi_inf_plottest():
    gi_gi_inf_params = gigiinf_load()[0]
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

def gi_gi_inf_test():
    gi_gi_inf_params = gigiinf_load()
    param_num = 1
    for param in gi_gi_inf_params:
        input_flow = param["input_flow"]
        service_func = param["service_func"]
        T = param["T"]
        gauss_cdf = param["gauss_cdf"]
        r = exp_series(input_flow, service_func, T, gauss_cdf, int(1e5))
        plots = [
            {"x": r["x_P_i1"], "y": r["y_P_i1"], "title": "QMS series test frequences"},
            {"x": r["x_P_i"], "y": r["y_P_i"], "title": "Discrette Gauss Approximation"}
        ]
        plot_module.draw_plots(plots, "Experiment params here. Kolmogorov distance = " + str(r["kolmogorov_distance"]), True, "img/figure" + str(param_num))
        param_num += 1

if __name__ == "__main__":
    #gi_gi_inf_plottest()
    gi_gi_inf_test()
    print("Finish modeling!")

