# Model

[back to overview](../README.md)

## Table of Contents
1. [Libraries and Imports](#libraries-and-imports)
2. [Functions](#functions)
   1. [Data Processing](#data-processing)
   2. [Hill Climbing](#hill-climbing)
   3. [Neighbor State Generation](#neighbor-state-generation)
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

This function reads from a file `schools_file` to instantiate the School objects. Optionally, it can also read from a file `rivals_file` to add rivalry data.

**Parameters**
- `schools_file`
  - Path to the schools data file.
  - The first row should be a header row.
  - The first three columns should contain the school name, its latitude, and its longitude in that order
  - Any subsequent columns can contain any data as a float or a boolean.
  - A sample file exists at [ncaaf.txt](../ncaaf.txt).
- `rivals_rile=None`

**Returns** a list of School objects.

#### Function `divide_list_evenly`

This is a simple function that divides a list evenly into k groups.

**Parameters**

1. `lst`
   - A list.
2. `k`
   - The number of desired groups.

**Returns**
a list of lists, where the inner lists contain the elements of the initially passed `lst` divided among `k` groups such that each group has an equal number of members, or, if necessary, one extra member as the remainder is distributed among the groups.

### Hill Climbing

#### Function `hill_climb_greedy`

This function performs a search for an optimum solution through a hill climbing approach. It iteratively generates and evaluates each neighbor state of the current state until it finds a neighbor state that improves on the cost. The algorithm repeats until it finds a local optimum or the maximum number of iterations `max_iter` is surpassed.

**Parameters**

1. `state` (list)
   - The initial state to start the hill climb process. It is a list of lists, where the outer list represents the current state, and each inner list contains School objects, representing a conference.
2. `f` (function)
   - The cost function used to evaluate states. This function takes a state as input and returns a float, representing the cost of that state. An example cost function `cost_function()` is available in the `cost_functions.py` file.
3. `max_iter` (int, optional)
   - The maximum number of iterations the hill climb should perform. If a local optimum is not found by the time the limit is reached, the process stops.
   - Default: 1000
4. `print_info` (bool, optional)
   - A boolean indicating whether to periodically print to the console information about the current best state found in the hill climb operation.
5. `show_graph` (bool, optional)
   - A boolean indicating
6. `show_map` (bool, optional)
   - A boolean indicating
7. `show_3d_map` (bool, optional)
   - A boolean indicating
8. `create_image` (bool, optional)
   - A boolean indicating
9. `minimize` (bool, optional)
   - A boolean indicating
10. `max_batch_size` (int, optional)
    - An integer
11. `print_freq` (int, optional)
    - An integer representing how often information should be printed to the console if `print_info` is `True`.
12. `allow_uneven` (bool, optional)
    - A boolean indicating

### Neighbor State Generation

#### Function `random_swap_neighbors_gen`

### Visualization

#### Function `show_map_f`

#### Function `show_3d_map_f`

#### Function `show_graph_f`

#### Function `create_and_save_image`

#### Function `print_state`

### Utility

#### Function `divide_list_evenly`