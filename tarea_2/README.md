# Things to consider when developing an app

This is an experiment to benchmark 3 algos

The problem is about graphs. The goal is to found that every node is connected to at least two edges. Every edge has a cost. The goal is to minimize the cost of the edges.

## What did I need for this app?

### 1. Benchmark system

Params needed:

- **Algoritihms**: list of algorithms to test
- **Input sizes**: list of **n** number of nodes to test 
- **Repetitions**: number of repetitions to test
- **Output**: benchmark results
  - **cost** = cost of the edges
  - **time** = time to run the algorithm
  - **space** = space to run the algorithm
 
Outcomes needed:
- Cost
  - function to calculate the value ´evaluate_solution´
- Temporal Complexity
  - Package: ´´timeit´´
- Space Complexity
  - Package: ´´tracemalloc´´ or ´´memory_profiler´´


### 2. Algorithms

**Preconditions**

Prepare a function to generate a graph.
- Params:
  - **n**: number of nodes
  - **min_weight**: minimum weight of the edges
  - **max_weight**: maximum weight of the edges

With ´networkx´ library, we can generate full connected graphs to then apply the algorithms.

**Implement the following algorithms**

- Brute force
- Heuristic based in Kruskal algorithm
- Metaheuristic based in simulated annealing

**How to manage a graph to do algorithm operations?**

Use ´´networkx´´ library for this. This way I have the data structure to manage the graph and the algorithms to work with it.

Moreover, this library have **minimum spanning tree algorithm**, which is useful for the heuristic algorithm and the simulated annealing algorithm. This algorithm used Kruskal algorithm to find the minimum spanning tree.


### 3. Results Analysis

We need to compare the results of the algorithms.

We can use plots, dicts or df to show the results.

Libraries:
- ´´matplotlib´´
- ´´pandas´´
- ´´numpy´´
- ´´seaborn´´

The results to compare for each number of node input are:

- Solution cost 
- Solution reliability???
- Time Complexity
- Space Complexity

Because each algorithm run with 3 different input sized and each of that runs are repeated, we can calculate:

- Average
- Min
- Max


Of the results.


## Benchmark system

### Sample size calculation
To compute the ideal sample por each algorithm with a given input size, we need to calculate the number of repetitions to get a good sample.

#### Option size 1 - 90% confidence and 10% error
With 90% confidence and 10% error, we can calculate the sample size with the following formula:
- z = 1.645: z-score for 90% confidence
- e = 0.1  : error
- p = 0.5  : population proportion
- n        : sample size

n = (z^2 * p * (1-p)) / e^2

n = 67,6

#### Option size 2 - 80% confidence and 20% error
With 80% confidence and 20% error, we can calculate the sample size with the following formula:
- z = 1.282: z-score for 80% confidence
- e = 0.2  : error
- p = 0.5  : population proportion
- n        : sample size

n = (z^2 * p * (1-p)) / e^2

n = 10,3

**Other considerations**

In the next function, we are going to do the benchmark for each algorithm with the sample size calculated.

Output:
- time_response_variable    : it will be a resulto with the average, min and max time for each algorithm
- space_results   : it will be a resulto with the average, min and max space for each algorithm
- utility_response_variable : it will be the solution of the algorithm.

Having mean, min and max values, we can compare the versatility of the algorithms.

**Run the bench after setup**

We need to run the benchmark after the setup of the algorithms. This way we can compare the results of the algorithms.

**Objective**:

- Display the results of the benchmark setup.
  - As a table or plots

To accomplish this, we need to have a data object to save the results of 
benchmark_algorithm function. And we need to save that with each number of nodes.

For this we can use a **dataframe**:
- Columns:
  - algorithm_name
  - input_size
  - time_mean
  - time_min
  - time_max
  - space_mean
  - space_min
  - space_max
  - total_cost

Then, we can use this dataframe to plot the results or show tables.

Output:
- None, only display the results 