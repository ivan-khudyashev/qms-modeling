#Local imports
import path_correction
from lib.io_module import load_gi_gi_inf_params as gigiinf_load

def first_test():
    params = gigiinf_load("tests/ex_in_gigiinf2.json")
    print(params)
    for next_param in params:
        print("type = ", type(next_param), "; next_param: ", next_param)

if __name__ == "__main__":
    first_test()
