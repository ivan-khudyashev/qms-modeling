from numpy.random import exponential as exp_dist

def qms(input_flow, service_dist, input_lambda, service_lambda, T):
    current_time = 0.0
    cnt_ns_events = 0
    cnt_all_events = 0
    while current_time < T:
        current_time = current_time + input_flow(input_lambda)
        cnt_all_events = cnt_all_events + 1
        if current_time + service_dist(service_lambda) > T:
            cnt_ns_events = cnt_ns_events + 1
    return cnt_ns_events

def exp_flow_gen():
    return lambda exp_param_lambda:exp_dist(1.0/exp_param_lambda)

def test_qms(cnt_experiment, T):
    input_l = 0.8
    service_l = 0.4
    avg_unserved = 0
    for i in range(0, cnt_experiment):
        avg_unserved = avg_unserved + qms(exp_flow_gen(), exp_flow_gen(), input_l, service_l, T)
    return avg_unserved / (cnt_experiment - 1.0)

if __name__ == "__main__":
    T = [1, 5, 10, 25, 50]
    T_len = len(T)
    cur_i = 0
    cnt = 1000000
    res = []
    for nextT in T:
        cur_i = cur_i + 1
        print(cur_i, " from ", T_len)
        res.append(test_qms(cnt, nextT))
    print(T)
    print(res)
