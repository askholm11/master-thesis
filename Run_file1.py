from numpy import loadtxt
import random
import numpy as np
from scipy.spatial import distance_matrix
from functools import reduce 
import time
import math
from Make_instance_1 import make_var
from Construct1 import Construct_sol
from Helper_func1 import cost_cal
from LS_first1 import opt2_first
from LS_best1 import opt2_best
from Construct2 import Construct_sol_random
import matplotlib.pyplot as plt


pass_cost = 5
packs_cost = 7
max_dura = 350

cost_first_diff = []
cost_best_diff = []
diff_avg_first = []
diff_avg_best = []

start = time.time()

requests, cost, service_time, dur = make_var('Data/bar-n100-3.txt', mu = 0.5, delta=0.6)
req_spec = np.insert(requests[:,[0,-2]],0, [0,0], axis=0)
print('instance made')

#for i in range(50):
    #
sol = Construct_sol(requests, dur, cost, service_time, 8, 75, pass_cost, packs_cost, max_dura)


for route in sol:
    route.insert(0,0)

sol_cost = [cost_cal(route, cost, pass_cost, packs_cost) for route in sol]

#print('ready for first-accept')

opt2first_sol, opt2first_cost = opt2_first(sol, req_spec, cost, dur=dur, pas_cost= pass_cost, pack_cost=packs_cost, max_dur=max_dura)
#print('cost first', np.sum(opt2first_cost)-np.sum(sol_cost))
diff_first = np.sum(opt2first_cost)-np.sum(sol_cost)
#print('first', diff_first)
cost_first_diff.append(diff_first)
#diff_avg_first.append([i, np.sum(cost_first_diff)/len(cost_first_diff)])

#
#print('ready for best-accept')
opt2best_sol, opt2best_cost = opt2_best(sol, req_spec, cost, dur=dur, pas_cost= pass_cost, pack_cost=packs_cost, max_dur=max_dura)
#print('cost best', np.sum(opt2best_cost)-np.sum(sol_cost))
diff_best = np.sum(opt2best_cost)-np.sum(sol_cost)
#print('best',diff_best)
cost_best_diff.append(diff_best)
#diff_avg_best.append([i, np.sum(cost_best_diff)/len(cost_best_diff)])

end = time.time()

print(end-start)


'''

diff_first_avg = np.array(diff_avg_first)
diff_best_avg = np.array(diff_avg_best)

#print('first-avg', diff_first_avg)
#print('best-avg', diff_first_avg)


plt.plot(diff_first_avg[:,0], diff_first_avg[:,1], 'm')
plt.plot(diff_best_avg[:,0], diff_best_avg[:,1], 'g')
plt.legend(['first-accept','best-accept'], loc = 0)
plt.title('Average improvement of 2-opt')
plt.xlabel('Iteration')
plt.ylabel('Average improvement')
plt.savefig('no-random-diff-100.png')
plt.show()
#print('first', np.sum(cost_first_diff)/len(cost_first_diff))

#print('best', np.sum(cost_best_diff)/len(cost_best_diff))


'''


