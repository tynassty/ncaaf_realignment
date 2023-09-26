import random
import numpy as np

import model
from School import School

# Define genetic algorithm parameters
POPULATION_SIZE = 100
MAX_GENERATIONS = 3000
MUTATION_RATE = 0.1


def objective_function(conference_assignments):
    # Initialize variables to store the total distance and count of schools
    total_distance = 0.0
    total_schools = 0
    conference_sizes = []

    for conference in conference_assignments:
        if not conference:
            continue  # Skip empty conferences

        # Calculate the mean latitude and longitude for schools in the conference
        conference_center_lat = np.mean([school.latitude for school in conference])
        conference_center_lon = np.mean([school.longitude for school in conference])

        conference_distance = 0
        conference_schools = 0

        # Iterate over schools in the conference
        for school in conference:
            # Calculate the distance of the school to the conference center
            distance = ((school.latitude - conference_center_lat) ** 2 +
                        (school.longitude - conference_center_lon) ** 2) ** 0.5

            # Add the distance to the total and increment the count
            conference_distance += distance
            conference_schools += 1

        total_distance += conference_distance
        total_schools += conference_schools
        conference_sizes.append(conference_schools)

    # Calculate the average distance (avoid division by zero)
    if total_schools > 0:
        average_distance = total_distance / total_schools
    else:
        average_distance = 0.0

    conference_size_difference = max(conference_sizes) - min(conference_sizes)

    return average_distance


# Initialize the population
def initialize_population(schools, k, population_size):
    population = []
    for _ in range(population_size):
        # Randomly assign schools to conferences
        random.shuffle(schools)
        conference_assignments = [schools[i::k] for i in range(k)]
        population.append(conference_assignments)
    return population


# Perform tournament selection
def tournament_selection(population, fitness_values, tournament_size):
    selected_parents = []
    for _ in range(len(population)):
        tournament_indices = random.sample(range(len(population)), tournament_size)
        tournament_fitness_values = [fitness_values[i] for i in tournament_indices]
        winner_index = tournament_indices[np.argmin(tournament_fitness_values)]
        selected_parents.append(population[winner_index])
    return selected_parents


# Perform single-point crossover
def single_point_crossover(parent1, parent2):
    # crossover_point = random.randint(1, len(parent1) - 1)
    # child1 = parent1[:crossover_point] + parent2[crossover_point:]
    # child2 = parent2[:crossover_point] + parent1[crossover_point:]
    # return child1, child2
    child1 = parent1[:]
    child2 = parent2[:]
    return child1, child2


# Perform mutation by swapping schools between conferences
def mutation(conference_assignment, mutation_rate):
    mutated_assignment = [list(conference) for conference in conference_assignment]
    for conference in mutated_assignment:
        if len(conference) > 0:  # Ensure the conference is not empty
            if random.random() < mutation_rate:
                school_to_move = random.choice(conference)
                conference.remove(school_to_move)
                other_conference = random.choice([c for c in mutated_assignment if c is not conference])
                other_conference.append(school_to_move)
    return mutated_assignment


# Genetic algorithm
def genetic_algorithm(schools, k, population_size, max_generations, mutation_rate):
    population = initialize_population(schools, k, population_size)
    best_solution = None
    best_fitness = float('inf')  # Initialize with a high value for minimization

    for generation in range(max_generations):
        if generation % 100 == 0:
            print(generation, best_fitness)
        # Evaluate fitness for each individual in the population
        fitness_values = [objective_function(individual) for individual in population]

        # Select parents using tournament selection
        selected_parents = tournament_selection(population, fitness_values, tournament_size=5)

        # Create the next generation through crossover and mutation
        offspring = []
        while len(offspring) < population_size:
            parent1, parent2 = random.choices(selected_parents, k=2)
            child1, child2 = single_point_crossover(parent1, parent2)
            child1 = mutation(child1, mutation_rate)
            child2 = mutation(child2, mutation_rate)
            offspring.extend([child1, child2])

        # Replace the old population with the new generation
        population = offspring

        # Update the best solution found so far
        current_best_fitness = min(fitness_values)
        if current_best_fitness < best_fitness:
            best_fitness = current_best_fitness
            best_solution = population[fitness_values.index(current_best_fitness)]

    return best_solution, best_fitness


def int_div_round_up(dividend, divisor):
    return -(dividend // -divisor)


if __name__ == "__main__":
    # Replace with your school data
    schools = model.create_schools("ncaaf.txt")

    k = 67  # Number of conferences or groups

    population = initialize_population(schools, k, POPULATION_SIZE)

    best_solution, best_fitness = genetic_algorithm(schools, k, POPULATION_SIZE, MAX_GENERATIONS, MUTATION_RATE)

    # Print the best conference assignment and its fitness
    for i, conference in enumerate(best_solution):
        print(f"Conference {i+1}: {', '.join([school.name for school in conference])}")
    print(f"Best Fitness: {best_fitness}")

    model.create_and_save_image(best_solution, display=True, save=False)


