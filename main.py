# tyler nass
import copy
import math
import random
import statistics
import urllib.request
import matplotlib.pyplot as plt

from School import School

COLORS = ['purple', 'green', 'blue', 'pink', 'brown', 'red', 'teal', 'orange', 'magenta', 'tan', 'cyan', 'grey',
          'lavender', 'maroon']


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
    random.shuffle(schools)
    return divide_list_evenly(schools, k)
    # state = [[] for _ in range(k)]
    # for school in schools:
    #     group = random.randint(0, k-1)
    #     state[group].append(school)
    # return state


def divide_list_evenly(lst, k):
    n = len(lst)
    group_size = n // k
    remainder = n % k

    groups = []
    start = 0
    for i in range(k):
        if i < remainder:
            end = start + group_size + 1
        else:
            end = start + group_size
        groups.append(lst[start:end])
        start = end

    return groups


def random_swap_neighbors(state, batch_size=100):

    k = len(state)
    neighbor_states = []
    swaps = 0
    while swaps < batch_size:
        i = random.randint(0, k-1)
        j = random.randint(0, k-1)
        if i != j:
            ii = random.randint(0, len(state[i])-1)
            jj = random.randint(0, len(state[j])-1)
            neighbor_state = copy.deepcopy(state)
            temp1 = neighbor_state[i].pop(ii)
            temp2 = neighbor_state[j].pop(jj)
            neighbor_state[j].append(temp1)
            neighbor_state[i].append(temp2)
            neighbor_states.append(neighbor_state)
            swaps += 1
    return neighbor_states


def hill_climb(schools, k, f, max_iter=100, print_info=True, show_graph=False, show_map=False, buffer=50):
    current_state = initial_state(schools, k)
    current_cost = f(current_state)

    iteration = 0

    consecutive_optimum = 0
    x_axis = []
    data_to_plot = [[] for _ in range(k)]
    while iteration < max_iter:

        if print_info:
            if iteration % 10 == 0:
                print("iteration:", "{:03d}".format(iteration), "current cost:", f"{current_cost:,.0f}")
                counts = [len(group) for group in current_state]
                distances = [f"{f([grp]):,.0f}" for grp in current_state]
                print(distances)
                # print(counts)

        if show_graph:
            x_axis.append(iteration)
            for j in range(len(current_state)):
                data_to_plot[j].append(group_total_distance(current_state[j]))

        neighbor_states = random_swap_neighbors(current_state)
        neighbor_states.append(initial_state(schools, k))

        best_state = current_state
        best_cost = current_cost
        for neighbor_state in neighbor_states:
            neighbor_cost = f(neighbor_state)
            if neighbor_cost < best_cost:
                best_state = neighbor_state
                best_cost = neighbor_cost

        if best_cost == current_cost:
            consecutive_optimum += 1
            if consecutive_optimum >= buffer:
                print("LOCAL MINIMUM REACHED on iteration", "{:03d}".format(iteration - buffer))
                break
        else:
            consecutive_optimum = 0

        current_state = best_state
        current_cost = best_cost

        iteration += 1

    if show_graph:
        plt.figure(figsize=(10, 5))
        for index in range(len(data_to_plot)):
            plt.plot(x_axis, data_to_plot[index], label="group "+str(index))
        plt.title("cost per school by iteration")
        plt.legend()
        plt.show()

    if show_map:
        plt.figure(figsize=(10, 5))
        for index in range(len(current_state)):
            grp = current_state[index]
            lat = [sch.get_latitude() for sch in grp]
            lon = [sch.get_longitude() for sch in grp]
            plt.plot(lon, lat, 'o')
        plt.title("map by conference")
        plt.show()

    return current_state


def cost_function(state):
    total_distance = state_total_distance(state)

    counts = []
    for group in state:
        counts.append(len(group))

    # return total_distance + (statistics.stdev(counts) * 1000)
    return total_distance + ((max(counts) - min(counts)) * 1000)


def one_small_group_cost_function(state):
    """cost function that only optimizes one group"""
    costs = [group_total_distance(group) for group in state]
    return min(costs)


def state_total_distance_squared(state):
    return state_total_distance(state) ** 2


def run():
    schools = create_schools()

    k = 67

    result_state = hill_climb(schools, k, state_total_distance_squared, max_iter=1000, buffer=200, show_map=False,
                              show_graph=True)
    for i in range(len(result_state)):
        group = result_state[i]
        print("\nGROUP " + str(i) + ":")
        school_name_list = []
        for school in group:
            school_name_list.append(school.get_name())
        school_name_list.sort()
        print(school_name_list)


if __name__ == "__main__":
    run()








