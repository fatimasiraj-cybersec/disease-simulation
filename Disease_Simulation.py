# 
# diseaseSim.py - simulates the spread of disease through a population
#
#
# Version history:
#
# 28/10/24 - beta version released for FOP assignment
#

import numpy as np
import matplotlib.pyplot as plt
import random

#Function to get inputs from the user for population, neighborhood type, and rates
def UserInputs():
    population = int(input("Enter total population (e.g: 200): "))
    while population <= 0:
        print("Population must be a positive integer!")
        population = int(input("Enter total population (e.g: 200): "))

    neighborhood = input("Enter neighborhood type (moore or von neumann): ").lower()
    while neighborhood not in ['moore', 'von neumann']:
        print("Invalid input. Please enter 'moore' or 'von neumann'.")
        neighborhood = input("Enter neighborhood type (moore or von neumann): ").lower()

    recovery_rate = float(input("Enter recovery rate (0 to 1, e.g: 0.1 for 10%): "))
    while recovery_rate < 0 or recovery_rate > 1:
        print("Recovery rate must be between 0 and 1!")
        recovery_rate = float(input("Enter recovery rate (0 to 1, e.g: 0.1 for 10%): "))

    death_rate = float(input("Enter death rate (0 to 1, e.g: 0.05 for 5%): "))
    while death_rate < 0 or death_rate > 1:
        print("Death rate must be between 0 and 1.")
        death_rate = float(input("Enter death rate (0 to 1, e.g: 0.05 for 5%): "))

    immunity_rate = float(input("Enter immunity rate (0 to 1, e.g: 0.2 for 20%): "))
    while immunity_rate < 0 or immunity_rate > 1:
        print("Immunity rate must be between 0 and 1.")
        immunity_rate = float(input("Enter immunity rate (0 to 1, e.g: 0.2 for 20%): "))

    return population, neighborhood, recovery_rate, death_rate, immunity_rate

#Function to distribute people randomly on the grid
def distribute(grid, num_rows, num_cols, num_peeps):
    for _ in range(num_peeps):
        rpos, cpos = random.randint(0, num_rows-1), random.randint(0, num_cols-1)
        grid[rpos, cpos] += 1

#function to initialize the population with healthy and infected individuals
def InitializePopulation(population_size, grid_size):
    population_grids = [np.zeros(grid_size, dtype=int) for _ in range(5)]  #5 health statuses
    distribute(population_grids[1], grid_size[0], grid_size[1], int(population_size * 0.8))  #80% healthy
    distribute(population_grids[0], grid_size[0], grid_size[1], int(population_size * 0.2))  #20% Infected
    return population_grids

#function to move people based on their current position and the neighborhood type
def MovePeople(current_grid, next_grid, current_row, current_col, total_rows, total_cols, neighborhood_type):
    for _ in range(current_grid[current_row, current_col]):
        if neighborhood_type == 'moore':
            row_move, col_move = random.randint(-1, 1), random.randint(-1, 1) #people move 8 directions 
        else:
            possible_moves = [(0, 1), (1, 0), (0, -1), (-1, 0)]
            row_move, col_move = random.choice(possible_moves) #people move cardinal directions
        new_row = max(0, min(total_rows - 1, current_row + row_move))
        new_col = max(0, min(total_cols - 1, current_col + col_move))
        next_grid[new_row, new_col] += 1

#updates the health statuses based on infection, recovery, death, and immunity rates
def HealthStatus(population_grids, recovery_rate, death_rate, immunity_rate, grid_size):
    infected, healthy, recovered, dead, immune = population_grids
    for row in range(grid_size[0]):
        for col in range(grid_size[1]):
            #calculates new infections
            new_infections = np.random.binomial(healthy[row, col], 0.2 * (infected[row, col] / (np.sum(infected) + 1))) 
            infected[row, col] += new_infections
            healthy[row, col] -= new_infections
            #calculates recovery and death rates
            recoveries = np.random.binomial(infected[row, col], recovery_rate)
            deaths = np.random.binomial(infected[row, col] - recoveries, death_rate)
            infected[row, col] -= (recoveries + deaths)
            recovered[row, col] += recoveries
            dead[row, col] += deaths
            #calculates immunity from people who recovered 
            new_immune = np.random.binomial(recovered[row, col], immunity_rate)
            recovered[row, col] -= new_immune
            immune[row, col] += new_immune

#function to apply barriers to prevent movement to certain locations
def Barriers(population_grids, barrier_positions):
    for grid in population_grids:
        for barrier in barrier_positions:
            grid[barrier] = 0


#visualize the population's health status at each month
def Visualize(population_grids, month, simulation_params):
    grid_size = simulation_params["grid_size"]
    colors = simulation_params["colors"]
    health_statuses = simulation_params["health_statuses"]
    plt.figure(figsize=(12, 10))
    for status, grid in zip(health_statuses, population_grids):
        row_values, col_values = np.where(grid > 0)
        plt.scatter(col_values, row_values, s=simulation_params["dot_size"], c=colors[status], alpha=0.6, 
                    edgecolors="w", linewidth=0.5, label=status.capitalize())
    plt.xlim(0, grid_size[0])
    plt.ylim(0, grid_size[1])
    plt.grid(True, which='both', color='gray', linestyle='-', linewidth=0.5)
    plt.title(f"Population Health Status at Month {month}")
    plt.legend(loc="upper right")
    plt.savefig(f"simulation_month_{month}.png")
    plt.show()
    plt.close()

#function to print the number of people in each health status
def PrintHealthStatus(stats, month):
    print(f"Month {month}:")
    for status, count in stats.items():
        print(f"{status.capitalize()}: {count}")
    print()

#function to run the simulation, including updating the population grid at each month
def Simulation(population_size, neighborhood_type, recovery_rate, death_rate, immunity_rate, simulation_params):
    health_statuses = simulation_params["health_statuses"]
    grid_size = simulation_params["grid_size"]
    population_grids = InitializePopulation(population_size, grid_size)
    stats = []
    for month in range(simulation_params["timesteps"]):
        new_population_grids = [np.zeros(grid_size, dtype=int) for _ in health_statuses]  #storing the updated population for the next month
        for row in range(grid_size[0]):
            for col in range(grid_size[1]):
                for i, grid in enumerate(population_grids):
                    MovePeople(grid, new_population_grids[i], row, col, grid_size[0], grid_size[1], neighborhood_type)
        population_grids = new_population_grids
        Barriers(population_grids, simulation_params["barrier_positions"])
        HealthStatus(population_grids, recovery_rate, death_rate, immunity_rate, grid_size)
        stats.append({status: np.sum(grid) for status, grid in zip(health_statuses, population_grids)}) #records the total number of people in each health status
        PrintHealthStatus(stats[-1], month)
        if month in [0, 10, simulation_params["timesteps"] - 1]:
            Visualize(population_grids, month, simulation_params)


#main program to start the simulation
if __name__ == "__main__":
    #simulation parameters
    simulation_parameters = {
        "grid_size": (20, 20),
        "timesteps": 20,
        "barrier_positions": [(5, 5), (10, 10)],
        "airport_locations": [(2, 2), (18, 18)],
        "health_statuses": ["infected", "healthy", "recovered", "dead", "immune"],
        "colors": { "infected": "red", "healthy": "blue",  "recovered": "purple", "dead": "black",
            "immune": "green"},
        "dot_size": 50, }
    

    #user inputs for simulation
    population_size, neighborhood_type, recovery_rate, death_rate, immunity_rate = UserInputs()
    Simulation(population_size, neighborhood_type, recovery_rate, death_rate, immunity_rate, simulation_parameters)
