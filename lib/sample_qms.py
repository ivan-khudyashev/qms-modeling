from numpy.random import exponential as exp_dist
from numpy.random import random as uniform_dist
from collections import OrderedDict
from math import fabs
from scipy.stats import norm as norm_distribution

def qms(input_flow, B, T):
    """Queueing Model System
    Emulate some System which accept external flow of events (requests) and
    service events from that flow

    Parameters
    ----------
    input_flow : function
        function which define exponential probability distribution with parameter lambda
        Parameters
        ----------
            lambda : number
                lambda-parameter of exponential distribution
    B : function
        Distribution of requests' service function. Define time spending for
        service each request.
    T : number
        Time interval during which System service input requests

    Returns
    -------
    dictionary
    {
        serviced: int
            count of serviced requests
        left: int
            count of requests still in work when time T is over
    }
    """
    current_time = 0.0
    cnt_left_requests = 0
    cnt_serviced_requests = 0
    while current_time < T:
        current_time = current_time + input_flow()
        if current_time + B() > T:
            cnt_left_requests += 1
        else:
            cnt_serviced_requests += 1
    return {"serviced": cnt_serviced_requests, "left": cnt_left_requests} 

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

def B_rand_factory(func_dist, steps_count = 100000, step_accuracy = 0.1):
    """ Define approximation for generated Random Value based on Distribution 
    Function in analitycal form. Return function-closure which generate 
    random values according to defined Distribution Function
    Parameters
    ----------
    func_dist : function
        Define analitycal Distribution Function for Random Value
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
        Random function for generate value of Random Value with 
        Distribution Function func_dist
    """
    y = [0]*steps_count
    cur_y = 0.0
    for i in range(0, steps_count):
        y[i] = func_dist(cur_y)
        cur_y = cur_y + step_accuracy
    def rand_func_B():
        """Function which generate random value for defined Distribution Function
        based on library Uniform Distribution
        Parameters
        ----------

        Returns
        -------
        number
            value of Random Value with defined Distribution Function
        """
        x = uniform_dist()
        # find nearest y value according x
        borders = [0, steps_count - 1]
        while True:
            cur_index = (borders[1] + borders[0]) // 2
            if borders[1] - borders[0] < 2:
                break
            if x > func_dist(y[cur_index]):
                borders[0] = cur_index
            else:
                borders[1] = cur_index
        find_index = borders[0]
        # TODO: when x out of range we need more accuracy
        
        # Method of calculation F(x) (B(x) in our case)
        #  was taken from
        #  https://www.intuit.ru/studies/courses/643/499/lecture/11355?page=4#sect7
        # y - random value with distribution function F()
        # y_k - preliminary calculated value of F()
        # x - current value of uniform continius distribution
        # F(y_k) - first value of F() for which: F(y_k) < x < F(y_k+1)
        # delta_y = y_k+1 - y_k
        # delta_F = F(y_k+1) - F(y_k)
        # MAIN equation: delta_F / delta_y = (x - F(y_k)) / (y - y_k)
        #
        # Hence: y = y_k + (x - F(y_k)) * delta_y / delta_F
        #DEBUG
        y_k = y[borders[0]]
        # TODO: check why this happen
        while func_dist(y_k) > x: # TODO: need to optimize!
            y_k = y_k - step_accuracy
        y_k_p_1 = y_k + step_accuracy
        ret_val = y_k + ((x - func_dist(y_k)) * step_accuracy / (func_dist(y_k_p_1) - func_dist(y_k)) )
        if ret_val > 1.0:
            # some cheat
            ret_val = 0.999 + (ret_val - 1.0) / (ret_val + 1.0) * 0.0001
        return ret_val
    return rand_func_B

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

def experiment_series_qms(cnt_experiments, T, input_flow_F, B, gauss_cdf):
    """Carry out <cnt_experiments> starts of QMS with defined input flow and service
    function B.

    Parameters
    ----------
    cnt_experiments : integer
        Count of starts QMS
    T : number
        Interval of time (mean [0, T]) during which QMS serivece requests
    input_flow_F : function
        Random function which define when next request arrive in QMS
    B : function
        Random function which calculate next value of time when QMS evaluate next request
    gauss_cdf : function
        Cummulative Distribution Function of Normalize (Gauss) Probabilities Distribution
        with integrated parameters _params_ = {mu: x, sigma: y}. Integration of parameters
        must be executed outside of this method
    """
    def add_experiment_res(qms_total_res, qms_current_res):
        """ Insert result of QMS work in ordered way. Ordered by count of 
        unserved(inwork, left) requests

        Parameters
        ----------
        qms_total_res : dictionary
            {
            current_len_left_req : integer
                current length of Count of unserved requests row in OrderedDict
            left_req_values : OrderedDict
                list of all Counts of unserved (left, inwork) requests in QMS after
                time is over
            }
            This help construct for union values of series QMS-iteration work
        qms_current_res : dictionary
            {
            left : integer
                Count of requests still inwork (left) in QMS after time is over
            serviced: integer
                Count of served requests in QMS before time is over
            }
            This result of one QMS-iteration work
        """
        if qms_current_res["left"] > qms_total_res["current_len_left_req"] - 1:
            # if left request has already not included in Total res dict
            #  then add all elements before (they 0) and this element
            for i in range(qms_total_res["current_len_left_req"], qms_current_res["left"]):
                qms_total_res["left_req_values"][i] = 0
            # index of Results by one less then size, because indexing from 0
            qms_total_res["current_len_left_req"] = qms_current_res["left"] + 1
            qms_total_res["left_req_values"][qms_current_res["left"]] = 1 # init value
        else:
            # Hence this index already present in Total res dict
            # That why just increment this value
            qms_total_res["left_req_values"][qms_current_res["left"]] += 1

    def discrette_gauss_aproximation(G):
        """Discrete Gauss aproximation function
        P(x,_params_) = (  G(x + 0.5, _params_) - G(x - 0.5, _params_) ) / ( 1 - G(-0.5, _params_))
        This formula defined in scientific work and try normalize (by deletion on (1 - G(-0.5, _params_)) )
        expected value of x requests in QMS. x requests defined by Cummulative Distribution Function(CDF) G - 
        Normalize (Gauss) Distribution CDF with parameters _params_ = (mu, sigma). Here mu - mathematical
        expectation, sigma - standard deviation (sigma**2 - variance or dispersion)
        
        Parameters
        ----------
        x : number
            x-value for Gauss CDF
        G : function
            CDF of Normalize (Gauss) Probabilities Distribuion with parameters _params_
            _params_ - dictionary
            {
            mu : number
                mathematical expectation
            sigma : number
                standard deviation
            }
            Parameters of Normalize Probabilities Distribution

        Returns
        -------
        number
            Approximation value that in QMS left x requests after time is over
        """
        return lambda x:(G(x + 0.5) - G(x - 0.5)) / (1.0 - G(-0.5))

    def handle_experiment_series_result(qms_total_res, n, gauss_aprox_F):
        """Handle results of n starts of QMS and calculate some needed statistical values

        Parameters
        """
        max_delta = -1 # Kolmogorov's distance
        cur_delta = 0
        for i in range(0, qms_total_res["current_len_left_req"]):
            cur_delta += ( qms_total_res["left_req_values"][i] / n - gauss_aprox_F(i) )
            if fabs(cur_delta) > max_delta:
                max_delta = fabs(cur_delta)
        return {"kolmogorov_distance": max_delta}

    def print_all_result(qms_total_res):
        for i in range(0, qms_total_res["current_len_left_req"]):
            print(i, qms_total_res["left_req_values"][i])

    qms_exp_total_result = {"current_len_left_req": 1, "left_req_values": OrderedDict([(0, 0)])}
    for i in range(0, cnt_experiments):
        add_experiment_res(qms_exp_total_result, qms(input_flow_F, B, T) )
    return handle_experiment_series_result(qms_exp_total_result, cnt_experiments, discrette_gauss_aproximation(gauss_cdf))

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

if __name__ == "__main__":
    experiment_series_qms(100, 3.0, 1.0, 0.8)
    #qms_experiment_type1()
    #test_B_func(0.5)

