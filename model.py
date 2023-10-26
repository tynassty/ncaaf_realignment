# tyler nass
import copy
import datetime
import math
import os.path
import random
import matplotlib.pyplot as plt
import cost_functions as cf
import drawing
from School import School
from PIL import Image, ImageDraw, ImageFont


def create_schools(schools_file, rivals_file=None):
    dict_of_schools = {}
    f = open(schools_file)

    header = next(f).strip().split(", ")
    print(header)

    for line in f:
        line = line.split(", ")
        line[-1] = line[-1][:-1]
        school = School(line[0], float(line[1]), float(line[2]))

        for i in range(3, len(header)):
            if line[i] == "1":
                school.add_detail(header[i], True)
            elif line[i] == "0":
                school.add_detail(header[i], False)
            else:
                try:
                    value_as_float = float(line[i])
                    school.add_detail(header[i], value_as_float)
                except ValueError:
                    print(f"Invalid value at index {i}: {line[i]}")

        dict_of_schools.update({school.get_name(): school})
    f.close()

    if rivals_file:
        f = open(rivals_file)
        for line in f:
            line = line.split(", ")
            line[-1] = line[-1][:-1]
            school = dict_of_schools.get(line[0])
            rival = dict_of_schools.get(line[1])
            weight = float(line[2])
            school.add_rival(rival, weight=weight)
        f.close()

    return list(dict_of_schools.values())


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


def random_swap_neighbors_gen(state, allow_uneven=True):
    k = len(state)
    max_size = max(len(lst) for lst in state)
    swaps_order = []

    for i in range(k):
        for j in range(i + 1, k):
            for ii in range(len(state[i])):
                for jj in range(len(state[j])):
                    swaps_order.append(("even", i, j, ii, jj))

    if allow_uneven:
        for i in range(len(state)):
            if len(state[i]) == max_size:
                jrange = list(range(len(state)))
                random.shuffle(jrange)
                for j in jrange:
                    if len(state[j]) < max_size:
                        irange = list(range(len(state[i])))
                        random.shuffle(irange)
                        for ii in irange:
                            swaps_order.append(("uneven", i, j, ii))

    random.shuffle(swaps_order)

    for swap_order in swaps_order:
        if swap_order[0] == "even":
            i, j, ii, jj = swap_order[1], swap_order[2], swap_order[3], swap_order[4]
            neighbor_state = copy.deepcopy(state)
            temp1 = neighbor_state[i].pop(ii)
            temp2 = neighbor_state[j].pop(jj)
            neighbor_state[j].append(temp1)
            neighbor_state[i].append(temp2)
            yield neighbor_state
        else:
            i, j, ii = swap_order[1], swap_order[2], swap_order[3]
            neighbor_state = copy.deepcopy(state)
            temp = neighbor_state[i].pop(ii)
            neighbor_state[j].append(temp)
            yield neighbor_state

    yield "over"


def sort_state(current_state):
    new_state = []
    for conference in current_state:
        new_state.append(sorted(conference, key=lambda school: school.get_name()))

    current_state = sorted(new_state, key=lambda group: cf.group_sagarin_average(group), reverse=True)
    return current_state


def show_map_f(current_state):
    """
    plots each school by its latitude and longitude. currently, does so on a simple pyplot graph
    :param current_state: a list of conferences, each being a list of School objects
    :return: none
    """
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
    plt.show(block=False)


def show_3d_map_f(current_state):
    """
    plots each school by its latitude and longitude, as well as by its sagarin rating
    :param current_state: a list of conferences, each being a list of School objects
    :return: none
    """
    plt.figure()
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    for index in range(len(current_state)):
        grp = current_state[index]
        lat = [sch.get_latitude() for sch in grp]
        lon = [sch.get_longitude() for sch in grp]
        sag = [sch.get_detail("sagarin") for sch in grp]
        ax.scatter(lon, lat, sag, marker='o')

    ax.set_xlabel('Latitude')
    ax.set_ylabel('Longitude')
    ax.set_zlabel('Sagarin rating')
    ax.set_ylim(10, 60)
    ax.set_xlim(-160, -60)
    plt.show()


def show_graph_f(costs_to_plot, x_axis):
    """
    a simple helper function to graph costs over time
    :param costs_to_plot: a list of lists, where the outer lists represent each conference and the inner lists represent
    the progression of the cost associated with that conference over each step of the hill climb
    :param x_axis: the graph's x axis (either the step numbers or the datetime of each step)
    :return: none
    """
    plt.figure(figsize=(10, 5))
    for index in range(len(costs_to_plot)):
        plt.step(x_axis, costs_to_plot[index], label="group " + str(index))
    plt.title("cost per school by iteration")
    plt.legend()
    plt.show()


def hill_climb_greedy(state, f, max_iter=1000, print_info=True, show_graph=False, show_map=False, show_3d_map=False,
                      minimize=True, max_batch_size=1000, print_freq=10, create_image=False, allow_uneven=True):
    """
    calculates an optimal solution through a hill climb. even greedier than a hill climb inherently is. rather than
    evaluating a set of neighbor states and picking the best, it simply evaluates one at a time. if a state improves
    upon the current state even marginally, it chooses that state.
    :param state: the initial starting state. a list of lists of School objects.
    :param create_image: boolean representing whether or not to produce an image of the logos grouped by group
    :param f: the maximization function to use
    :param max_iter: the maximum number of iterations to do
    :param print_info: a boolean representing whether to print information about the run to the console
    :param show_graph: a boolean representing whether to display a graph of the progression of costs
    :param show_map: a boolean representing whether to display a map of the optimal groups
    :param show_3d_map: a boolean representing whether to display a 3d map of the optimal groups
    :param minimize: a boolean representing whether the hill climb should minimize (vs maximize)
    :param print_freq: how often the current state should be printed to the console (iff print_info == True)
    :param allow_uneven: a boolean representing whether uneven swaps should be allowed
    :return:
    """
    best_state = state
    best_cost = f(best_state)

    iteration = 0

    x_axis = []
    costs_to_plot = [[] for _ in range(len(state))]
    finished = False

    total_indexes = 0
    while iteration < max_iter and not finished:

        if print_info:
            if iteration % print_freq == 0:
                if iteration != 0:
                    x = total_indexes/iteration
                else:
                    x = 1
                print("iteration:", f"{iteration:04d}", "--- current cost:", f"{best_cost:,.0f}",
                      "--- evals performed:", f"{total_indexes:,.0f}", "--- eval/iter:", f"{x:,.2f}")
                distances = [f"{f([grp]):,.0f}" for grp in best_state]
                counts = [len(group) for group in best_state]
                print(distances)
                print(counts)

        if show_graph:
            # x_axis.append(iteration)
            x_axis.append(datetime.datetime.now())
            for j in range(len(best_state)):
                costs_to_plot[j].append(f([best_state[j]]))

        neighbor_states_gen = random_swap_neighbors_gen(best_state, allow_uneven=allow_uneven)

        improved = False
        index = 0
        while not improved and not finished:
            if index > max_batch_size:
                print("Batch size exceeded")
                finished = True
                break
            neighbor_state = next(neighbor_states_gen)
            if neighbor_state == "over":
                print("Local optimum reached")
                finished = True
                break
            neighbor_cost = f(neighbor_state)
            if minimize:
                if neighbor_cost < best_cost:
                    best_state = neighbor_state
                    best_cost = neighbor_cost
                    improved = True
            else:
                if neighbor_cost > best_cost:
                    best_state = neighbor_state
                    best_cost = neighbor_cost
                    improved = True
            index += 1
            total_indexes += 1

        iteration += 1
        # best_state = sort_state(best_state)

    if iteration <= max_iter:
        print("Hill climb concluded")

    # print_state(best_state)

    if show_graph:
        show_graph_f(costs_to_plot, x_axis)

    if show_map:
        show_map_f(best_state)

    if show_3d_map:
        show_3d_map_f(best_state)

    best_state = sort_state(best_state)

    if create_image:
        create_and_save_image(best_state, display=False, save=True)

    return best_state


def create_and_save_image(state, display=True, save=True):
    """
    a function to create and save an image showing each school's logo arranged into the generated conferences
    :param state: a list of conferences, each being a list of School objects
    :param display: a boolean flag representing whether to display the created image
    :param save: a boolean flag representing whether to save the created image
    :return:
    """
    school_count = sum(len(group) for group in state)
    k = len(state)
    col_count = max(int_div_round_up(int_div_round_up(school_count, k), 2), 2)
    images = []

    for group in state:
        group_image_paths = []
        for school in group:
            image_path = school.get_name()
            image_path = image_path.replace(" ", "_")
            image_path = "images/" + image_path + ".png"
            if not os.path.isfile(image_path):
                image_path = "images/NCAA.png"
            group_image_paths.append(image_path)
        images.append(drawing.group_images_from_paths(group_image_paths, col_count))
    final_image = drawing.group_images(images, 1, group_spacing=0.5)

    if display:
        final_image.show()

    if save:
        width = final_image.width // 10
        height = final_image.height // 10
        final_image = final_image.resize((width, height))

        current_datetime = datetime.datetime.now()
        current_datetime_str = str(current_datetime).replace(" ", "_").replace(":", "-").replace(".", "-")
        image_filename = f"image_{current_datetime_str}.png"
        image_path = os.path.join("C:/Users/Tyler/OneDrive/Desktop/ncaaf_realign_gen", image_filename)
        final_image.save(image_path)
        return image_path

    return ""


def int_div_round_up(dividend, divisor):
    """
    Divides the dividend by the divisor and rounds up to the nearest integer value
    :param dividend: The number to be divided
    :param divisor: The number to divide by
    :return: The result of the division rounded up to the nearest integer
    """
    return -(dividend // -divisor)


def print_state(result_state):
    """
    Print the names of schools in each group within the result state
    :param result_state: a list of conferences, each being a list of School objects
    :return: none
    """
    for i in range(len(result_state)):
        group = result_state[i]
        print("\nGROUP " + str(i) + ":")
        school_name_list = []
        # school_name_list.sort()
        for school in group:
            school_name_list.append(school.get_name())
        print(school_name_list)


def image_test():
    schools = create_schools("ncaaf.txt", "top_ten_matchups.txt")
    random.shuffle(schools)
    state = divide_list_evenly(schools, 10)

    result_state = hill_climb_greedy(state, cf.cost_function, max_iter=1, create_image=True)

    print_state(result_state)


if __name__ == "__main__":

    schools = create_schools("ncaaf.txt", rivals_file="knowrivalry.txt")

    # k = 10

    random.shuffle(schools)
    state = divide_list_evenly(schools, 13)
    # state = sort_state(state)
    # print_state(state)

    result_state = hill_climb_greedy(state, cf.cost_function, print_freq=1, max_iter=1000, create_image=True,
                                     max_batch_size=33856, show_map=True, show_3d_map=True, show_graph=True)
    print_state(result_state)
