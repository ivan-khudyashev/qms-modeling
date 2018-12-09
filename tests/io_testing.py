#Local imports
import path_correction
from lib.io_module import load_gi_gi_inf_params as gigiinf_load

def first_test():
    params = gigiinf_load()
    print(params)

if __name__ == "__main__":
    first_test()
