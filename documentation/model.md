# Model

[back to overview](../README.md)

## Table of Contents
1. [Libraries and Imports](#libraries-and-imports)
2. [Functions](#functions)
   1. [Data Processing](#data-processing)
      1. [create_schools](#function-create_schools)
      2. [initial_state](#function-initial_state)
   2. [Hill Climbing](#hill-climbing)
      1. hill_climb
      2. hill_climb_greedy
   3. [Neighbor State Generation](#neighbor-state-generation)
   4. [Visualization](#visualization)
   5. [Utility](#utility)

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

#### Function `initial_state`
1. 

### Hill Climbing

### Neighbor State Generation

### Visualization

### Utility

1. `divide_list_evenly`