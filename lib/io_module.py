import json
import os.path
import math
# Local imports
import lib.commons as commons
from lib.cdf import CDF_factory as build_cdf
from lib.random_by_cdf import F_rand_factory as gen_rand_f

#TODO: make check as automatic by schema
def check_function_param(func_params):
    if not "type" in func_params or not isinstance(func_params["type"], str):
        return False
    # check if function registered in commons
    cdftype = commons.CDF_type[func_params["type"].upper()]
    if not isinstance(cdftype, commons.CDF_type):
        return False
    if not "parameters" in func_params or not isinstance(func_params["parameters"], dict):
        return False
    # check if parameters for registered type ALL exists
    for dist_param in commons.CDF_parameters_schema[cdftype].keys():
        if not dist_param in func_params["parameters"]:
            return False
    return True

def check_gi_gi_inf(json_params):
    # check if <input_flow_function> parameter exists
    if not "input_flow_function" in json_params or not isinstance(json_params["input_flow_function"], dict):
        return False
    if check_function_param(json_params["input_flow_function"]) == False:
        return False
    if not "serviced_time_function" in json_params or not isinstance(json_params["serviced_time_function"], dict):
        return False
    if check_function_param(json_params["serviced_time_function"]) == False:
        return False
    if not "T" in json_params:
        return False
    if not isinstance(json_params["T"], float) and not isinstance(json_params["T"], int):
        return False
    if not "gauss_aproximation" in  json_params or not isinstance(json_params["gauss_aproximation"], dict):
        return False
    if not ("mu" in json_params["gauss_aproximation"] and "dispersion" in json_params["gauss_aproximation"]):
        return False
    return True

def gen_rand_func_from_json(json_params, json_name_func):
    f_type = commons.CDF_type[json_params[json_name_func]["type"].upper()]
    func = gen_rand_f(build_cdf(f_type, json_params[json_name_func]["parameters"]))
    return func

def load_gi_gi_inf_params(filename="tests/gigiinf_input.json"):
    if not os.path.isfile(filename):
        return None
    json_params = json.load(open(filename))
    if check_gi_gi_inf(json_params):
        return {
            "input_flow": gen_rand_func_from_json(json_params, "input_flow_function"),
            "service_func": gen_rand_func_from_json(json_params, "serviced_time_function"),
            "T": float(json_params["T"]),
            "gauss_cdf": build_cdf(commons.CDF_type.GAUSS, {
                "mu": json_params["gauss_aproximation"]["mu"],
                "sigma": math.sqrt(json_params["gauss_aproximation"]["dispersion"])
                }
            )
        }
    #TODO: throw exception
    print("Not valid schema")
    return None
