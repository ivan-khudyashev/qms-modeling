from enum import Enum
# Global constants
## Define schemas for CDF
class CDF_type(Enum):
    """Enum for defining Cummulative Distribution Function
    (CDF) using in project qms-modeling
    """
    EXPONENTIAL = 1
    GAUSS = 2
    GAMMA = 3
    B_SERVICE = 4

"""Schema for defining name of parameters which using in
definition CDF. This schema used in Factory which
generated CDF.
"""
CDF_parameters_schema = {
    CDF_type.EXPONENTIAL: {"lambda_p": 0.5},
    CDF_type.GAUSS : {"mu": 1.0, "sigma": 0.5},
    CDF_type.GAMMA : {"a": 1.0, "thetta": 1.0},
    CDF_type.B_SERVICE : {"gamma": 0.5}
}
