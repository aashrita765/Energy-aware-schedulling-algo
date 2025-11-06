# import random
# import matplotlib.pyplot as plt

# # -----------------------------
# # Task Generator
# # -----------------------------
# def generate_tasks(n):
#     tasks = []
#     for i in range(n):
#         arrival = random.randint(0, 10)
#         burst = random.randint(1, 10)
#         priority = random.randint(1, 5)
#         energy = burst * random.uniform(0.8, 1.5)
#         tasks.append({"id": i, "arrival": arrival, "burst": burst, 
#                       "priority": priority, "energy": energy})
#     return tasks

# # -----------------------------
# # Scheduling Algorithms
# # -----------------------------
# def fcfs(tasks):
#     tasks = sorted(tasks, key=lambda x: x["arrival"])
#     time, waiting, turnaround, energy_used = 0, 0, 0, 0
#     for t in tasks:
#         if time < t["arrival"]: time = t["arrival"]
#         waiting += time - t["arrival"]
#         time += t["burst"]
#         turnaround += time - t["arrival"]
#         energy_used += t["energy"]
#     return waiting/len(tasks), turnaround/len(tasks), len(tasks)/time, energy_used

# def round_robin(tasks, quantum=4):
#     queue = []
#     tasks = sorted(tasks, key=lambda x: x["arrival"])
#     time, idx = 0, 0
#     waiting, turnaround, energy_used = 0, 0, 0
#     remaining = {t["id"]: t["burst"] for t in tasks}
#     arrival_map = {t["id"]: t["arrival"] for t in tasks}
#     done = {}

#     while len(done) < len(tasks):
#         while idx < len(tasks) and tasks[idx]["arrival"] <= time:
#             queue.append(tasks[idx]["id"])
#             idx += 1
#         if not queue:
#             time += 1
#             continue
#         tid = queue.pop(0)
#         burst_left = remaining[tid]
#         exec_time = min(quantum, burst_left)
#         time += exec_time
#         remaining[tid] -= exec_time
#         if remaining[tid] == 0:
#             turnaround += time - arrival_map[tid]
#             waiting += turnaround - (tasks[tid]["burst"])
#             done[tid] = True
#             energy_used += tasks[tid]["energy"]
#         else:
#             queue.append(tid)
#     return waiting/len(tasks), turnaround/len(tasks), len(tasks)/time, energy_used

# def priority_scheduling(tasks):
#     tasks = sorted(tasks, key=lambda x: (x["arrival"], x["priority"]))
#     time, waiting, turnaround, energy_used = 0, 0, 0, 0
#     for t in tasks:
#         if time < t["arrival"]: time = t["arrival"]
#         waiting += time - t["arrival"]
#         time += t["burst"]
#         turnaround += time - t["arrival"]
#         energy_used += t["energy"]
#     return waiting/len(tasks), turnaround/len(tasks), len(tasks)/time, energy_used

# def energy_aware(tasks):
#     tasks = sorted(tasks, key=lambda x: (x["arrival"], x["energy"]))
#     time, waiting, turnaround, energy_used = 0, 0, 0, 0
#     for t in tasks:
#         if time < t["arrival"]: time = t["arrival"]
#         waiting += time - t["arrival"]
#         time += t["burst"]
#         turnaround += time - t["arrival"]
#         energy_used += t["energy"] * 0.8  # assume ~20% energy saving
#     return waiting/len(tasks), turnaround/len(tasks), len(tasks)/time, energy_used

# # -----------------------------
# # Experiment Runner
# # -----------------------------
# def run_experiment(task_sizes=[10,30,50,100]):
#     algos = {"FCFS": fcfs, "RR": round_robin, 
#              "Priority": priority_scheduling, "EnergyAware": energy_aware}
#     results = {a: {"waiting": [], "turnaround": [], "throughput": [], "energy": []} for a in algos}

#     for n in task_sizes:
#         print(f"\n--- Metrics for {n} tasks ---")
#         tasks = generate_tasks(n)
#         for name, func in algos.items():
#             w,t,tr,e = func(tasks)
#             results[name]["waiting"].append(w)
#             results[name]["turnaround"].append(t)
#             results[name]["throughput"].append(tr)
#             results[name]["energy"].append(e)
#             print(f"{name}: Waiting={w:.2f}, Turnaround={t:.2f}, Throughput={tr:.2f}, Energy={e:.2f}")

#     # Plot metrics
#     for metric in ["waiting", "turnaround", "throughput", "energy"]:
#         plt.figure(figsize=(7,5))
#         for name in algos:
#             plt.plot(task_sizes, results[name][metric], marker='o', label=name)
#         plt.title(f"{metric.capitalize()} vs Number of Tasks")
#         plt.xlabel("Number of Tasks")
#         plt.ylabel(metric.capitalize())
#         plt.legend()
#         plt.grid(True)
#         plt.show()

# # Run experiment
# run_experiment()


import random
import heapq
import matplotlib.pyplot as plt
import numpy as np

# --------------------------------
# Task Generator
# --------------------------------
def generate_tasks(n):
    tasks = []
    for i in range(n):
        arrival = random.randint(0, 10)
        burst = random.randint(1, 10)
        priority = random.randint(1, 5)
        energy = burst * random.uniform(0.8, 1.5)
        tasks.append({"id": i, "arrival": arrival, "burst": burst,
                      "priority": priority, "energy": energy})
    return tasks


# --------------------------------
# Scheduling Algorithms
# --------------------------------
def fcfs(tasks):
    tasks = sorted(tasks, key=lambda x: x["arrival"])
    time, waiting, turnaround, energy_used = 0, 0, 0, 0

    for t in tasks:
        if time < t["arrival"]:
            time = t["arrival"]
        waiting += time - t["arrival"]
        time += t["burst"]
        turnaround += time - t["arrival"]
        energy_used += t["energy"]

    n = len(tasks)
    return waiting/n, turnaround/n, n/time, energy_used


def round_robin(tasks, quantum=4, context_switch=0.0):
    tasks = sorted(tasks, key=lambda x: x["arrival"])
    n = len(tasks)
    time = 0
    idx = 0
    queue = []
    remaining = {t["id"]: t["burst"] for t in tasks}
    arrivals = {t["id"]: t["arrival"] for t in tasks}
    bursts = {t["id"]: t["burst"] for t in tasks}
    energies = {t["id"]: t["energy"] for t in tasks}
    completion = {}

    while len(completion) < n:
        while idx < n and tasks[idx]["arrival"] <= time:
            queue.append(tasks[idx]["id"])
            idx += 1

        if not queue:
            if idx < n:
                time = max(time, tasks[idx]["arrival"])
            continue

        tid = queue.pop(0)
        exec_time = min(quantum, remaining[tid])
        time += exec_time
        remaining[tid] -= exec_time

        # Add new arrivals during execution
        while idx < n and tasks[idx]["arrival"] <= time:
            queue.append(tasks[idx]["id"])
            idx += 1

        if remaining[tid] == 0:
            completion[tid] = time
        else:
            queue.append(tid)
        time += context_switch  # Add context switch delay

    waiting_times = [completion[i] - arrivals[i] - bursts[i] for i in range(n)]
    turnaround_times = [completion[i] - arrivals[i] for i in range(n)]
    energy_used = sum(energies.values())

    return np.mean(waiting_times), np.mean(turnaround_times), n/time, energy_used


def priority_scheduling(tasks):
    tasks = sorted(tasks, key=lambda x: x["arrival"])
    n = len(tasks)
    time = 0
    idx = 0
    ready_queue = []
    completion = {}

    while len(completion) < n:
        # Add tasks that have arrived
        while idx < n and tasks[idx]["arrival"] <= time:
            heapq.heappush(ready_queue, (tasks[idx]["priority"], tasks[idx]["id"], tasks[idx]))
            idx += 1

        if not ready_queue:
            if idx < n:
                time = max(time, tasks[idx]["arrival"])
            continue

        _, _, t = heapq.heappop(ready_queue)
        if time < t["arrival"]:
            time = t["arrival"]
        time += t["burst"]
        completion[t["id"]] = time
    
    by_id = {t["id"]: t for t in tasks}
    waiting_times = [completion[i] - by_id[i]["arrival"] - by_id[i]["burst"] for i in range(n)]
    turnaround_times = [completion[i] - by_id[i]["arrival"] for i in range(n)]


    # waiting_times = [completion[i] - tasks[i]["arrival"] - tasks[i]["burst"] for i in range(n)]
    # turnaround_times = [completion[i] - tasks[i]["arrival"] for i in range(n)]
    energy_used = sum(t["energy"] for t in tasks)

    return np.mean(waiting_times), np.mean(turnaround_times), n/time, energy_used


def energy_aware(tasks):
    tasks = sorted(tasks, key=lambda x: (x["arrival"], x["energy"]))
    time, waiting, turnaround, energy_used = 0, 0, 0, 0

    for t in tasks:
        if time < t["arrival"]:
            time = t["arrival"]
        waiting += time - t["arrival"]
        time += t["burst"]
        turnaround += time - t["arrival"]
        energy_used += t["energy"] * 0.8  # ~20% energy saving

    n = len(tasks)
    return waiting/n, turnaround/n, n/time, energy_used


# --------------------------------
# Experiment Runner
# --------------------------------
def run_experiment(task_sizes=[10, 30, 50, 100], trials=10):
    random.seed(42)
    algos = {
        "FCFS": fcfs,
        "RoundRobin": round_robin,
        "Priority": priority_scheduling,
        "EnergyAware": energy_aware,
    }

    results = {a: {"waiting": [], "turnaround": [], "throughput": [], "energy": []}
               for a in algos}

    for n in task_sizes:
        print(f"\n--- Averaged Metrics for {n} Tasks (over {trials} runs) ---")
        for name, func in algos.items():
            w_list, t_list, tr_list, e_list = [], [], [], []
            for _ in range(trials):
                tasks = generate_tasks(n)
                w, t, tr, e = func(tasks)
                w_list.append(w)
                t_list.append(t)
                tr_list.append(tr)
                e_list.append(e)
            results[name]["waiting"].append(np.mean(w_list))
            results[name]["turnaround"].append(np.mean(t_list))
            results[name]["throughput"].append(np.mean(tr_list))
            results[name]["energy"].append(np.mean(e_list))
            print(f"{name:<12}: W={np.mean(w_list):.2f}, TAT={np.mean(t_list):.2f}, "
                  f"TH={np.mean(tr_list):.3f}, Energy={np.mean(e_list):.2f}")

    # Plot results
    for metric in ["waiting", "turnaround", "throughput", "energy"]:
        plt.figure(figsize=(7, 5))
        for name in algos:
            plt.plot(task_sizes, results[name][metric], marker='o', label=name)
        plt.title(f"{metric.capitalize()} vs Number of Tasks")
        plt.xlabel("Number of Tasks")
        plt.ylabel(metric.capitalize())
        plt.legend()
        plt.grid(True)
        plt.show()


# --------------------------------
# Run Simulation
# --------------------------------
run_experiment()
