from numpy.random import exponential as exp_dist
from numpy.random import random as uniform_dist
from scipy.stats import norm as norm_distribution
import math


def B_factory(gamma):
    """Factory for defining distribution function B for distribute
    serviced time intervals

    Parameters
    ----------
    gamma : number
        TODO: define this parameter

    Returns
    -------
    function-closure
        function B with defined parameter <gamma>
    """
    def B_func_body(y):
        """Distribution function represented in analitical form.
        This function define some Random value based by Distribution function
        Parameters
        ----------
        y : number
            TODO: define this parameter
        Returns
        number
            Time-interval necessary for service request
        """
        return y**gamma/(1.0 + y**gamma)
    return B_func_body

def Exp_factory(lambda_p):
    def Exp_func_body(y):
        if y < 0.0:
            return 0.0
        return 1 - math.exp(-lambda_p * y) 
    return Exp_func_body

def F_rand_factory(cdf_func, steps_count = 100000, step_accuracy = 0.1):
    """ Define approximation for generated Random Value based on Distribution 
    Function in analitycal form. Return function-closure which generate 
    random values according to defined Cumulative Distribution Function(CDF)
    Parameters
    ----------
    cdf_func : function
        Define analitycal CDF for Random Value
    steps_count : integer
        Internal variable. Define interval on Y-axes for more-closely approximation
        of ended value for generate Random Value. Besides Y-axes-interval defining by
        [0, step_counts * step_accuracy] Random Value calculate more rough
    step_accuracy : number
        Internal variable. Define accuracy for which on Y-axes was finding values of
        Random Value

    Returns
    -------
    function
        Random function for generate value of Random Value with CDF func_dist
    """
    y = [0]*steps_count
    cur_arg = 0.0
    for i in range(0, steps_count):
        y[i] = cdf_func(cur_arg)
        cur_arg += step_accuracy
    def rand_func_CDF():
        """Function which generate random value for defined CDF based on
        library Uniform Distribution
        Parameters
        ----------

        Returns
        -------
        number
            value of Random Value with defined CDF
        """
        x = uniform_dist()
        # find nearest y value according x
        borders = [0, steps_count - 1]
        while True:
            cur_index = (borders[1] + borders[0]) // 2
            if borders[1] - borders[0] < 2:
                break
            if x > y[cur_index]:
                borders[0] = cur_index
            else:
                borders[1] = cur_index
        find_index = borders[0]
        #DEBUG
        print("find_index = ", find_index)
        # TODO: when x out of range we need more accuracy
        
        # Method of calculation F(x)
        #  was taken from
        #  https://www.intuit.ru/studies/courses/643/499/lecture/11355?page=4#sect7
        # y - random value with distribution function F()
        # y_k - preliminary calculated value of F()
        # x - current value of uniform continius distribution
        # F(y_k) - first value of F() for which: F(y_k) < x < F(y_k+1)
        # delta_y = y_k+1 - y_k = step_accuracy
        # delta_F = F(y_k+1) - F(y_k)
        # MAIN equation: delta_F / delta_y = (x - F(y_k)) / (y - y_k)
        #
        # Hence: y = y_k + (x - F(y_k)) * delta_y / delta_F
        #DEBUG
        y_k = step_accuracy * borders[0]
        # TODO: check why this happen
        if cdf_func(y_k) > x:
            # It can only be when approximation interval [0; step_count * step_accuracy] not enough
            print("error when calculate Random_func by CDF")
        y_k_p_1 = y_k + step_accuracy
        ret_val = y_k + ((x - cdf_func(y_k)) * step_accuracy / (cdf_func(y_k_p_1) - cdf_func(y_k)) )
        return ret_val
    return rand_func_CDF

def test_B_func(gamma):
    """Function for debug-purpose. Create analitycal Distribution Function
    Parameters
    ----------

    Returns
    -------
    """
    B = B_factory(gamma)
    B_dist = B_rand_factory(B)
    print("gen_value = ", B_dist())

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


def single_exp_test():
    input_lambda = 0.5
    exp_dist_lib = Exponential_Flow_Factory(input_lambda)
    exp_hand = F_rand_factory(Exp_factory(input_lambda))
    print("Lib realisation: ", exp_dist_lib())
    print("Own realisation: ", exp_hand())

if __name__ == "__main__":
    single_exp_test()
    print("Finish modeling!")

