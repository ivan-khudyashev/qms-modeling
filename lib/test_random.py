from numpy.random import exponential as exp_dist
import cdf
import random_by_cdf as cdf_rand

def Exponential_Flow_Factory(input_lambda):
    """Factory for define function for generation random value distributed by
    Exponential Distribution Function. Use library function exp_dist
    Parameters
    ----------

    Returns
    -------
    function-closure
        Function for generate random value of Exponental Random Value based on
        parameter input_lambda
    """
    return lambda :exp_dist(1.0/input_lambda)

def single_generate_test():
    input_lambda = 1.0
    exp_dist_lib = Exponential_Flow_Factory(input_lambda)
    exp_hand = cdf_rand.F_rand_factory(cdf.Exp_factory(input_lambda))
    print("Lib realisation: ", exp_dist_lib())
    r_value = exp_hand()
    print("Own realisation: ", r_value)

def compare_with_lib_distrib(n, input_lambda):
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

    import numpy as np
    import matplotlib.pyplot as plt
    if n < 1:
        return None
    exp_dist_hand = cdf_rand.F_rand_factory(cdf.Exp_factory(input_lambda))
    exp_dist_lib = Exponential_Flow_Factory(input_lambda)
    # Initial values for defining plots
    y_max_scale = 10
    y_scale_koef = float(y_max_scale) / float(n)
    x_max = 5
    delta = 0.1
    points_count = int(x_max / delta)
    x = np.linspace(0, x_max, points_count)
    y_exp_hand = np.zeros(points_count, dtype = float)
    y_exp_lib = np.zeros(points_count, dtype = float)
    # experiments to get statistic for plots
    for i in range(0, n + 1):
        r_val = exp_dist_hand()
        y_exp_hand[found_interval(r_val, delta, points_count)] += y_scale_koef
        r_val = exp_dist_lib()
        y_exp_lib[found_interval(r_val, delta, points_count)] += y_scale_koef
    # Accumulate statistic for definint CDF
    #  since CDF(x) = P{X < x}, hence all previous intervals must added to all
    #  next intervals
    for i in range(1, points_count):
        y_exp_hand[i] += y_exp_hand[i - 1]
        y_exp_lib[i] += y_exp_lib[i - 1]
    # build plots
    plt.plot(x, y_exp_hand, label = "Hand Exp, l = " + str(input_lambda))
    plt.plot(x, y_exp_lib, label = "Lib exp, l = " + str(input_lambda))
    plt.xlabel("x label")
    plt.ylabel("y label")
    plt.title("Compare Lib and Hand Realisation. N = " + str(n))
    plt.legend()
    plt.show()

if __name__ == "__main__":
    #single_generate_test()
    compare_with_lib_distrib(10000, 0.5)
    print("Finish test Random Value with defined CDF!")

