import numpy as np
import commons
from cdf import CDF_factory

def print_CDF_values(cdf_f, vals):
    for x in vals:
        print("x = ", x, "cdf(x) = ", cdf_f(x))

def exp_func_def(input_lambda):
    exp_cdf = CDF_factory(commons.CDF_type.EXPONENTIAL,
                {"lambda_p": input_lambda}
              )
    return exp_cdf

def plot_cdf(cdf_f, x_values, plot_title = "Some CDF", title = "CDF"):
    import matplotlib.pyplot as plt
    plt.plot(x_values, np.array([cdf_f(x) for x in x_values]), label = plot_title)
    plt.xlabel('x label')
    plt.ylabel('y label')
    plt.title(title)
    plt.legend()
    plt.show()

if __name__ == "__main__":
    lambda_p = 5.0
    #print_CDF_values(exp_func_def(lambda_p), np.linspace(0.0, 5.0, 10))
    plot_cdf(exp_func_def(lambda_p), np.linspace(0.0, 5.0, 300), "Exponential CDF with l = " + str(lambda_p))
    print("Finish CDF module test")
