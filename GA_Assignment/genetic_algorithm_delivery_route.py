import random

# 1. Distance matrix (kilometres)
distance = {
    'A': {'A': 0, 'B': 4, 'C': 8, 'D': 6, 'E': 7, 'F': 9, 'G': 5},
    'B': {'A': 4, 'B': 0, 'C': 5, 'D': 7, 'E': 3, 'F': 8, 'G': 6},
    'C': {'A': 8, 'B': 5, 'C': 0, 'D': 4, 'E': 6, 'F': 3, 'G': 7},
    'D': {'A': 6, 'B': 7, 'C': 4, 'D': 0, 'E': 5, 'F': 6, 'G': 8},
    'E': {'A': 7, 'B': 3, 'C': 6, 'D': 5, 'E': 0, 'F': 4, 'G': 6},
    'F': {'A': 9, 'B': 8, 'C': 3, 'D': 6, 'E': 4, 'F': 0, 'G': 5},
    'G': {'A': 5, 'B': 6, 'C': 7, 'D': 8, 'E': 6, 'F': 5, 'G': 0}
}

# 2. Set parameters
random.seed(42)

population_size = 50
generations = 200
mutation_rate = 0.15

locations = ['B', 'C', 'D', 'E', 'F', 'G']


# 3. Calculate total route distance
def calculate_distance(route):
    full_route = ['A'] + route + ['A']

    total = 0

    for i in range(len(full_route) - 1):
        total += distance[full_route[i]][full_route[i + 1]]

    return total


# 4. Create initial population
def create_population():
    population = []

    for i in range(population_size):
        route = random.sample(locations, len(locations))
        population.append(route)

    return population


# 5. Selection (Tournament Selection)
def selection(population):
    candidates = random.sample(population, 3)

    best = min(candidates, key=calculate_distance)

    return best[:]


# 6. Crossover (Ordered Crossover)
def crossover(parent1, parent2):

    size = len(parent1)

    start, end = sorted(random.sample(range(size), 2))

    child = [None] * size

    child[start:end + 1] = parent1[start:end + 1]

    remaining = [
        location for location in parent2
        if location not in child
    ]

    empty_positions = (
        list(range(end + 1, size)) +
        list(range(0, start))
    )

    for position, location in zip(empty_positions, remaining):
        child[position] = location

    return child


# 7. Mutation (Swap Mutation)
def mutation(route):

    new_route = route[:]

    position1, position2 = random.sample(range(len(route)), 2)

    new_route[position1], new_route[position2] = (
        new_route[position2],
        new_route[position1]
    )

    return new_route


# 8. Genetic Algorithm
def genetic_algorithm():

    population = create_population()

    best_route = None

    for generation in range(generations):

        # Sort population based on distance
        population.sort(key=calculate_distance)

        # Save the best route
        if (best_route is None or
            calculate_distance(population[0]) <
            calculate_distance(best_route)):

            best_route = population[0][:]

        # Elitism: keep the best route
        new_population = [population[0][:]]

        while len(new_population) < population_size:

            # Select parents
            parent1 = selection(population)
            parent2 = selection(population)

            # Crossover
            child = crossover(parent1, parent2)

            # Mutation
            if random.random() < mutation_rate:
                child = mutation(child)

            new_population.append(child)

        population = new_population

    # Check the final population
    final_best = min(population, key=calculate_distance)

    if calculate_distance(final_best) < calculate_distance(best_route):
        best_route = final_best[:]

    return best_route


# 9. Run the Genetic Algorithm
best_route = genetic_algorithm()

# 10. Display results
final_route = ['A'] + best_route + ['A']

print("GENETIC ALGORITHM RESULTS")
print("-------------------------")

print("Best Route:", " -> ".join(final_route))

print("Total Distance:",
      calculate_distance(best_route), "km")