
# Variable Neighborhood Search (VNS) for Traveling Salesman Problem

This repository provides an implementation of the Variable Neighborhood Search (VNS) algorithm to solve the Traveling Salesman Problem (TSP) using 2-opt and 3-opt techniques. 

## Requirements

- Python 3
- numpy

## Features

1. **Local Search**: Uses 2-opt or 3-opt technique to find a better tour by locally optimizing the given tour.
2. **Shaking**: Perturbs the given tour `k` times using 2-opt technique to explore different neighborhoods.
3. **VNS Algorithm**: Main algorithm that alternates between the shaking and local search steps.
4. **Benchmark Testing**: Loads the benchmark dataset from `benchmark_dataset/optimal_solutions.json` and evaluates the VNS algorithm's performance on them.

## Usage

1. Ensure the benchmark dataset files (`.txt` format) are present in the `benchmark_dataset` directory.
2. Make sure that `optimal_solutions.json` contains the optimal solutions for the respective TSP instances.
3. Run the main script to execute the VNS algorithm on the benchmark dataset. The results will be printed to the console and also saved in `logs/results.json`.

```bash
python vns_tsp.py
```


## Structure

1. **tour_distance**: Computes the distance of the given tour using the distance matrix.
2. **two_opt**: Reverses the order of cities between indices `i` and `j`.
3. **three_opt**: Applies the 3-opt technique between indices `i`, `j`, and `k`.
4. **local_search**: Continuously optimizes the tour until no better solutions can be found in the neighborhood.
5. **shaking**: Performs `k` random 2-opt perturbations on the tour.
6. **vns**: Main VNS algorithm that alternates between shaking and local search.

## Output

After running the script, the following metrics are provided for each test:

- Test number
- Number of cities
- Total distance obtained using VNS
- Optimal distance (from benchmark)
- Score (calculated based on how close the obtained solution is to the optimal one)
- Time of execution
- Exploration time (time spent in shaking phase)
- Exploitation time (time spent in local search phase)

Finally, the average score across all tests is also printed.

## Contributions

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.
