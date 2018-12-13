import math
from scipy.stats import norm as norm_distribution
from scipy.stats import gamma as gamma_distribution
# Local imports
import lib.commons as commons

def CDF_factory(cdf_type, params):
    """Factory for define CDF base on analitical or library representation.
    Return determination (mean not random) function for choosen CDF_type.
    CDF instantiate with input parameters if any exists or default
    parameters (in commons) - else.

    Parameters
    ----------
    cdf_type : enum CDF_type(Enum)
        type of CDF for return according function to caller
    params : dict
        Dictionary with parameters for choose CDF. Parameters must be 
        according schema defined in commons.CDF_parameters_schema

    Returns
    -------
    function-closure
        function which implement choosen CDF
    """
    def B_service_CDF(gamma):
        """CDF B in Queue System defined as service-time-interval function

        Parameters
        ----------
        gamma : number
            TODO: define this parameter

        Returns
        -------
        lambda-closure
            function B with defined parameter <gamma>
        """
        return lambda x: x**gamma/(1.0 + x**gamma)

    def Exponential_CDF(lambda_p):
        """CDF for exponential probabilities distribution
        https://en.wikipedia.org/wiki/Exponential_distribution

        Parameters
        ----------
        lambda_p : number
            TODO: define this parameter

        Returns
        -------
        function-closure
            Exponential CDF with defined parameter <lambda_p>
        """
        def Exp_func_body(x):
            if x < 0.0:
                return 0.0
            return 1 - math.exp(-lambda_p * x) 
        return Exp_func_body

    def Gauss_CDF(mu, sigma):
        """CDF of Normal (Gauss) probabilities distribution
        https://en.wikipedia.org/wiki/Normal_distribution

        Parameters
        ----------
        mu : number
            TODO: define this parameter
        sigma : number
            TODO: define this parameter

        Returns
        -------
        lambda-closure
            Normal (Gauss) CDF with defined parameters <mu>, <sigma>
        """
        return lambda x: norm_distribution.cdf(x, mu, sigma)

    def Gamma_CDF(alfa, betta):
        """CDF of Gamma probabilities distribution
        In SciPy library gamma distribution have 3 parameters: <a>, <loc>, <scale>.
        But in qms-modeling project using only 2: <alfa> and <betta>. Parameter <loc>
        is just offset on X-axis and it set to 0.0
        PDF in scipy-lib for this distribution define as
        PDF(x) = (x - loc)^(a - 1) * e^(-(x - loc)/scale) / (Г(a) * scale^a)
        There are 2 independent groups of parameters according Wikipedia:
        this https://en.wikipedia.org/wiki/Gamma_distribution:
        * (k, thetta)
        * (alfa, betta)
        and third group defined in python libraries <scipy.stats.gamma>:
        * (a, loc, scale)
        It is accordance:
        <a> the same as <k>
        <loc> accordance nothing
        <scale> the same as <thetta>
        But in theoretical work we have group of parameters (alfa, betta) and
        accordance:
        <alfa> the same as <k>
        <betta> the same as <scale>.
        THEREFORE:
        a = alfa
        scale = 1.0 / betta
        loc = 0.0
        

        Parameters
        ----------
        alfa : number
            This parameter define form of distribution
        betta: number
            This parameter define scale of distribution

        Returns
        -------
        lambda-closure
            CDF for Gamma-distribution
        """
        return lambda x: gamma_distribution.cdf(x, alfa, 0.0, 1.0 / thetta)

    def HyperExp_CDF(l1, l2, q):
    """CDF of hyperexponential probabilities distribution
    Common version of this distribution describes here:
    https://en.wikipedia.org/wiki/Hyperexponential_distribution
    CDF(x) = q*(1 - e^(-lambda_1 * x)) + (1 - q)*(1 - e^(-lambda2 * x))

    Parameters
    ----------
    l1: number
        lambda_1
    l2: number
        lambda_2
    q: number
        #TODO: define parameter

    Returns
    lambda-closure
        CDF for HyperExponential distribution
    """
        return lambda x:(q*(1 - math.exp(-l1 * x)) + (1 - q)*(1 - math.exp(-l2 * x)))
    
    # Process input and default params
    if not isinstance(cdf_type, commons.CDF_type):
        #TODO: throw exception
        return None
    #TODO: check is this necessary to COPY this args
    final_args = commons.CDF_parameters_schema[cdf_type]
    # If some params match CDF schema parameters then redefine its
    if isinstance(params, dict):
        for param_name, param_value in params.items():
            if param_name in final_args:
                final_args[param_name] = param_value
    # Define output func
    choose_cdf = None
    #TODO: think how redifine thiw switch() more elegant
    if cdf_type == commons.CDF_type.EXPONENTIAL:
        choose_cdf = Exponential_CDF
    if cdf_type == commons.CDF_type.GAUSS:
        choose_cdf = Gauss_CDF
    if cdf_type == commons.CDF_type.GAMMA:
        choose_cdf = Gamma_CDF
    if cdf_type == commons.CDF_type.B_SERVICE:
        choose_cdf = B_service_CDF
    if cdf_type == commons.CDF_type.HYPER_EXPONENTIAL:
        choose_cdf = HyperExp_CDF
    if choose_cdf == None:
        #TODO: throw exception
        return None
    return choose_cdf(**final_args)

