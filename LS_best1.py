from numpy import loadtxt
import random
import numpy as np
from scipy.spatial import distance_matrix
from functools import reduce 
import time
import math
from Helper_func1 import cost_cal, duration_cal


def improved_best(new_route, duration, costs, best_cost, r, r_prime, requests, pas_cost, pack_cost, max_dur):
    if isinstance(r, list) and isinstance(r_prime, list):
        new_cost = cost_cal(new_route, costs, pas_cost ,pack_cost)
        duration = duration_cal(new_route, duration)
        if new_cost < best_cost and duration <= max_dur:
            #print('best update1')
            return True
        else:
            return False
        
    elif isinstance(r, list):
        pickup_del = [np.where(requests[:,0] == r_prime)[0], np.where(requests[:,1] == r_prime)[0]]
        
        req_idx = max(pickup_del, key=len)[0]

        pick_loc, del_loc = requests[req_idx]

        # Makes list iterable
        flat_route = []
        for row in new_route:
            if isinstance(row, list):
                for ele in row:
                    flat_route.append(ele)
            else:
                flat_route.append(row)

        pick_pos = flat_route.index(pick_loc)
        del_pos = flat_route.index(del_loc)

        if pick_pos <= del_pos:
            new_cost = cost_cal(new_route, costs, pas_cost ,pack_cost)
            duration = duration_cal(new_route, duration)
            if new_cost < best_cost and duration <= max_dur:
                #print('best update2-r')
                return True
        else:
            return False 
    

    elif isinstance(r_prime, list):
        pickup_del = [np.where(requests[:,0] == r)[0], np.where(requests[:,1] == r)[0]]
        
        req_idx = max(pickup_del, key=len)[0]

        pick_loc, del_loc = requests[req_idx]

        # Makes list iterable
        flat_route = []
        for row in new_route:
            if isinstance(row, list):
                for ele in row:
                    flat_route.append(ele)
            else:
                flat_route.append(row)

        pick_pos = flat_route.index(pick_loc)
        del_pos = flat_route.index(del_loc)

        if pick_pos <= del_pos:
            new_cost = cost_cal(new_route, costs, pas_cost ,pack_cost)
            duration = duration_cal(new_route, duration)
            if new_cost < best_cost and duration <= max_dur:
                #print('best update2-r_prime')
                return True
        else:
            return False 
    else:
        # For element r
        pickup_del = [np.where(requests[:,0] == r)[0], np.where(requests[:,1] == r)[0]]
        req_idx = max(pickup_del, key=len)[0]
        pick_loc, del_loc = requests[req_idx]

        # For element r'
        pickup_del_prime = [np.where(requests[:,0] == r_prime)[0], np.where(requests[:,1] == r_prime)[0]]
        req_idx_prime = max(pickup_del_prime, key=len)[0]
        pick_loc_prime, del_loc_prime = requests[req_idx_prime]

        # Makes list iterable
        flat_route = []
        for row in new_route:
            if isinstance(row, list):
                for ele in row:
                    flat_route.append(ele)
            else:
                flat_route.append(row)

        pick_pos = flat_route.index(pick_loc)
        del_pos = flat_route.index(del_loc)
        pick_pos_prime = flat_route.index(pick_loc_prime)
        del_pos_prime = flat_route.index(del_loc_prime)



        if pick_pos <= del_pos and pick_pos_prime <= del_pos_prime:
            new_cost = cost_cal(new_route, costs, pas_cost ,pack_cost)
            duration = duration_cal(new_route, duration)
            if new_cost < best_cost and duration <= max_dur:
                #print('best update3')
                return True
        else:
            return False 
        

def opt2_best(routes, req_specs, cost, dur, pas_cost, pack_cost, max_dur):
    opt2_cost =[cost_cal(start_route, cost, pas_cost, pack_cost) for start_route in routes]
    for idx_route, route in enumerate(routes):
        best_route = routes[idx_route]
        best_cost = opt2_cost[idx_route]
        
        for idx, r in enumerate(route):        
            if idx == 0:
                for idx_prime, r_prime in enumerate(route):
                    if idx == idx_prime or idx_prime == idx + 1 or idx_prime == len(route) - 1 :
                        continue 
                    sort_idx, sort_idx_prime = sorted([idx, idx_prime])
                    replace_route = (route[0:sort_idx+1] + (route[sort_idx+1:sort_idx_prime])[::-1] + route[sort_idx_prime:])
                    improve = improved_best(replace_route, dur, cost, best_cost, r, r_prime, req_specs, pas_cost, pack_cost, max_dur)
                    if improve:
                        best_route = replace_route
                        best_cost = cost_cal(best_route, cost, pas_cost ,pack_cost)
                        routes[idx_route] = best_route
                        opt2_cost[idx_route] = best_cost

            elif idx == len(route)-1:
                for idx_prime, r_prime in enumerate(route):
                    new_route = best_route
                    if idx == idx_prime or idx_prime == 0 or idx_prime == idx - 1:
                        continue 
                    sort_idx, sort_idx_prime = sorted([idx, idx_prime])
                    replace_route = (route[0:sort_idx+1] + (route[sort_idx+1:sort_idx_prime])[::-1] + route[sort_idx_prime:])
                    improve = improved_best(replace_route, dur, cost, best_cost, r, r_prime, req_specs, pas_cost, pack_cost, max_dur)
                    if improve:
                        best_route = replace_route
                        best_cost = cost_cal(best_route, cost, pas_cost, pack_cost)
                        routes[idx_route] = best_route
                        opt2_cost[idx_route] = best_cost
            else:
                for idx_prime, r_prime in enumerate(route):
                    new_route = best_route
                    if idx == idx_prime or idx_prime == idx + 1 or idx_prime == idx - 1:
                        continue 
                    sort_idx, sort_idx_prime = sorted([idx, idx_prime])
                    replace_route = (route[0:sort_idx+1] + (route[sort_idx+1:sort_idx_prime])[::-1] + route[sort_idx_prime:])
                    improve = improved_best(replace_route, dur, cost, best_cost, r, r_prime, req_specs, pas_cost, pack_cost, max_dur)
                    if improve:
                        best_route = replace_route
                        best_cost = cost_cal(best_route, cost, pas_cost, pack_cost)
                        routes[idx_route] = best_route
                        opt2_cost[idx_route] = best_cost 
    return routes, opt2_cost