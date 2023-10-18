# Conference Realignment Optimizer

## Introduction
The Conference Realignment Optimizer is a Python project that attempts to algorithmically generate college football conferences based on a variety of factors.
These factors include geographic location, Sagarin ratings, and rivalries.
This README provides an overview of the project and its functionality.

## Project Description
The goal of this project is to try to find an optimal grouping of schools into conferences based on certain criteria.
It uses a hill climbing algorithm.

The key features and components of this project include:

1. **School Data**
    - The project reads data from a file which contains data about each school.
    - The default file (`ncaaf.txt`) contains the following:
      - Each school's name
      - Its latitude and longitude
      - Its average season-end Sagarin rating over the 2005 to 2022 seasons
      - Boolean values representing whether it's a public school, whether it's an HBCU, and whether it is an R1: Doctoral University.
2. **Rivalries**
    - The project allows for the consideration of rivalries while optimizing. These rivalries can be weighted based on intensity.
    - There are two provided rivalry files:
      - `rivalries.txt`
        - This file contains a list of rivalries based on the Wikipedia article [List of NCAA college football rivalry games](https://en.wikipedia.org/wiki/List_of_NCAA_college_football_rivalry_games).
        - These rivalries are not weighted.
      - `knowrivalry.txt`
        - This file contains a list of rivalries taken from [Know Rivalry](https://knowrivalry.com/league/fbs-football/).
        - Know Rivalry is a project that collects rivalry data via surveys of fans, allowing fans of each school to assign up to 100 "rivalry points" to rival schools.
        - All rivalries in which one school's respondents give 10+ points to a given rival are included, and rivalries are weighted by the number of rivalry points assigned.
3. **Hill-Climbing Algorithm**
   - The project uses a hill-climbing algorithm to optimize conferences.
   - [Read more](documentation/model.md)

## Getting Started

### Usage
- Modify the data files:
  - Modify the main data file (`ncaaf.txt`) to include whatever data you wish to use for optimization.
  - Optionally, create a file (e.g., `rivalries.txt`) for school rivalries.
- Run the main script:
  ```bash
  python main.py
  ```
  
## Acknowledgments
This project was created by Tyler Nass. 
It was inspired by the wave of conference realignment in 2021-2024 in DI of the NCAA.