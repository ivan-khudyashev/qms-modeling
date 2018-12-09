def qms_experiment_type1():
    #T = [1, 5, 10, 25, 50]
    T = [0.1, 1.0, 3.0, 5.0]
    gamma = [1.0, 0.5, 0.25]
    input_lambda = 0.8
    input_flow_F = Exponential_Flow_Factory(input_lambda)
    T_len = len(T)
    # define Gauss CDF with _params_{mu, sigma}
    mu = 0.0
    sigma = 1.0
    gauss_cdf = lambda x: norm_distribution.cdf(x, mu, sigma)
    cnt = 10
    for next_gamma in gamma:
        print("gamma = ", next_gamma)
        cur_i = 0
        res = []
        B = B_rand_factory(B_factory(next_gamma))
        for nextT in T:
            cur_i = cur_i + 1
            print(cur_i, " from ", T_len)
            res.append(experiment_series_qms(cnt, nextT, input_flow_F, B, gass_cdf))
        print("----------")
        print("T = ", T)
        print(res)
        print("----------")

if __name__ == "__main__":
    mu = 0.0
    sigma = 1.0
    gauss_cdf = lambda x: norm_distribution.cdf(x, mu, sigma)
    input_flow_F = Exponential_Flow_Factory(0.8)
    B = B_rand_factory(B_factory(1.0))
    res = experiment_series_qms(10, 3.0, input_flow_F, B, gauss_cdf)
    print(res)
    #qms_experiment_type1()
    #test_B_func(0.5)
    print("Finish modeling!")

