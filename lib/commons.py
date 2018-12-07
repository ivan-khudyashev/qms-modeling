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

def discrette_gauss_aproximation(G):
    """Discrete Gauss aproximation function
    P(x,_params_) = (  G(x + 0.5, _params_) - G(x - 0.5, _params_) ) / ( 1 - G(-0.5, _params_))
    This formula defined in scientific work and try normalize (by deletion on (1 - G(-0.5, _params_)) )
    expected value of x requests in QMS. x requests defined by Cummulative Distribution Function(CDF) G -
    Normalize (Gauss) Distribution CDF with parameters _params_ = (mu, sigma). Here mu - mathematical
    expectation, sigma - standard deviation (sigma**2 - variance or dispersion)
    
    Parameters
    ----------
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
    function
        Approximation function P(x, _params_) defined in scientific work
    """
    return lambda x:(G(x + 0.5) - G(x - 0.5)) / (1.0 - G(-0.5))
