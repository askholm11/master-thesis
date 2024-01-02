from numpy import loadtxt
import random
import numpy as np
from scipy.spatial import distance_matrix
from functools import reduce 
import time
import math

def check_feasible(request, route, total_service=0, service_time=0, max_time= 20):
    if request[-1] == 0:
        service_times =  service_time[int(request[0])-1][1] + service_time[int(request[-2]-1)][1]
        if service_times + total_service <= max_time:
            return (request, route)
        

    else:
        service_times =  service_time[int(request[0])-1][1] + service_time[int(request[-2]-1)][1]
        if service_times + total_service <= max_time:
            return (request, route)
        
def cost_cal(route, cost_matrix, pas_cost, pack_cost):
    flat_list = []
    count_pas = 0
    count_pack = 0
    for row in route:
        if isinstance(row, list):
            count_pas += 1
            for ele in row:
                flat_list.append(ele)
        else:
            count_pack += 1
            flat_list.append(row)
    len_r = len(flat_list)
    start_cost = cost_matrix[0][int(flat_list[0])]
    route_cost = [cost_matrix[int(flat_list[i-1])][int(flat_list[i])] for i in range(1,len_r)]
    depot_cost = cost_matrix[int(flat_list[len_r-1])][0]

    final_cost = start_cost + np.sum(route_cost) + depot_cost + count_pas * pas_cost + count_pack * pack_cost

    return final_cost

def service_cal(route, service_time):
    flat_list = []
    for row in route:
        if isinstance(row, list):
            for ele in row:
                flat_list.append(ele)
        else:
            flat_list.append(row)
    return np.sum([service_time[int(flat_list[i])-1][1] for i in range(len(flat_list))])

def duration_cal(route, dur):
    flat_list = []
    for row in route:
        if isinstance(row, list):
            for ele in row:
                flat_list.append(ele)
        else:
            flat_list.append(row)
    len_r = len(flat_list)
    start_dur = dur[0][int(flat_list[0])]#[int(flat_list[0])]
    route_dur = [dur[int(flat_list[i-1])][int(flat_list[i])] for i in range(1,len_r)]
    depot_dur = dur[int(flat_list[len_r-1])][0]

    duration = start_dur + np.sum(route_dur) + depot_dur


    return duration