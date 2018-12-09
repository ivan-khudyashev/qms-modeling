import lib.commons as commons

def main_test():
    print("commons CDF_parameters_schema:")
    print(commons.CDF_parameters_schema)

def check_accord_type():
    a = commons.CDF_type.EXPONENTIAL
    b = 10
    print("a = ", a, "is CDF_type?: ", isinstance(a, commons.CDF_type))
    print("b = ", b, "is CDF_type?: ", isinstance(b, commons.CDF_type))

if __name__ == "__main__":
    #main_test()
    check_accord_type()
    print("Finish commons_test!")
