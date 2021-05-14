#!/usr/bin/python
# -*- coding: utf-8 -*-

class Order:
    def __init__(self,number,delivery_time,weight,start_p,end_p) -> None:
        self.delivery_time = delivery_time
        self.weight = weight
        self.start_p = start_p
        self.end_p = end_p
        self.number = number

class Vehicle:
    def __init__(self, speed, capacity, fuel_c) -> None:
        self.speed = speed
        self.capacity = capacity
        self.fuel_c = fuel_c

class Driver:
    def __init__(self, vehicle, driver_c, work_time) -> None:
        self.vehicle = vehicle
        self.driver_c = driver_c
        self.left_time = work_time
        self.work_time = work_time
        self.orders = []
        self.solution = []
        self.rate = None
        self.list_of_solutions = []
        self.list_of_rate = []

    