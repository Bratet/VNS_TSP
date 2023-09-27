import random
import time
import json
import os
import numpy as np

def tour_distance(tour, dist_matrix):
    tour_shifted = np.roll(tour, -1)
    return np.sum(dist_matrix[tour, tour_shifted])

def two_opt(tour, i, j):
    new_tour = np.concatenate((tour[:i], tour[i:j+1][::-1], tour[j+1:]))
    return new_tour

def three_opt(tour, i, j, k):
    new_tour = np.concatenate((tour[:i], tour[j:k], tour[i:j], tour[k:]))
    return new_tour

def local_search(tour, dist_matrix, operator):
    better_solution_found = True
    original_distance = tour_distance(tour, dist_matrix)
    
    while better_solution_found:
        better_solution_found = False
        for i in range(1, len(tour) - 1):
            for j in range(i+1, len(tour)):
                if j-i == 1: continue
                new_tour = operator(tour, i, j)
                new_distance = tour_distance(new_tour, dist_matrix)
                if new_distance < original_distance:
                    tour = new_tour
                    original_distance = new_distance
                    better_solution_found = True
                    
    return tour

def shaking(tour, k):
    new_tour = tour.copy()
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
        dist_matrix = np.array([list(map(float, line.split())) for line in lines])

    initial_tour = random.sample(range(len(dist_matrix)), len(dist_matrix))
    time_start = time.time()
    best_tour, exploration_time, exploitation_time = vns(initial_tour, dist_matrix, k_max=50, operator=two_opt)
    time_end = time.time()
    
    results.append({
        "Test": matrix_number,
        "Number of cities": len(dist_matrix),
        "Total distance by VNS": tour_distance(best_tour, dist_matrix),
        "Optimal distance": optimal_solutions[matrix_number]["optimal_solution"],
        "Score": (optimal_solutions[matrix_number]["optimal_solution"] / tour_distance(best_tour, dist_matrix)) * 100,
        "Time of execution": time_end - time_start,
        "Exploration time": exploration_time,
        "Exploitation time": exploitation_time
    })
    counter += 1

print("Done!")
    
logs = {
    "Average score": np.mean([result["Score"] for result in results]),
    "Results": results
}

with open("logs/results.json", "w") as json_file:
    json.dump(logs, json_file, indent=4)