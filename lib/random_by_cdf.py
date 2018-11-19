from numpy.random import random as uniform_dist

def F_rand_factory(cdf_func, steps_count = 10000, step_accuracy = 0.01):
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
    CDF_vals = [0]*steps_count
    cur_arg = 0.0
    for i in range(0, steps_count):
        CDF_vals[i] = cdf_func(cur_arg)
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
        def define_interval(f, f_vals, find_index, acc, r_value):
            """Calculate parameters for defining random value with
            cumulative distribution function f

            Parameters
            ----------
            f : function
                CDF function necessary distribution
            f_vals : list
                tabulated CDF f on some interval
            find_index : integer
                index of f_vals such than f_vals[find_index] very closely to r_value
            acc : number
                accuracy step - accuracy for finding value of Y: CDF(Y) ~= r_value
            r_value : number
                Random value of Uniform Distributed Random Value

            Returns
            -------
            tuple (y_k, `y_k+1`, f(y_k), f(`y_k+1`) )
            """
            if find_index < 0 or find_index >= len(f_vals):
                return (None, None, None, None)
            # DEBUG value type_interval:
            # 0 - inside f_vals
            # 1 - outside left f_vals
            # 2 - outside right f_vals
            type_interval = 0
            y_k = find_index * acc
            y_k_1 = y_k + acc
            f_k = f_vals[find_index]
            f_k_1 = 0.0
            if find_index == 0:
                if r_value > f_vals[find_index]:
                    f_k_1 = f_vals[find_index + 1]
                else:
                    type_interval = 1
                    y_k_1 = y_k
                    y_k -= acc
                    f_k_1 = f_k
                    f_k = f(y_k)
            elif find_index == len(f_vals) - 1:
                if r_value > f_vals[find_index]:
                    type_interval = 2
                    #TODO: make more accurate because true value of CDF(Y) may be
                    # too distance from f_vals[last_index] value
                    f_k_1 = f(y_k_1)
                else:
                    y_k_1 = y_k
                    y_k -= acc
                    f_k_1 = f_k
                    f_k = f_vals[find_index - 1]
            elif r_value > f_vals[find_index]:
                f_k_1 = f_vals[find_index + 1]
            else:
                y_k_1 = y_k
                y_k -= acc
                f_k_1 = f_k
                f_k = f_vals[find_index - 1]
            return y_k, y_k_1, f_k, f_k_1, type_interval
        
        x = uniform_dist()
        # find nearest y value according x
        cur_index = steps_count - 1
        borders = [0, steps_count - 1]
        while True:
            if x > CDF_vals[cur_index]:
                borders[0] = cur_index
            else:
                borders[1] = cur_index
            if borders[1] - borders[0] < 2:
                break
            cur_index = (borders[1] + borders[0]) // 2
        #DEBUG
        #print("find_index = ", cur_index)
        
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
        y_k, y_k_p_1, cdf_k, cdf_k_p_1, type_interval = define_interval(cdf_func, CDF_vals, cur_index, step_accuracy, x)
        return y_k + ( (x - cdf_k) * step_accuracy / (cdf_k_p_1 - cdf_k)  ), type_interval
    return rand_func_CDF
