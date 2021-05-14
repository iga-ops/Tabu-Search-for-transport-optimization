# Tabu-Search-for-transport-optimization

## DETALIED DOCUMETATION
For a very detailed documentation, with a full problem description and testing process, click the link.
Detailed documantation in polish

## 1. Problem description
The considered optimization problem is from the category of transport theory - a company delivering food in a single city. In the created problem, the solution is to find the optimal allocation of supplies to suppliers and the order of their implementation, to maximize profits. 

Within the supplier network, 3 types of vehicles have been distinguished with different average delivery speeds, load capacity, and delivery costs: bike, electric scooter, motorbike. The delivered products will differ in weight and the point of receipt of the goods by the supplier. An additional parameter will be the maximum time after which they must reach the ordering person. The time specified as the maximum delivery time is counted from the moment the food is picked up by delivery service from the collection point. 

The supplier has the choice of executing orders individually or several at the same time, executing subsequent orders during the execution of the previous one, depending on which strategy will bring greater profit. At no time, however, its loading may exceed the maximum load capacity. Each supplier is associated with its labor costs depending on the allocated vehicle.  As a food delivery company, orders are selected from an available order base in a way that maximizes profits.

## 2. Alogithm adaptation
The specifications of the problem and the operating principles of the algorythm make the usage of Tabu Search in our case unconventional - firstly, the entire driver's route is being added as a solution, to which possible orders are being found.

The route is then modified randomly, taking into account the maximization of the number and the weight of the orders processed by drivers, whose collection and delivery points were included in the route. Thus, the orders made are directly dependent on the selected route, and the waypoints of a given driver are only indirectly changed based on the order list.

## 3. Algorithm steps
A simplified block diagram of the Tabu search algorithm for the adopted problem:


<img width="261" alt="przerobiony_graf_readme" src="https://user-images.githubusercontent.com/75940256/118335582-4237f600-b510-11eb-8482-5332524f8039.png">

