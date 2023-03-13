import math
import random


def cost_function(state):
    total_distance = state_total_distance(state)
    rival_count = state_rival_count(state)
    # print(total_distance, rival_count)
    return total_distance - (rival_count * 1000)


def noisy_state_total_distance(state):
    random_factor = random.random() - 0.5
    std = state_total_distance(state)
    return std + (0.1 * random_factor * std)


def state_total_distance_squared(state):
    """returns square of state total distance"""
    return state_total_distance(state) ** 2


def state_total_distance_root(state):
    """returns square root of state total distance"""
    return math.sqrt(state_total_distance(state))


def state_total_distance_except_one(state):
    costs = [group_total_distance(group) for group in state]
    costs.sort()
    return sum(costs[:-1])


def one_small_group_cost_function(state):
    """cost function that only optimizes one group"""
    costs = [group_total_distance(group) for group in state]
    return min(costs)


def state_total_distance(state):
    """
    returns the total total_cost of a state
    :param state: the list of groups, where each group is a list of schools
    :return: the total total_cost
    """
    total_cost = 0.0
    for group in state:
        total_cost += group_total_distance(group)
    return total_cost


def group_rival_count(schools: list):
    count = 0
    for i in range(len(schools)):
        for j in range(len(schools)):
            if schools[i].is_rival(schools[j]):
                count += 1
    return count


def state_rival_count(state):
    total_cost = 0.0
    for group in state:
        total_cost += group_rival_count(group)
    return total_cost


def group_total_distance(schools: list):
    """
    takes a list of schools and calculates the total distance between every pair of schools in the list
    :param schools: a list of schools
    :return: the total distance
    """
    distance = 0.0
    for i in range(len(schools)):
        for j in range(i, len(schools)):
            distance += great_circle_distance(schools[i].latitude, schools[i].longitude,
                                              schools[j].latitude, schools[j].longitude)
    return distance


def great_circle_distance(lat1, lon1, lat2, lon2, miles=True):
    """
    calculates the great circle distance between two points
    :param lat1: first latitude coordinate
    :param lon1: first longitude coordinate
    :param lat2: second latitude coordinate
    :param lon2: second longitude coordinate
    :param miles: boolean representing whether to use miles (rather than kilometers)
    :return: the great circle distance
    """
    # Convert decimal degrees to radians
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])

    # Haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
    c = 2 * math.asin(math.sqrt(a))
    if miles:
        r = 3956
    else:
        r = 6371
    return c * r
