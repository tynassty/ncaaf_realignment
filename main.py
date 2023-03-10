# tyler nass
import copy
import math
import random
import statistics
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


def initial_state(schools, k):
    state = [[] for _ in range(k)]
    for school in schools:
        group = random.randint(0, k-1)
        state[group].append(school)
    return state


def neighbors(state):
    k = len(state)
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


def hill_climb(schools, k, f, max_iter=100):
    current_state = initial_state(schools, k)
    current_cost = state_total_distance(current_state)

    i = 0

    while i < max_iter:
        if i % 10 == 0:
            print("i:", "{:03d}".format(i), "current cost:", f"{current_cost:,.3f}")
            counts = [len(group) for group in current_state]
            print(counts)
        neighbor_states = neighbors(current_state)

        best_state = current_state
        best_cost = current_cost
        for neighbor_state in neighbor_states:
            neighbor_cost = f(neighbor_state)
            if neighbor_cost < best_cost:
                best_state = neighbor_state
                best_cost = neighbor_cost

        if best_cost == current_cost:
            print("LOCAL MINIMUM REACHED on iteration", "{:03d}".format(i))
            break

        current_state = best_state
        current_cost = best_cost

        i += 1

    return current_state


def cost_function(state):
    total_distance = state_total_distance(state)

    counts = []
    for group in state:
        counts.append(len(group))

    # return total_distance + (statistics.stdev(counts) * 1000)
    return total_distance + ((max(counts) - min(counts)) * 1000)


if __name__ == "__main__":
    schools = create_schools()
    k = 13

    result_state = hill_climb(schools, k, state_total_distance, 1000)
    for group in result_state:
        print("\nGROUP:")
        school_name_list = []
        for school in group:
            school_name_list.append(school.get_name())
        school_name_list.sort()
        print(school_name_list)







