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
    input_lambda = 0.5
    exp_dist_lib = Exponential_Flow_Factory(input_lambda)
    exp_hand = cdf_rand.F_rand_factory(cdf.Exp_factory(input_lambda))
    print("Lib realisation: ", exp_dist_lib())
    r_value, type_interval = exp_hand()
    print("Own realisation: ", r_value, "; type = ", type_interval)

def distrib_types(n, input_lambda):
    # DEBUG test only ontime debugging
    if n < 1:
        return None
    type_distr = {0: 0, 1:0, 2:0}
    exp_hand = cdf_rand.F_rand_factory(cdf.Exp_factory(input_lambda))
    for i in range(0, n):
        r_val, type_interval = exp_hand()
        if type_interval < 3 and type_interval >= 0:
            type_distr[type_interval] += 1
    print(type_distr)

if __name__ == "__main__":
    #single_generate_test()
    distrib_types(10000, 0.01)
    print("Finish test Random Value with defined CDF!")

