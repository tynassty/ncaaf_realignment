# Model

[back to overview](../README.md)

## Table of Contents
1. [Libraries and Imports](#libraries-and-imports)
2. [Functions](#functions)
   1. [Data Processing](#data-processing)
      1. [create_schools](#function-create_schools)
      2. [divide_list_evenly](#function-divide_list_evenly)
   2. [Hill Climbing](#hill-climbing)
      1. [hill_climb_greedy](#function-hill_climb_greedy)
   3. [Neighbor State Generation](#neighbor-state-generation)
      1. random_swap_neighbors_gen
   4. [Visualization](#visualization)
      1. show_map_f
      2. show_3d_map_f
      3. show_graph_f
      4. create_and_save_image
      5. print_state
   5. [Utility](#utility)
      1. int_div_round_up

## Libraries and Imports

## Functions

### Data Processing

#### Function `create_schools`
1. This function reads from a file `schools_file` to instantiate the School objects. Optionally, it can also read from a file `rivals_file` to add rivalry data.
2. Parameters
   1. `schools_file`
      1. Path to the schools data file.
      2. The row should be a header row.
      3. The first three columns should contain the school name, its latitude, and its longitude in that order
      4. Any subsequent columns can contain any data as a float or a boolean.
      5. A sample file exists at [ncaaf.txt](../ncaaf.txt).
   2. `rivals_rile=None`
3. Return

#### Function `divide_list_evenly`
1. A simple function that divides a list evenly into k groups.
2. Parameters
   1. `lst`
      1. A list
   2. `k`
      1. The number of desired groups
3. Return
   1. A list of lists, where the inner lists contain the elements of the initially passed `lst` divided among `k` groups such that each group has an equal number of members, or, if necessary, one extra member as the remainder is distributed among the groups.

### Hill Climbing

#### Function `hill_climb_greedy`
1. Finds a local optimum solution through a hill climb. Generates and evaluates each neighbor state of the current state until it finds a neighbor state that improves on the cost. At this point, that neighbor state becomes the current state and the algorithm repeats until it finds a state in which no neighbors can improve upon (local optimum) or the maximum number of iterations `max_iter` is surpassed.
2. Parameters
   1. `state` (list)
      1. 
   2. `f` (function)
      1. 
   3. `max_iter`
      1. 
   4. `print_info`
      1. 
   5. `show_graph`, `show_map`, `show_3d_map`
   6. `create_image`
   7. `minimize`
   8. `max_batch_size`
   9. `print_freq`
   10. `allow_uneven`

### Neighbor State Generation

### Visualization

### Utility

1. `divide_list_evenly`