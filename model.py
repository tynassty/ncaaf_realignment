# tyler nass
import copy
import random
import matplotlib.pyplot as plt
import cost_functions as cf
from School import School


def create_schools(schools_file, rivals_file=None, return_dict=False):
    list_of_schools = []
    dict_of_schools = {}
    f = open(schools_file)
    for line in f:
        line = line.split(", ")
        school = School(line[0], float(line[1]), float(line[2][:-2]))
        list_of_schools.append(school)
        dict_of_schools.update({school.get_name(): school})
    f.close()

    if rivals_file:
        f = open(rivals_file)
        for line in f:
            line = line.split(", ")
            school = dict_of_schools.get(line[0])
            rival = dict_of_schools.get(line[1][:-1])
            school.add_rival(rival)
        f.close()

    if return_dict:
        return dict_of_schools
    else:
        return list_of_schools


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
    uneven_neighbor_states = random_swap_neighbors_uneven(state, batch_size=batch_size//4)
    neighbor_states.extend(uneven_neighbor_states)
    swaps += len(neighbor_states)
    # print(swaps)

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
    # print(swaps)
    return neighbor_states


def random_swap_neighbors_all(state, batch_size=None):
    k = len(state)
    neighbor_states = []

    for i in range(k):
        for j in range(k):
            if i != j:
                for ii in range(len(state[i])):
                    for jj in range(len(state[j])):
                        neighbor_state = copy.deepcopy(state)
                        temp1 = neighbor_state[i].pop(ii)
                        temp2 = neighbor_state[j].pop(jj)
                        neighbor_state[j].append(temp1)
                        neighbor_state[i].append(temp2)
                        neighbor_states.append(neighbor_state)
    return neighbor_states


def random_swap_neighbors_uneven(state, batch_size=100):
    k = len(state)
    neighbor_states = []
    swaps = 0
    max_size = 0
    for i in range(len(state)):  # find the largest list's size
        if len(state[i]) > max_size:
            max_size = len(state[i])
    for i in range(len(state)):  # iterate through each list
        if len(state[i]) == max_size:  # if a list is the (tied/)largest
            jrange = list(range(len(state)))
            random.shuffle(jrange)
            for j in jrange:  # iterate through lists
                if len(state[j]) < max_size:  # find second list that is not (tied/)largest
                    irange = list(range(len(state[i])))
                    random.shuffle(irange)
                    for ii in irange:  # for each school in first list
                        neighbor_state = copy.deepcopy(state)
                        temp = neighbor_state[i].pop(ii)
                        neighbor_state[j].append(temp)
                        neighbor_states.append(neighbor_state)  # create a neighbor state where the school is now in
                        # the second list
                        swaps += 1
                        if swaps >= batch_size:  # cut off if batch size reached
                            return neighbor_states
    return neighbor_states  # return if batch size is not reached


def hill_climb(schools, k, f, max_iter=100, print_info=True, show_graph=False, show_map=False, buffer=50, minimize=True,
               batch_size=100, print_freq=10, random_swap_function=random_swap_neighbors):
    current_state = initial_state(schools, k)
    current_cost = f(current_state)

    iteration = 0

    consecutive_optimum = 0
    x_axis = []
    data_to_plot = [[] for _ in range(k)]
    while iteration < max_iter:

        if print_info:
            if iteration % print_freq == 0:
                print("iteration:", f"{iteration:04d}", "current cost:", f"{current_cost:,.0f}",
                      "consecutive failures:", f"{consecutive_optimum:03d}")
                counts = [len(group) for group in current_state]
                distances = [f"{f([grp]):,.0f}" for grp in current_state]
                print(distances)
                print(counts)

        if show_graph:
            x_axis.append(iteration)
            for j in range(len(current_state)):
                data_to_plot[j].append(f([current_state[j]]))

        # neighbor_states = random_swap_neighbors_uneven(current_state, batch_size=batch_size)
        neighbor_states = random_swap_function(current_state, batch_size=batch_size)
        neighbor_states.append(initial_state(schools, k))

        best_state = current_state
        best_cost = current_cost
        for neighbor_state in neighbor_states:
            neighbor_cost = f(neighbor_state)
            if minimize:
                if neighbor_cost < best_cost:
                    best_state = neighbor_state
                    best_cost = neighbor_cost
            else:
                if neighbor_cost > best_cost:
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
            plt.plot(lon, lat, 'o', label=str(index))
        plt.title("map by conference")
        plt.legend()
        plt.xlim([-160, -65])
        plt.ylim([20, 50])
        plt.show()

    return current_state


def run_nwsl():
    schools = create_schools("nwsl.txt")
    k = 6

    result_state = hill_climb(schools, k, cf.state_total_distance, max_iter=2000, buffer=200, show_map=True,
                              show_graph=False, print_info=True, minimize=True, batch_size=100, print_freq=10)

    for i in range(len(result_state)):
        group = result_state[i]
        print("\nGROUP " + str(i) + ":")
        school_name_list = []
        for school in group:
            school_name_list.append(school.get_name())
        school_name_list.sort()
        print(school_name_list)


def run_with_divisions():
    schools = create_schools("ncaaf.txt", "rivalries.txt")
    k = 10

    result_state = hill_climb(schools, k, cf.cost_function, max_iter=2000, buffer=200, show_map=True,
                              show_graph=True, print_info=True, minimize=True, batch_size=100, print_freq=10)

    conferences = [[] for _ in range(len(result_state))]
    for i in range(len(result_state)):
        conference = result_state[i]
        conferences[i] = hill_climb(conference, 2, cf.cost_function, max_iter=2000, buffer=200, show_map=True,
                                    show_graph=False, print_info=True, minimize=True, batch_size=100, print_freq=10)

    for i in range(len(conferences)):
        conference = conferences[i]
        for j in range(len(conference)):
            division = conference[j]
            print("\nGROUP " + str(i) + " DIVISION " + str(j) + ":")
            school_name_list = []
            for school in division:
                school_name_list.append(school.get_name())
            school_name_list.sort()
            print(school_name_list)


def run_full():
    schools = create_schools("ncaaf.txt", "top_ten_matchups.txt")
    k = 10

    result_state = hill_climb(schools, k, cf.cost_function, max_iter=100, buffer=1, show_map=True,
                              show_graph=True, print_info=True, minimize=True, print_freq=1,
                              random_swap_function=random_swap_neighbors_all)
    for i in range(len(result_state)):
        group = result_state[i]
        print("\nGROUP " + str(i) + ":")
        school_name_list = []
        for school in group:
            school_name_list.append(school.get_name())
        school_name_list.sort()
        print(school_name_list)


def run():
    schools = create_schools("ncaaf.txt", "top_ten_matchups.txt")
    k = 10

    result_state = hill_climb(schools, k, cf.cost_function, max_iter=2000, buffer=200, show_map=True,
                              show_graph=True, print_info=True, minimize=True, batch_size=100, print_freq=10)
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

    # rsnu = random_swap_neighbors_uneven([[1, 2, 3], [4, 5], [6, 7]])
    # print(rsnu)
