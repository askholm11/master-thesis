from numpy import loadtxt
import random
import numpy as np
from scipy.spatial import distance_matrix
from functools import reduce 
import time
import math
from Helper_func1 import check_feasible, cost_cal, service_cal, duration_cal

def Construct_sol(requests, dur, cost, servicetime, vehicle, max_serivce, pas_cost, pack_cost, max_duration):
    S = [[] for _ in range(vehicle)]
    n = reduce(lambda count, requests: count + len(requests), requests, 0)
    total_service_time = np.zeros(vehicle)
    duration = np.zeros(vehicle)
    while reduce(lambda count, S: count + len(S), S, 0) < n:
        #print('l', len(requests))
        CL = []
        for req in requests:
            for route in range(vehicle):
                check = check_feasible(req, route, total_service = total_service_time[route], service_time=servicetime, max_time=max_serivce)
                if check != None:
                    CL.append(check)
        if not CL:
            print('break')
            break

        # Evaluation of greedy function. Check impact of insertion of each (i,k) in CL
        cost_phi = []
        for (i,k) in CL:
            cur_r = []
            cur_cost = float('inf')
           
            K = S[k]

            '''When the route is empty the if condition is used.
            Else is when the route has other stops. If it a passenger, 0, then the delivery has to be the next stop
            and if it a package, 1, then the delivery can be placed at any point, the delivery just need to be
            after the pickup on the route'''
            if not K: 
                if i[-1] == 0:
                    cur_r = [[i[0], i[-2]]]
                    cur_cost = cost_cal(cur_r, cost, pas_cost ,pack_cost)
                else:
                    cur_r = [i[0], i[-2]]
                    cur_cost = cost_cal(cur_r, cost, pas_cost ,pack_cost)
            else:
                for r, _ in enumerate(K):
                    if i[-1] == 0:
                        new_r = K[0:r] + [[i[0],] + [i[-2],]] + K[r:]
                        new_cost = cost_cal(new_r, cost, pas_cost ,pack_cost)
                        dura = duration_cal(new_r, dur)
                        if new_cost < cur_cost and dura <= max_duration:
                            cur_r = new_r
                            cur_cost = new_cost
                    else:
                        new_r = K[0:r] + [i[0],] + K[r:]
                        pos = r
    
                        for p, _ in enumerate(new_r):
                            new_r_del = new_r[:pos + 1 + p] + [i[-2],] + new_r[pos + 1 + p:]
                            new_cost_del = cost_cal(new_r_del, cost, pas_cost ,pack_cost)
                            dura = duration_cal(new_r_del, dur)
                            if new_cost_del < cur_cost and dura <= max_duration:
                                cur_r = new_r_del
                                cur_cost = new_cost_del
                    
                            
            if not cur_r:
                continue

            cost_phi.append((cur_r, cur_cost, i[0], k))
        cost_phi.sort(key = lambda a: a[1])

        phi_min = cost_phi[0][1]
        phi_max = cost_phi[-1][1]

        alpha = 1

        phi_min_max = phi_min + alpha*(phi_max-phi_min)
        # Construction of RCL
        RCL = []
        
        for phi in cost_phi:
            if phi[1] <= phi_min_max:
                RCL.append(phi)

        insertion = RCL.pop(random.randrange(len(RCL)))

        S[insertion[-1]] = insertion[0]
        
        del_idx = np.where(requests[:,0] == insertion[-2])[0][0]
        requests = np.delete(requests, del_idx, axis = 0)
        total_service_time[insertion[-1]] = service_cal(S[insertion[-1]], servicetime)
        duration[insertion[-1]] = duration_cal(insertion[0], dur)
    return S