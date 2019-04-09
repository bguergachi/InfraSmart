import googlemaps
from itertools import combinations
import database
import numpy as np
import pandas as pd
import random

gmaps = googlemaps.Client(key="AIzaSyDerKFzrHHVHWIHqqohps8R36Tce0KEibQ")


class Router:
    def __init__(self, dataFrame, file=False):

        skip = False

        self._accessibility = dataFrame['availability'].values.tolist()

        self._all_waypoints = (dataFrame['lat'].map(str) + "," + dataFrame['lng'].map(str)).values.tolist()

        waypoint_distances = {}
        waypoint_durations = {}

        if file:
            for (waypoint1, waypoint2) in combinations(self._all_waypoints, 2):
                try:
                    route = gmaps.distance_matrix(origins=[waypoint1],
                                                  destinations=[waypoint2],
                                                  mode="driving",  # Change this to "walking" for walking directions,
                                                  # "bicycling" for biking directions, etc.
                                                  language="English",
                                                  units="metric")

                    # "distance" is in meters
                    distance = route["rows"][0]["elements"][0]["distance"]["value"]

                    # "duration" is in seconds
                    duration = route["rows"][0]["elements"][0]["duration"]["value"]

                    waypoint_distances[frozenset([waypoint1, waypoint2])] = distance
                    waypoint_durations[frozenset([waypoint1, waypoint2])] = duration

                except Exception as e:
                    print("Error with finding the route between %s and %s." % (waypoint1, waypoint2))
                    raise LookupError("Please fix Google maps API connection")

            with open("my-waypoints-dist-dur.tsv", "w") as out_file:
                out_file.write("\t".join(["waypoint1",
                                          "waypoint2",
                                          "distance_m",
                                          "duration_s"]))

                for (waypoint1, waypoint2) in waypoint_distances.keys():
                    out_file.write("\n" +
                                   "\t".join([waypoint1,
                                              waypoint2,
                                              str(waypoint_distances[frozenset([waypoint1, waypoint2])]),
                                              str(waypoint_durations[frozenset([waypoint1, waypoint2])])]))

        waypoint_distances = {}
        waypoint_durations = {}
        all_waypoints = set()

        waypoint_data = pd.read_csv("my-waypoints-dist-dur.tsv", sep="\t")

        for i, row in waypoint_data.iterrows():
            waypoint_distances[frozenset([row.waypoint1, row.waypoint2])] = row.distance_m
            waypoint_durations[frozenset([row.waypoint1, row.waypoint2])] = row.duration_s
            all_waypoints.update([row.waypoint1, row.waypoint2])

        self._waypoint_distances = waypoint_distances
        self._waypoint_durations = waypoint_durations
        self._all_waypoints = all_waypoints

    def _compute_fitness(self, solution, bias=0.1):
        """
            This function returns the total distance traveled on the current road trip.

            The genetic algorithm will favor road trips that have shorter
            total distances traveled.
        """

        solution_fitness = 0.0

        for index in range(len(solution)):
            waypoint1 = solution[index - 1]
            waypoint2 = solution[index]
            solution_fitness += self._waypoint_distances[frozenset([waypoint1, waypoint2])] * bias * (
                        1 - (self._accessibility[index] - self._accessibility[index - 1]) / sum(self._accessibility))

        return solution_fitness

    def _generate_random_agent(self):
        """
            Creates a random road trip from the waypoints.
        """

        new_random_agent = list(self._all_waypoints)
        random.shuffle(new_random_agent)
        return tuple(new_random_agent)

    def _mutate_agent(self, agent_genome, max_mutations=3):
        """
            Applies 1 - `max_mutations` point mutations to the given road trip.

            A point mutation swaps the order of two waypoints in the road trip.
        """

        agent_genome = list(agent_genome)
        num_mutations = random.randint(1, max_mutations)

        for mutation in range(num_mutations):
            swap_index1 = random.randint(0, len(agent_genome) - 1)
            swap_index2 = swap_index1

            while swap_index1 == swap_index2:
                swap_index2 = random.randint(0, len(agent_genome) - 1)

            agent_genome[swap_index1], agent_genome[swap_index2] = agent_genome[swap_index2], agent_genome[swap_index1]

        return tuple(agent_genome)

    def _shuffle_mutation(self, agent_genome):
        """
            Applies a single shuffle mutation to the given road trip.

            A shuffle mutation takes a random sub-section of the road trip
            and moves it to another location in the road trip.
        """

        agent_genome = list(agent_genome)

        start_index = random.randint(0, len(agent_genome) - 1)
        length = random.randint(2, 20)

        genome_subset = agent_genome[start_index:start_index + length]
        agent_genome = agent_genome[:start_index] + agent_genome[start_index + length:]

        insert_index = random.randint(0, len(agent_genome) + len(genome_subset) - 1)
        agent_genome = agent_genome[:insert_index] + genome_subset + agent_genome[insert_index:]

        return tuple(agent_genome)

    def _generate_random_population(self, pop_size):
        """
            Generates a list with `pop_size` number of random road trips.
        """

        random_population = []
        for agent in range(pop_size):
            random_population.append(self._generate_random_agent())
        return random_population

    def run_genetic_algorithm(self, generations=5000, population_size=100):
        """
            The core of the Genetic Algorithm.

            `generations` and `population_size` must be a multiple of 10.
        """

        population_subset_size = int(population_size / 10.)
        generations_10pct = int(generations / 10.)

        # Create a random population of `population_size` number of solutions.
        population = self._generate_random_population(population_size)

        # For `generations` number of repetitions...
        for generation in range(generations):

            # Compute the fitness of the entire current population
            population_fitness = {}

            for agent_genome in population:
                if agent_genome in population_fitness:
                    continue

                population_fitness[agent_genome] = self._compute_fitness(agent_genome)

            # Take the top 10% shortest road trips and produce offspring each from them
            new_population = []
            for rank, agent_genome in enumerate(sorted(population_fitness,
                                                       key=population_fitness.get)[:population_subset_size]):

                if (generation % generations_10pct == 0 or generation == generations - 1) and rank == 0:
                    print("Generation %d best: %d | Unique genomes: %d" % (generation,
                                                                           population_fitness[agent_genome],
                                                                           len(population_fitness)))
                    print(agent_genome)
                    print("")

                # Create 1 exact copy of each of the top road trips
                new_population.append(agent_genome)

                # Create 2 offspring with 1-3 point mutations
                for offspring in range(2):
                    new_population.append(self._mutate_agent(agent_genome, 3))

                # Create 7 offspring with a single shuffle mutation
                for offspring in range(7):
                    new_population.append(self._shuffle_mutation(agent_genome))

            # Replace the old population with the new population of offspring
            for i in range(len(population))[::-1]:
                del population[i]

            population = new_population

        return population


if __name__ == '__main__':
    sql = database.SQLServer('dumpstersite')
    markers = sql.getMarkersFromTraining()
    markerData = markers.reset_index(drop=True)
    markerData.index.name = 'id'
    markerData = markerData.iloc[:9]
    router = Router(markerData, file=True)
    stuff = router.run_genetic_algorithm()
    print(stuff)
