⚙️ Energy-Aware CPU Scheduling Simulator — Summary Points

Objective:
Designed a Python-based simulator to analyze and compare multiple CPU scheduling algorithms — FCFS, Round Robin, Priority Scheduling, and an Energy-Aware variant — in terms of efficiency and energy consumption.

Motivation:
Traditional schedulers optimize for speed but ignore power; this project introduces energy awareness to balance performance and energy efficiency, a key concern in modern mobile and data-center systems.

Task Model:
Each simulated process (task) includes arrival time, burst time, priority, and a calculated energy cost proportional to its workload.

Algorithms Implemented:

FCFS: Non-preemptive, executes tasks in order of arrival.

Round Robin: Time-sharing with fixed quantum for fairness.

Priority Scheduling: Chooses task with the highest priority.

Energy-Aware Scheduling: Prioritizes tasks with lower energy demands to minimize overall power usage.

Metrics Computed:

Average waiting time

Average turnaround time

Throughput (tasks completed per unit time)

Total energy consumption

Energy Model:
Each task’s base energy = burst × random(0.8–1.5); in the Energy-Aware algorithm, a 0.8 multiplier (≈ 20 % saving) models reduced voltage/frequency operation (DVFS-like behavior).

Simulation Logic:
Simulates CPU “time” progression, handles task arrivals dynamically, and records per-task waiting and completion times for accuracy.

Use of Data Structures:

Lists for FCFS and RR queues.

Python heapq priority queue for efficient priority selection.

Dictionaries for constant-time task lookup by ID.

Experiment Design:
Runs repeated trials for varying task counts (10 – 100 tasks) to average out randomness, ensuring statistically reliable comparisons.

Visualization:
Generates line plots (Matplotlib) showing each metric vs. number of tasks — clearly revealing performance-energy trade-offs.

Results & Insights:

Round Robin improves fairness but increases context-switch overhead.

Priority scheduling favors high-priority tasks but risks starvation.

Energy-Aware scheduling consistently reduces total energy (~20 %) with minimal loss in throughput.

Energy Saving Mechanism:
By running low-energy tasks first and simulating DVFS scaling, the scheduler keeps the CPU in low-power states longer, reducing active power draw.

Complexity:
Most algorithms run in O(n log n) due to sorting/heap operations, with Round Robin slightly higher because of multiple time slices.

Limitations:
Simplified static energy model (fixed 0.8 factor), single-core system, and no modeling of idle or context-switch energy.

Future Enhancements:

Implement dynamic DVFS model with real-time frequency scaling.

Add multi-core scheduling and preemptive energy-aware variants.

Include Gantt-chart visualization and detailed per-task energy tracking.
