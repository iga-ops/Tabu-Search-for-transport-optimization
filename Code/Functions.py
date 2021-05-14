#!/usr/bin/python
# -*- coding: utf-8 -*-

import Classes as Cls
from typing import List, Tuple
import random
import copy


def f_gain(unit_price, weight, distance, costs) -> float:
    return unit_price*weight-distance*costs


def map_generator(number_of_points, min_distance, max_distance, edge_probability) -> List:
    inf_ = float('inf')
    
    map_ = [inf_]*number_of_points
    for elem in range(len(map_)):
        map_[elem]=[inf_]*number_of_points
        
    for i in range(len(map_)):
        while map_[i] == number_of_points*[inf_]:
            for j in range(len(map_)):
                temp = random.random()
                if i!=j and temp < edge_probability:
                    map_[i][j] = random.randint(min_distance, max_distance)
                    
    for i in range(len(map_)):                
        col = [row[i] for row in map_]
        if col == number_of_points*[inf_]:
            map_ = map_generator(number_of_points, min_distance, max_distance, edge_probability)
            
    return map_


def define_locals(number_of_points, number_of_locals) -> List:
    locals_ = []
    for number in range(0, number_of_locals):
        temp = random.randint(0, number_of_points-1)
        while temp in locals_:
            temp = random.randint(0, number_of_points-1)
        locals_.append(temp)
    return locals_


def orders_generator(number_of_orders, min_delivery_time, max_delivery_time, min_weight, max_weight, number_of_points, locals_) -> List:
    list_of_orders = []
    for elem in range(number_of_orders):
        delivery_time = random.randint(10*min_delivery_time, 10*max_delivery_time)/10 #proporcjonalne do długosci trasy
        weight = random.randint(10*min_weight, 10*max_weight)/10
        end_p = random.randint(0, number_of_points-1) #nie może lokalem ???
        start_p = locals_[random.randint(0,len(locals_)-1)] 
        number = elem+1
        
        while start_p == end_p:
            end_p = random.randint(0, number_of_points-1)
            
        list_of_orders.append(Cls.Order(number, delivery_time, weight, start_p, end_p))

    return list_of_orders


def tabu_search(driver, map_, list_of_orders, unit_price, number_of_iterations, reset_time) -> Tuple:
    
    iteration = 0
    tabu_list = []
    for i in range(0, reset_time):
        tabu_list.append([])
    
    solution = first_solution(driver, map_)
    rate, driver_orders, copy_of_orders = solution_assessment(driver, map_, solution, list_of_orders, unit_price)
    driver.list_of_solutions.append(solution)
    driver.list_of_rate.append(rate)
    
    while(iteration < number_of_iterations):
        new_solution = next_solution(driver, map_, solution, tabu_list)
            
        new_rate, new_driver_orders, new_copy_of_orders = solution_assessment(driver, map_, new_solution, list_of_orders, unit_price)
        idx = iteration % reset_time

        driver.list_of_solutions.append(new_solution)
        driver.list_of_rate.append(new_rate)
        
        if new_rate > rate:
            rate = new_rate
            tabu_list[idx] = copy.copy(solution)
            solution = copy.copy(new_solution)
            driver_orders = new_driver_orders
            driver.left_time = driver.work_time - get_distance(map_, new_solution)/driver.vehicle.speed
            copy_of_orders = new_copy_of_orders
        else:
            tabu_list[idx] = copy.copy(new_solution)
        iteration += 1
    
    list_of_orders = copy_of_orders
    for elem in list_of_orders:
        if elem in driver_orders:
            elem.end_p = float('inf')
    
    driver.orders = driver_orders
    driver.solution = solution
    driver.rate = rate
    
    return list_of_orders


def get_distance(map_, solution) -> int:
    distance = 0
    for idx in range(1,len(solution)):
        distance += map_[solution[idx-1]][solution[idx]]
    return distance


def first_solution(driver, map_) -> List:
    solution = []
    inf_ = float('inf')
    driver.left_time = driver.work_time
    number_of_points = len(map_)-1
    solution.append(random.randint(0, number_of_points))
    attempt = 20
    while(driver.left_time > 0):
        next_ = random.randint(0, number_of_points)
        while(map_[solution[-1]][next_] == inf_):
            next_ = random.randint(0, number_of_points)
        if(driver.left_time - map_[solution[-1]][next_]/driver.vehicle.speed > 0):
            driver.left_time = driver.left_time - map_[solution[-1]][next_]/driver.vehicle.speed
            solution.append(next_)
        else:
            attempt -= 1
            if (attempt == 0):
                break
            
    return solution


def next_solution(driver, map_, solution, tabu_list) -> List:
    inf_=float('inf')
    check = 0
    
    if(len(solution) <= 3):
        driver.left_time = driver.work_time - get_distance(map_, solution)/driver.vehicle.speed
        number_of_points = len(map_)-1
        attempt = 20
        while(driver.left_time > 0):
            next_ = random.randint(0, number_of_points)
            while(map_[solution[-1]][next_] == inf_):
                next_ = random.randint(0, number_of_points)
            if(driver.left_time - map_[solution[-1]][next_]/driver.vehicle.speed > 0):
                    driver.left_time = driver.left_time - map_[solution[-1]][next_]/driver.vehicle.speed
                    solution.append(next_)
            else:
                attempt -= 1
                if (attempt == 0):
                    break
        if(solution not in tabu_list):
            return solution
            
    while(check == 0):
        changed_point_idx = random.randint(1, len(solution)-2)
        if (map_[solution[changed_point_idx-1]].count(inf_) <= len(map_[solution[changed_point_idx-1]])-2):
            iter_ = 0
            new_points = []
            previous_point = solution[changed_point_idx-1]
            next_point = solution[changed_point_idx+1]
            new_points.append(previous_point)
            accepted = 0
            while(accepted == 0):
                accepted = 0
                new_point = random.randint(0, len(map_[new_points[-1]])-1)
                if (map_[new_points[-1]][new_point] != float('inf')):
                    if (iter_ == 1):
                        new_points.append(new_point)
                        if(new_point == next_point):
                            accepted = 1
                    if (iter_ == 0 and new_point != solution[changed_point_idx] and new_point != next_point):
                        iter_ = 1
                        new_points.append(new_point)
        else:
            continue
        
        new_sol = []
        new_sol = solution[0:changed_point_idx-1]
        new_sol.extend(new_points)
        new_sol.extend(solution[changed_point_idx+2:])
        while(get_distance(map_, new_sol)/driver.vehicle.speed > driver.work_time):
            new_sol = new_sol[:-1]
            
        if (new_sol not in tabu_list):
            check = 1
        
    return new_sol


def checking_solution(driver, map_, list_of_orders, solution) -> Tuple:
    
    driver_orders = []
    copy_of_orders = copy.deepcopy(list_of_orders)
    driver_capacity = []
    for i in range(0,len(solution)):
        driver_capacity.append(driver.vehicle.capacity)
        
    for elem in copy_of_orders:
        if(elem.end_p != float('inf')):
            start_p_idx = [i for i,x in enumerate(solution) if x == elem.start_p]
            for idx in start_p_idx:
                driver_capacity_copy = copy.copy(driver_capacity)
                delivery_time = elem.delivery_time
                if(driver_capacity_copy[idx] >= elem.weight):
                    driver_capacity_copy[idx] -= elem.weight
                    point_idx = idx + 1
                    if(point_idx < len(solution) and solution[point_idx] != elem.end_p):
                        while(point_idx < len(solution) and delivery_time > 0 and driver_capacity_copy[point_idx] > 0 and solution[point_idx] != elem.end_p):
                            driver_capacity_copy[point_idx] -= elem.weight
                            delivery_time -= map_[solution[point_idx-1]][solution[point_idx]]/driver.vehicle.speed
                            point_idx += 1
                    if(point_idx < len(solution) and delivery_time >= map_[solution[point_idx-1]][solution[point_idx]]/driver.vehicle.speed and driver_capacity_copy[point_idx] > 0):
                        driver_orders.append(elem)
                        driver_capacity = copy.copy(driver_capacity_copy)
                        elem.end_p = float('inf')
                    continue
            
    return driver_orders, copy_of_orders


def solution_assessment(driver, map_, solution, list_of_orders, unit_price) -> Tuple:
    
    sum_of_weights = 0
    distance = get_distance(map_, solution)
    driver_orders = []
    driver_orders, copy_of_orders = checking_solution(driver, map_, list_of_orders, solution)
    for elem in driver_orders:
        sum_of_weights += elem.weight
    
    rate = f_gain(unit_price, sum_of_weights, distance, driver.driver_c + driver.vehicle.fuel_c)
    
    return rate, driver_orders, copy_of_orders
    
    