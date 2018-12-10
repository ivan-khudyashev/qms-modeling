import math
from collections import OrderedDict
# Local imports
from lib.cdf import CDF_factory as build_cdf
from lib.random_by_cdf import F_rand_factory as gen_rand_f
from lib.commons import discrette_gauss_aproximation as P_i

def qms(input_flow_f, request_service_f, T):
    """Queueing Model System
    Emulate some System which accept external flow of events (requests) and
    service events from that flow

    Parameters
    ----------
    input_flow_f : function
        random function defining time-interval of input requests
    request_service_f : function
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
        current_time += input_flow_f()
        if current_time + request_service_f() > T:
            cnt_left_requests += 1
        else:
            cnt_serviced_requests += 1
    return {"serviced": cnt_serviced_requests, "left": cnt_left_requests} 

def experiment_series_qms(input_flow_f, request_service_f, T, gauss_cdf, cnt_experiments=int(2e6)):
    """Carry out <cnt_experiments> starts of QMS with defined input flow and service
    function B = <request_service_f> and compare Resuls with approximation base on <gauss_cdf>

    Parameters
    ----------
    input_flow_f : function
        Random function which define when next request arrive in QMS
    request_service_f : function
        Random function which calculate next value of time when QMS evaluate next request
    T : number
        Interval of time (mean [0, T]) during which QMS serivece requests
    gauss_cdf : function
        Cummulative Distribution Function of Normalize (Gauss) Probabilities Distribution
        with integrated parameters _params_ = {mu: x, sigma: y}. Integration of parameters
        must be executed outside of this method and in it <gauss_cdf> must be just ready function
    cnt_experiments : integer
        Count of starts QMS
    """
    def add_experiment_res(qms_total_res, qms_current_res):
        """ Insert result of QMS work in ordered way. Ordered by count of 
        unserved(mean left in QMS after time is over) requests

        Parameters
        ----------
        qms_total_res : dictionary
            {
            current_len_left_req : integer
                current length of Count of unserved requests row in OrderedDict
            left_req_values : OrderedDict
                list of all Counts of unserved requests in QMS after time is over
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

    def handle_experiment_series_result(qms_total_res, gauss_aprox_F, n):
        """Handle results of n starts of QMS and calculate some needed statistical values.
        This most interesting function. It defines result of Modeling!

        Parameters
        ----------
        qms_total_res: dict
            {
            current_len_left_req : integer
                current length of Count of unserved requests row in OrderedDict
            left_req_values : OrderedDict
                list of all Counts of unserved requests in QMS after time is over
            }
            Total result from experiment's series
        gauss_aprox_F: function
            Approximation function P(x, _params_) defined in scientific work
        n: integer
            Count of starts of QMS. Ammount of samples of experiment's series.


        Returns
        -------
        dictionary (still under construction)
            {
            kolmogorov_distance : number
                special parameters for assessment of quality of discrette Gaus
                approximation P(x, _params_) for experiment's series results
            }
        """
        max_delta = -1 # Kolmogorov's distance
        cur_delta = 0
        for i in range(0, qms_total_res["current_len_left_req"]):
            cur_delta += ( qms_total_res["left_req_values"][i] / n - gauss_aprox_F(i) )
            if math.fabs(cur_delta) > max_delta:
                max_delta = math.fabs(cur_delta)
        # Define values for plotting distributions in returns
        dots_for_smooth_figure = 1000
        x_max = qms_total_res["current_len_left_req"] # need x_max - 1, because start from 0
        x_P_i = [x/dots_for_smooth_figure for x in range(0, dots_for_smooth_figure * x_max) if x % x_max == 0]
        return {
            "kolmogorov_distance": max_delta,
            "x_max": x_max - 1,
            "x_P_i1": list(qms_total_res["left_req_values"].keys()),
            "y_P_i1": [y / n for y in qms_total_res["left_req_values"].values()],
            "x_P_i": x_P_i,
            "y_P_i": [gauss_aprox_F(y) for y in x_P_i]
        }

    def print_all_result(qms_total_res):
        for i in range(0, qms_total_res["current_len_left_req"]):
            print(i, qms_total_res["left_req_values"][i])

    qms_exp_total_result = {"current_len_left_req": 1, "left_req_values": OrderedDict([(0, 0)])}
    #TODO: make normal progress bar
    progress_cnt_intervals = 10
    progress = 1
    for i in range(0, cnt_experiments):
        if i >= (cnt_experiments // progress_cnt_intervals) * progress:
            print("Progress: " + str(progress) + " of " + str(progress_cnt_intervals))
            progress += 1
        add_experiment_res(qms_exp_total_result, qms(input_flow_f, request_service_f, T) )
    return handle_experiment_series_result(qms_exp_total_result, P_i(gauss_cdf), cnt_experiments)
