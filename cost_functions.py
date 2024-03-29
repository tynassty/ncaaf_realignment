import math
import random
from typing import List

import numpy as np

from School import School


def cost_function(state):
    total_distance = state_cost_by_function(state, group_avg_distance)
    sagarin_difference = state_cost_by_function_and_detail(state, group_detail_difference, "sagarin")
    # rival_count = state_rival_count(state)
    # public_difference = state_cost_by_function_and_detail(state, group_detail_difference, "public")
    # hbcu_difference = state_cost_by_function_and_detail(state, group_detail_difference, "HBCU")
    # r1_difference = state_cost_by_function_and_detail(state, group_detail_difference, "R1")

    # likemindedness = hbcu_difference + r1_difference - (10 * rival_count)
    # score = total_distance + (5.5 * sagarin_difference) + (100 * likemindedness)
    # score = total_distance + (3 * sagarin_difference) - (10 * rival_count)
    score = total_distance + (4 * sagarin_difference)
    return score


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


def group_rival_count(schools: list[School]):
    count = 0
    for i in range(len(schools)):
        for j in range(len(schools)):
            count += schools[i].get_rival_weight(schools[j])
    return count


def state_rival_count(state):
    return state_cost_by_function(state, group_cost_function=group_rival_count)


def state_total_distance(state):
    """
    returns the total total_cost of a state
    :param state: the list of groups, where each group is a list of schools
    :return: the total total_cost
    """
    return state_cost_by_function(state, group_cost_function=group_total_distance)


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


def group_avg_distance(schools: list):
    """
    takes a list of schools and calculates the average location. It then calculates the average distance to the center.
    :param schools:
    :return: average distance to center point.
    """
    center_point_lat = np.mean([school.latitude for school in schools])
    center_point_lon = np.mean([school.longitude for school in schools])
    distance = 0.0
    for school in schools:
        distance += great_circle_distance(school.latitude, school.longitude, center_point_lat, center_point_lon)
    return distance


def group_avg_distance_sqrt(schools: list):
    """
    takes a list of schools and calculates the average location. It then calculates the average distance to the center.
    :param schools:
    :return: average distance to center point.
    """
    center_point_lat = np.mean([school.latitude for school in schools])
    center_point_lon = np.mean([school.longitude for school in schools])
    distance = 0.0
    for school in schools:
        distance += math.sqrt(
            great_circle_distance(school.latitude, school.longitude, center_point_lat, center_point_lon))
    return distance


def group_sagarin_average(group):
    sagarin_sum = 0.0
    for i in range(len(group)):
        sagarin_sum += group[i].get_detail("sagarin")
    return sagarin_sum / len(group)


def group_sagarin_difference(group: List[School]):
    sagarin_difference = 0.0
    for i in range(len(group)):
        for j in range(i, len(group)):
            sagarin_difference += abs(group[i].get_detail("sagarin") - group[j].get_detail("sagarin"))
    return sagarin_difference


def group_detail_difference(group: List[School], detail: str):
    total_difference = 0.0
    for i in range(len(group)):
        for j in range(i, len(group)):
            total_difference += abs(group[i].get_detail(detail) - group[j].get_detail(detail))
    return total_difference


def group_sagarin_variation(group: List[School]):
    sagarin_sum = 0.0
    for school in group:
        sagarin_sum += school.get_detail("sagarin")
    sagarin_average = sagarin_sum / len(group)

    sagarin_variation = 0.0
    for school in group:
        sagarin_variation += abs(school.get_detail("sagarin") - sagarin_average)
    return sagarin_variation


def state_sagarin_difference(state):
    return state_cost_by_function(state, group_cost_function=group_sagarin_difference)


def state_cost_by_function(state, group_cost_function):
    total_cost = 0
    for group in state:
        total_cost += group_cost_function(group)
    return total_cost


def state_cost_by_function_and_detail(state, group_cost_function, detail):
    total_cost = 0
    for group in state:
        total_cost += group_cost_function(group, detail=detail)
    return total_cost


def state_sq_cost_by_function(state, group_cost_function):
    total_cost = 0
    for group in state:
        total_cost += group_cost_function(group) ** 2
    return total_cost


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
