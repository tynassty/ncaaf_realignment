# tyler nass
import copy
import math
import random
import urllib.request

from School import School


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


def create_schools():
    list_of_schools = []
    f = open("School_locations.txt")
    for line in f:
        line = line.split(", ")
        list_of_schools.append(School(line[0], float(line[1]), float(line[2][:-2])))
    return list_of_schools


def total_distance(schools: list):
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


def total_cost(state):
    """
    returns the total cost of a state
    :param state: the list of groups, where each group is a list of schools
    :return: the total cost
    """
    cost = 0.0
    for group in state:
        cost += total_distance(group)
    return cost


def initialize_state(schools, k, f):
    state = [[] for _ in range(k)]
    for school in schools:
        group = random.randint(0, k-1)
        state[group].append(school)
    return state


def random_swap(state):
    state_copy = state.copy()
    state_copy[0].append("dog")
    print(state, state_copy)


def neighbors(state, k):
    neighbor_states = []
    for i in range(k):
        for j in range(k):
            if i != j and len(state[i]) > 0:
                for x in range(len(state[i])):
                    neighbor_state = copy.deepcopy(state)
                    obj = neighbor_state[i].pop(x)
                    neighbor_state[j].append(obj)
                    neighbor_states.append(neighbor_state)
    return neighbor_states


if __name__ == "__main__":
    # schools = create_schools()
    # k = 10
    #
    # states = []
    # for i in range(10):
    #     state = initialize_state(schools, 2, total_distance)
    #     states.append(state)
    # for state in states:
    #     print(total_cost(state))

    print(neighbors([["a", "b"], ["c", "d"]], 2))







