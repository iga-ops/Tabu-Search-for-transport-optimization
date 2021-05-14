#!/usr/bin/python
# -*- coding: utf-8 -*-

import Functions as Fun
import copy
import time as tm

list_of_orders_ = copy.deepcopy(list_of_orders)
list_of_drivers_ = copy.deepcopy(list_of_drivers)
sum_of_rates = 0
sum_of_orders = 0
tabu_time = []
sum_of_time = 0


for i in range(0, number_of_bikes+number_of_scooters+number_of_motorbikes):
    start_time = tm.time()
    list_of_orders_ = Fun.tabu_search(list_of_drivers_[i], map_, list_of_orders_, unit_price, number_of_iterations, reset_time)
    tabu_time.append(round(tm.time()-start_time,5))
    sum_of_time += tabu_time[-1]
    print('Kierowca {0}:'.format(i+1))
    print('Zysk: {0}'.format(round(list_of_drivers_[i].rate,1)))
    print('Trasa: {0}'.format(list_of_drivers_[i].solution))
    for elem in list_of_drivers_[i].orders:
        sum_of_orders += 1
    sum_of_rates += list_of_drivers_[i].rate
print('Suma zysków: {0}'.format(round(sum_of_rates,1)))
print('Łączna ilość wykonanych zamówień: {0}'.format(sum_of_orders))

sum_of_weight = 0
sum_of_costs = 0
for elem in list_of_orders:
    sum_of_weight += elem.weight
gain = sum_of_weight*unit_price
for elem in list_of_drivers:
    sum_of_costs += elem.work_time*elem.vehicle.speed*(elem.vehicle.fuel_c+driver_cost)
reference_value = gain-sum_of_costs
print('Wartość odniesienia: {0}'.format(round(reference_value,1)))
print('Czas wykonywania algorytmu: {0} sekund'.format(round(sum_of_time,3)))

