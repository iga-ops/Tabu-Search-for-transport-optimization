#!/usr/bin/python
# -*- coding: utf-8 -*-

#from typing import List
import Classes as Cls
import Functions as Fun

number_of_iterations = 1000
reset_time = 80
    
#MAPA
number_of_points = 10 #brak sprawdzenia number_of_points >= number_of_locals
number_of_locals = 3
edge_probability = 0.9 
min_distance = 1
max_distance = 20

map_= Fun.map_generator(number_of_points, min_distance, max_distance, edge_probability)
locals_ = Fun.define_locals(number_of_points, number_of_locals)

print('Generated city map:')
for row in map_:
    print(row)
print('\nPlacement of locals:\n{0}\n'.format(locals_))

#DRIVERS
bike = Cls.Vehicle(speed = 15, capacity = 20, fuel_c = 0)
motorbike = Cls.Vehicle(speed = 30, capacity = 30, fuel_c = 0.05)
scooter = Cls.Vehicle(speed = 20, capacity = 10, fuel_c = 0.005)
driver_cost = 0.8
work_time = 6

number_of_bikes = 1
number_of_scooters = 1
number_of_motorbikes = 1
list_of_drivers = []

for num in range(0,number_of_bikes):
    list_of_drivers.append(Cls.Driver(bike, driver_cost, work_time))
for num in range(0,number_of_scooters):
    list_of_drivers.append(Cls.Driver(scooter, driver_cost, work_time))
for num in range(0,number_of_motorbikes):
    list_of_drivers.append(Cls.Driver(motorbike, driver_cost, work_time))

#ORDERS
unit_price = 4

number_of_orders = 100
min_delivery_time = 1
max_delivery_time = 2
min_weight = 1
max_weight = 5

list_of_orders = Fun.orders_generator(number_of_orders, min_delivery_time, max_delivery_time, min_weight, max_weight, number_of_points, locals_)
copy_of_list_of_orders = Fun.copy.deepcopy(list_of_orders)

print('Generated orders:')
for elem in list_of_orders:
    print('({0}) Delivery time: {1}   Weight: {2}   Start point: {3}   End point: {4}'.format(elem.number, elem.delivery_time, elem.weight, elem.start_p, elem.end_p))

'''
for i in range(0, number_of_bikes+number_of_motorbikes+number_of_scooters):
    list_of_orders = Fun.tabu_search(list_of_drivers[i], map_, list_of_orders, unit_price)
    print('\nDriver {0}:'.format(i+1))
    print('Track: {0}'.format(list_of_drivers[i].solution))
    print('Rate: {0}'.format(list_of_drivers[i].rate))
    print('Orders:')
    for elem in list_of_drivers[i].orders:
        print('({0}) Delivery time: {1}   Weight: {2}   Start point: {3}   End point: {4}'.format(elem.number, elem.delivery_time, elem.weight, elem.start_p, copy_of_list_of_orders[elem.number-1].end_p))
'''




