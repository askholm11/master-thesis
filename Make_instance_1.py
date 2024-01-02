from numpy import loadtxt
import random
import numpy as np
from scipy.spatial import distance_matrix
from functools import reduce 
import math

def make_var(instance, mu = 1, delta = 0.75, psi=0.1):
    with open(instance, 'r') as f:
        input_size = int(f.readlines()[4][6:])
    info = loadtxt(instance, skiprows=11, max_rows=input_size)
    edges = np.array(loadtxt(instance, skiprows=12+input_size, max_rows=input_size))
    slice_idx = math.ceil(input_size/2)
    done = info[1:slice_idx]
    rand_size = int(delta*len(done))
    done = np.random.permutation(done)

    # Passengers after randomization
    rand_pas = done[:rand_size]

    rand_pas[:,3] = 1
          
    passengers = np.array([np.append(item, 0) for item in rand_pas])

    service_pass = np.concatenate([passengers[:,0], passengers[:,-2]])

    service_time_pass = [[i, random.randint(3,6)] for i in service_pass]
    
    # Packages after randomization
    rand_pack = done[rand_size:]
    rand_pack[:,3] = 2

    
    

    #pack_all =  np.vstack((rand_pack,remain_pack))
    packages = np.array([np.append(item, 1) for item in rand_pack])

    service_pack = np.concatenate([packages[:,0], packages[:,-2]])

    service_time_pack = [[i, random.randint(5,9)] for i in service_pack]

    # Costs for travelling
    dist_xy = np.array(info[:,[2,3]])

    dist = distance_matrix(dist_xy, dist_xy)
    cost = np.round(mu * dist, decimals=2)

    duration = np.round(psi * dist, decimals=0)

    # Service time
    service_time = np.vstack([service_time_pass, service_time_pack])

    service_time = service_time[service_time[:, 0].argsort()]
    
    
    requests = np.vstack([passengers[:,[0,3,4,5,6,7,8,9]],packages[:,[0,3,4,5,6,7,8,9]]])

    return requests, cost, service_time, duration
