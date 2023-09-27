import random
import time
import json
import os
import matplotlib.pyplot as plt

def tour_distance(tour, dist_matrix):
    return sum(dist_matrix[tour[i-1]][tour[i]] for i in range(len(tour)))

def two_opt(tour, i, j):
    new_tour = tour[:i] + tour[i:j+1][::-1] + tour[j+1:]
    return new_tour

def three_opt(tour, i, j, k):
    seg1 = tour[:i]
    seg2 = tour[i:j]
    seg3 = tour[j:k]
    seg4 = tour[k:]
    new_tour = seg1 + seg3 + seg2 + seg4
    return new_tour

def local_search(tour, dist_matrix, operator):
    better_solution_found = True
    
    if operator == two_opt:
        while better_solution_found:
            better_solution_found = False
            for i in range(1, len(tour) - 1):
                for j in range(i+1, len(tour)):
                    if j-i == 1: continue
                    new_tour = two_opt(tour, i, j)
                    if tour_distance(new_tour, dist_matrix) < tour_distance(tour, dist_matrix):
                        tour = new_tour
                        better_solution_found = True
    else:
        while better_solution_found:
            better_solution_found = False
            for i in range(len(tour) - 2):
                for j in range(i + 1, len(tour) - 1):
                    for k in range(j + 1, len(tour)):
                        new_tour = three_opt(tour, i, j, k)
                        if tour_distance(new_tour, dist_matrix) < tour_distance(tour, dist_matrix):
                            tour = new_tour
                            better_solution_found = True
        
    return tour

def shaking(tour, k):
    new_tour = tour[:]
    for _ in range(k):
        i, j = sorted(random.sample(range(1, len(tour)-1), 2))
        new_tour = two_opt(new_tour, i, j)
    return new_tour

def vns(tour, dist_matrix, k_max=500, operator=two_opt):
    k = 1
    total_exploration_time = 0
    total_exploitation_time = 0
    while k <= k_max:
        time_start = time.time()
        k_tour = shaking(tour, k)
        time_end = time.time()
        total_exploration_time += time_end - time_start
        time_start = time.time()
        new_tour = local_search(k_tour, dist_matrix, operator)
        time_end = time.time()
        total_exploitation_time += time_end - time_start
        if tour_distance(new_tour, dist_matrix) < tour_distance(tour, dist_matrix):
            tour = new_tour
            k = 1
        else:
            k += 1
    return tour, total_exploration_time, total_exploitation_time


with open("benchmark_dataset/optimal_solutions.json", "r") as json_file:
    optimal_solutions = json.load(json_file)

benchmark_dir = "benchmark_dataset"

txt_files = [f for f in os.listdir(benchmark_dir) if f.endswith('.txt')]

results = []
counter = 1

for txt_file in txt_files:
    print(f"Test: {counter}/{len(txt_files)}")
    matrix_number = txt_file.split('.')[0]

    with open(os.path.join(benchmark_dir, txt_file), "r") as file:
        lines = file.readlines()
        dist_matrix = [list(map(float, line.split())) for line in lines]
    
    initial_tour = random.sample(range(len(dist_matrix)), len(dist_matrix))
    time_start = time.time()
    best_tour, exploration_time, exploitation_time = vns(initial_tour, dist_matrix, k_max=50, operator=two_opt)
    time_end = time.time()
    
    results.append({
        "Matrix": matrix_number,
        "Number of cities": len(dist_matrix),
        "Best tour by VNS": best_tour,
        "Total distance by VNS": tour_distance(best_tour, dist_matrix),
        "Optimal distance": optimal_solutions[matrix_number]["optimal_solution"],
        "Percentage far from the optimal solution": (tour_distance(best_tour, dist_matrix) - optimal_solutions[matrix_number]["optimal_solution"]) / optimal_solutions[matrix_number]["optimal_solution"] * 100,
        "Time of execution": time_end - time_start,
        "Exploration time": exploration_time,
        "Exploitation time": exploitation_time
    })
    counter += 1

print("Done!")
    
logs = {
    "Score": (100 - sum(result["Percentage far from the optimal solution"] for result in results) / len(results)) / 100,
    "Results": results
}

with open("logs/results.json", "w") as json_file:
    json.dump(logs, json_file, indent=4)
    
matrix_numbers = [result['Matrix'] for result in results]
percentage_far_from_optimal = [result['Percentage far from the optimal solution'] for result in results]

percentage_close_to_optimal = [100 - percentage for percentage in percentage_far_from_optimal]

plt.figure(figsize=(12, 8))
bars = plt.bar(matrix_numbers, percentage_close_to_optimal, color='lightgreen', label='VNS Solution Relative to Optimal')
plt.axhline(y=100, color='r', linestyle='--', label='Perfect match to Optimal (100%)')
plt.xlabel('Matrix Number')
plt.ylabel('Percentage Close to Optimal')
plt.title('Percentage Close to Optimal Solution for Each Test')
plt.legend()
plt.xticks(rotation=45)

for bar in bars:
    yval = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2, max(101, yval + 1), round(yval, 2), ha='center', va='bottom')

plt.tight_layout()
plt.savefig(f"logs/results.png")