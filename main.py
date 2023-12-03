# tyler nass
import random
import model
import cost_functions as cf

if __name__ == "__main__":
    schools = model.create_schools("ncaaf.txt", rivals_file="knowrivalry.txt")
    random.shuffle(schools)
    state = model.divide_list_evenly(schools, 20)

    result_state = model.hill_climb_greedy(state, cf.cost_function, print_freq=1, max_iter=1000, create_image=True,
                                           max_batch_size=33856, show_map=True, show_3d_map=True, show_graph=True)

    model.print_state(result_state)
