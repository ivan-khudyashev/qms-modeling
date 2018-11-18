import cdf

def calc_single_value(input_lambda):
    exp_dist_cdf = cdf.Exp_factory(input_lambda)
    for i in range(0, 4):
        print("x = ", i, "exp_cdf(x) = ", exp_dist_cdf(i))

def plot_exp_cdf(input_lambda):
    import numpy as np
    import matplotlib.pyplot as plt

    exp_dist_cdf = cdf.Exp_factory(input_lambda)
    exp_dist_cdf1_5 = cdf.Exp_factory(1.5)
    x = np.linspace(0, 5, 300)
    plt.plot(x, np.array([exp_dist_cdf(i) for i in x]), label = 'Exponential CDF ' + str(input_lambda) )
    plt.plot(x, np.array([exp_dist_cdf1_5(i) for i in x]), label = 'Exponental CDF 1.5')
    plt.xlabel('x label')
    plt.ylabel('y label')
    plt.title("Exponental CDF")
    plt.legend()
    plt.show()

if __name__ == "__main__":
    input_lambda = 0.5
    #calc_single_value(input_lambda)
    plot_exp_cdf(input_lambda)
    print("Finish CDF module test")
