from numpy.random import exponential as exp_dist
from numpy.random import random as uniform_dist

def qms(input_flow, input_lambda, B, T):
    current_time = 0.0
    cnt_ns_events = 0
    cnt_all_events = 0
    while current_time < T:
        current_time = current_time + input_flow(input_lambda)
        cnt_all_events = cnt_all_events + 1
        if current_time + B() > T:
            cnt_ns_events = cnt_ns_events + 1
    return cnt_ns_events

def B_func(gamma):
    def B_func_body(y):
        return y**gamma/(1.0 + y**gamma)
    return B_func_body

def B_gen(func_dist, steps_count = 100000, step_accuracy = 0.1):
    y = [0]*steps_count
    cur_y = 0.0
    for i in range(0, steps_count):
        y[i] = func_dist(cur_y)
        cur_y = cur_y + step_accuracy
    def rand_func_B():
        x = uniform_dist()
        # find nearest y value according x
        borders = [0, steps_count - 1]
        while True:
            cur_index = (borders[1] + borders[0]) // 2
            if borders[1] - borders[0] < 2:
                break
            if x > func_dist(y[cur_index]):
                borders[0] = cur_index
            else:
                borders[1] = cur_index
        find_index = borders[0]
        # TODO: when x out of range we need more accuracy
        
        # Method of calculation F(x) (B(x) in our case)
        #  was taken from
        #  https://www.intuit.ru/studies/courses/643/499/lecture/11355?page=4#sect7
        # y - random value with distribution function F()
        # y_k - preliminary calculated value of F()
        # x - current value of uniform continius distribution
        # F(y_k) - first value of F() for which: F(y_k) < x < F(y_k+1)
        # delta_y = y_k+1 - y_k
        # delta_F = F(y_k+1) - F(y_k)
        # MAIN equation: delta_F / delta_y = (x - F(y_k)) / (y - y_k)
        #
        # Hence: y = y_k + (x - F(y_k)) * delta_y / delta_F
        #DEBUG
        y_k = y[borders[0]]
        # TODO: check why this happen
        while func_dist(y_k) > x: # TODO: need to optimize!
            y_k = y_k - step_accuracy
        y_k_p_1 = y_k + step_accuracy
        ret_val = y_k + ((x - func_dist(y_k)) * step_accuracy / (func_dist(y_k_p_1) - func_dist(y_k)) )
        if ret_val > 1.0:
            #print("uniform val = ", x)
            #print("finded index k = ", borders[0])
            #print("y_k = ", y_k)
            #print("y_k+1", y_k_p_1)
            #print("F(y_k)", func_dist(y_k))
            #print("F(y_k+1)", func_dist(y_k_p_1))
            #print("delta_y", step_accuracy)
            #print("delta_F", func_dist(y_k_p_1) - func_dist(y_k))
            # some cheat
            ret_val = 0.999 + (ret_val - 1.0) / (ret_val + 1.0) * 0.0001
        return ret_val
    return rand_func_B

def test_B_func(gamma):
    B = B_func(gamma)
    B_dist = B_gen(B)
    print("gen_value = ", B_dist())

def exp_flow_gen():
    return lambda exp_param_lambda:exp_dist(1.0/exp_param_lambda)

def test_qms(cnt_experiment, T, gamma):
    input_l = 0.8
    B = B_gen(B_func(gamma))
    avg_unserved = 0
    for i in range(0, cnt_experiment):
        avg_unserved = avg_unserved + qms(exp_flow_gen(), input_l, B, T)
    return avg_unserved / (cnt_experiment - 1.0)

def qms_experiment_type1():
    #T = [1, 5, 10, 25, 50]
    T = [0.1, 1.0, 3.0, 5.0]
    gamma = [1.0, 0.5, 0.25]
    T_len = len(T)
    cnt = 100000
    for next_gamma in gamma:
        print("gamma = ", next_gamma)
        cur_i = 0
        res = []
        for nextT in T:
            cur_i = cur_i + 1
            print(cur_i, " from ", T_len)
            res.append(test_qms(cnt, nextT, next_gamma))
        print("----------")
        print("T = ", T)
        print(res)
        print("----------")

if __name__ == "__main__":
    qms_experiment_type1()
    #test_B_func(0.5)

