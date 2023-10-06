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


def create_schools(schools_file, rivals_file=None, return_dict=False):
    list_of_schools = []
    dict_of_schools = {}
    f = open(schools_file)
    for line in f:
        line = line.split(", ")
        line[-1] = line[-1][:-1]
        school = School(line[0], float(line[1]), float(line[2]))
        school.add_detail("sagarin", float(line[3]))
        school.add_detail("public", True if line[4] == "1" else False)
        school.add_detail("HBCU", True if line[5] == "1" else False)
        school.add_detail("R1", True if line[6] == "1" else False)
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


def random_swap_neighbors_gen(state):
    k = len(state)

    swaps_order = []

    for i in range(k):
        for j in range(i + 1, k):
            for ii in range(len(state[i])):
                for jj in range(len(state[j])):
                    swaps_order.append((i, j, ii, jj))

    # print(len(swaps_order))
    random.shuffle(swaps_order)

    for i, j, ii, jj in swaps_order:
        neighbor_state = copy.deepcopy(state)
        temp1 = neighbor_state[i].pop(ii)
        temp2 = neighbor_state[j].pop(jj)
        neighbor_state[j].append(temp1)
        neighbor_state[i].append(temp2)
        yield neighbor_state

    yield "over"


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
               batch_size=100, print_freq=10, generate_neighbors=random_swap_neighbors, create_image=False):
    """
    calculates an optimal solution through a hill climb
    :param create_image: boolean representing whether or not to produce an image of the logos grouped by group
    :param schools: a list of schools
    :param k: the number of groups to divide the schools into
    :param f: the maximization function to use
    :param max_iter: the maximum number of iterations to do
    :param print_info: a boolean representing whether to print information about the run to the console
    :param show_graph: a boolean representing whether to display a graph of the progression of costs
    :param show_map: a boolean representing whether to display a map of the optimal groups
    :param buffer: the number of iterations the model is allowed to do without making progress before terminating
    :param minimize: a boolean representing whether the hill climb should minimize (vs maximize)
    :param batch_size: the maximum number of neighbors to generate for each state
    :param print_freq: how often the current state should be printed to the console (iff print_info == True)
    :param generate_neighbors: the function to use to find neighbor states
    :return:
    """
    current_state = initial_state(schools, k)
    current_cost = f(current_state)

    iteration = 0

    consecutive_optimum = 0
    x_axis = []
    costs_to_plot = [[] for _ in range(k)]
    while iteration < max_iter:

        if print_info:
            if iteration % print_freq == 0:
                print("iteration:", f"{iteration:04d}", "current cost:", f"{current_cost:,.0f}",
                      "consecutive failures:", f"{consecutive_optimum:03d}")
                distances = [f"{f([grp]):,.0f}" for grp in current_state]
                counts = [len(group) for group in current_state]
                print(distances)
                print(counts)

        if show_graph:
            x_axis.append(iteration)
            for j in range(len(current_state)):
                costs_to_plot[j].append(f([current_state[j]]))

        neighbor_states = generate_neighbors(current_state, batch_size=batch_size)
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
    if iteration <= max_iter:
        print("Hill climb concluded")

    if show_graph:
        show_graph_f(costs_to_plot, x_axis)

    if show_map:
        show_map_f(current_state)

    # print([cf.group_sagarin_average(group) for group in current_state])
    current_state = sorted(current_state, key=lambda group: cf.group_sagarin_average(group), reverse=True)
    # print([cf.group_sagarin_average(group) for group in current_state])

    if create_image:
        create_and_save_image(current_state, display=False, save=True)

    return current_state


def show_map_f(current_state):
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


def show_graph_f(costs_to_plot, x_axis):
    plt.figure(figsize=(10, 5))
    for index in range(len(costs_to_plot)):
        plt.step(x_axis, costs_to_plot[index], label="group " + str(index))
    plt.title("cost per school by iteration")
    plt.legend()
    plt.show()


def hill_climb_greedy(schools, k, f, max_iter=100, print_info=True, show_graph=False, show_map=False, minimize=True,
                      max_batch_size=1000, print_freq=10, create_image=False):
    """
    calculates an optimal solution through a hill climb. even greedier than a hill climb inherently is. rather than
    evaluating a set of neighbor states and picking the best, it simply evaluates one at a time. if a state improves
    upon the current state even marginally, it chooses that state.
    :param create_image: boolean representing whether or not to produce an image of the logos grouped by group
    :param schools: a list of schools
    :param k: the number of groups to divide the schools into
    :param f: the maximization function to use
    :param max_iter: the maximum number of iterations to do
    :param print_info: a boolean representing whether to print information about the run to the console
    :param show_graph: a boolean representing whether to display a graph of the progression of costs
    :param show_map: a boolean representing whether to display a map of the optimal groups
    :param minimize: a boolean representing whether the hill climb should minimize (vs maximize)
    :param print_freq: how often the current state should be printed to the console (iff print_info == True)
    :return:
    """
    best_state = initial_state(schools, k)
    best_cost = f(best_state)

    iteration = 0

    x_axis = []
    costs_to_plot = [[] for _ in range(k)]
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

        neighbor_states_gen = random_swap_neighbors_gen(best_state)

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

    if iteration <= max_iter:
        print("Hill climb concluded")

    if show_graph:
        show_graph_f(costs_to_plot, x_axis)

    if show_map:
        show_map_f(best_state)

    best_state = sorted(best_state, key=lambda group: cf.group_sagarin_average(group), reverse=True)

    if create_image:
        create_and_save_image(best_state, display=False, save=True)

    return best_state


def text_to_image(text: str):
    image_size = 768
    font_size = 24
    image = Image.new('RGB', (image_size, image_size), 'white')
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype("arial.ttf", font_size)

    text_width, text_height = draw.textsize(text, font=font)
    x = (image_size - text_width) / 2
    y = (image_size - text_height) / 2

    draw.text((x, y), text, fill='black', font=font)

    return image


def create_and_save_image(state, display=True, save=True):
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
    return -(dividend // -divisor)


def print_state(result_state):
    for i in range(len(result_state)):
        group = result_state[i]
        print("\nGROUP " + str(i) + ":")
        school_name_list = []
        school_name_list.sort()
        for school in group:
            school_name_list.append(school.get_name())
        print(school_name_list)


def run_nwsl():
    schools = create_schools("nwsl.txt")
    k = 6

    result_state = hill_climb(schools, k, cf.state_total_distance, max_iter=2000, buffer=200, show_map=True,
                              show_graph=False, print_info=True, minimize=True, batch_size=100, print_freq=10)

    print_state(result_state)


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
        print_state(conference)


def run_full():
    schools = create_schools("ncaaf.txt", "top_ten_matchups.txt")
    k = 10

    result_state = hill_climb(schools, k, cf.cost_function, max_iter=100, buffer=1, show_map=True,
                              show_graph=True, print_info=True, minimize=True, print_freq=1,
                              generate_neighbors=random_swap_neighbors_all)
    print_state(result_state)


def image_test():
    schools = create_schools("ncaaf.txt", "top_ten_matchups.txt")

    result_state = hill_climb(schools, 10, cf.cost_function, max_iter=1, create_image=True)

    print_state(result_state)


def run_default(k=10, f=cf.cost_function, max_iter=2000, buffer=200, show_map=False, show_graph=False, print_info=True,
                minimize=True, batch_size=100, print_freq=10, create_image=False, find_neighbors=random_swap_neighbors):
    schools = create_schools("ncaaf.txt", "top_ten_matchups.txt")

    result_state = hill_climb(schools, k, f, max_iter=max_iter, buffer=buffer, show_map=show_map,
                              show_graph=show_graph, print_info=print_info, minimize=minimize, batch_size=batch_size,
                              print_freq=print_freq, create_image=create_image, generate_neighbors=find_neighbors)
    print_state(result_state)


if __name__ == "__main__":
    # run_default(create_image=True, max_iter=20000, batch_size=100, buffer=200, show_map=False,
                # f=cf.cost_function, minimize=True, print_freq=100, find_neighbors=random_swap_neighbors, k=17,
                # show_graph=True)
    # rsnu = random_swap_neighbors_uneven([[1, 2, 3], [4, 5], [6, 7]])
    # print(rsnu)

    schools = create_schools("ncaaf2.txt", rivals_file="rivalries.txt")
    k = 131

    # result_state = hill_climb(schools, k, cf.cost_function, print_freq=1, buffer=0, max_iter=1000,
    #                           create_image=True, batch_size=500, show_map=True, show_graph=True)
    # print_state(result_state)

    result_state = hill_climb_greedy(schools, k, cf.cost_function, print_freq=1, max_iter=1000, create_image=True,
                                     max_batch_size=33800, show_map=True, show_graph=True)
    print_state(result_state)

    # initial_state = initial_state(schools, k)
    # neighbors_gen = random_swap_neighbors_gen(initial_state)
    # print(len(list(neighbors_gen)))
