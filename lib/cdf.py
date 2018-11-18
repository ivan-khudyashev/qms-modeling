import math


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

def Exp_factory(lambda_p):
    def Exp_func_body(y):
        if y < 0.0:
            return 0.0
        return 1 - math.exp(-lambda_p * y) 
    return Exp_func_body
