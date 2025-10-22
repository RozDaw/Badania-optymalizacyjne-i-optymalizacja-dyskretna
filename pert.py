import math
from collections import defaultdict, deque
from random import Random
import numpy as np

def parse_input_file(filename):
    with open(filename, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]
    N, M = map(int, lines[0].split())
    durations_raw = list(map(int, lines[1].split()))
    durations = []
    for i in range(N):
        mi = durations_raw[i * 3]
        mp = durations_raw[i * 3 + 1]
        ma = durations_raw[i * 3 + 2]
        expected = (mi + 4 * mp + ma) / 6
        variance = ((ma - mi) / 6) ** 2
        durations.append({'min': mi, 'prob': mp, 'max': ma, 'expected': expected, 'variance': variance})
    dependencies_raw = list(map(int, lines[2].split()))
    dependencies = []
    for i in range(M):
        a = dependencies_raw[i * 2] - 1
        b = dependencies_raw[i * 2 + 1] - 1
        dependencies.append((a, b))
    X, Y = map(float, lines[3].split())
    return N, M, durations, dependencies, X, Y

def topological_order(N, dependencies):
    adj = [[] for _ in range(N)]
    indegree = [0] * N
    for a, b in dependencies:
        adj[a].append(b)
        indegree[b] += 1
    dq = deque([i for i in range(N) if indegree[i] == 0])
    order = []
    while dq:
        u = dq.popleft()
        order.append(u)
        for v in adj[u]:
            indegree[v] -= 1
            if indegree[v] == 0:
                dq.append(v)
    return order, adj

def cpm_pert(N, durations, dependencies):
    order, adj = topological_order(N, dependencies)

    ES = [0.0] * N
    for _ in range(N):
        for u in order:
            for v in adj[u]:
                if ES[u] + durations[u]['expected'] > ES[v]:
                    ES[v] = ES[u] + durations[u]['expected']

    EF = [ES[i] + durations[i]['expected'] for i in range(N)]
    project_time = max(EF)
    end_task = max(range(N), key=lambda i: EF[i])

    LF = [project_time] * N
    for u in reversed(order):
        for v in adj[u]:
            if LF[v] - durations[v]['expected'] < LF[u]:
                LF[u] = LF[v] - durations[v]['expected']
    LS = [LF[i] - durations[i]['expected'] for i in range(N)]

    critical_path = []
    current = end_task
    prev = defaultdict(list)
    for a, b in dependencies:
        prev[b].append(a)
    while True:
        critical_path.append(current)
        found = False
        for p in prev[current]:
            if ES[p] + durations[p]['expected'] == ES[current]:
                current = p
                found = True
                break
        if not found:
            break
    critical_path.reverse()

    exp_length = 0.0
    variance = 0.0
    for idx in critical_path:
        exp_length += durations[idx]['expected']
        variance += durations[idx]['variance']
    stddev = math.sqrt(variance)

    return critical_path, exp_length, stddev, project_time, ES, EF, LS, LF

def probability_finish_in_time(exp_length, stddev, X):
    if stddev == 0:
        return 1.0 if X >= exp_length else 0.0
    z = (X - exp_length) / stddev
    p = 0.5 * (1 + math.erf(z / math.sqrt(2)))
    return p

def project_duration_for_probability(exp_length, stddev, Y):
    from math import sqrt
    try:
        from scipy.special import erfinv
        z = sqrt(2) * erfinv(2 * Y - 1)
        return exp_length + stddev * z
    except ImportError:
        return None

def generate_instance(filename, numInstances=10000):
    # N, M, durations, dependencies, X, Y = parse_input_file(filename)
    # for duration in durations:
    #     # duration['actual_value'] = np.random.normal(loc= duration['expected'], scale=math.sqrt(duration['variance']), size = numInstances)
    #     print(duration)
    N, M, durations, dependencies, X, Y = parse_input_file(filename)

    task_times = []
    for _ in durations :
        task_times.append([])
    for i in range(len(durations)):
        task_times[i] = np.random.normal(loc= durations[i]['expected'], scale=math.sqrt(durations[i]['variance']), size = numInstances)

    instances = []
    for j in range(len(task_times[0])):
        for i in range(len(task_times)):
            instances.append((i, task_times[i][j]))







def main():
    filename = "data2.txt"
    N, M, durations, dependencies, X, Y = parse_input_file(filename)

    critical_path, exp_length, stddev, project_time, ES, EF, LS, LF = cpm_pert(N, durations, dependencies)
    print(f"Ścieżka krytyczna: {len(critical_path)}:", ' '.join(str(i + 1) for i in critical_path))
    print(f"Przewidywany czas: {exp_length:.2f} {stddev:.2f}")
    mode = int(input("Wybierz tryb (0 - czas X, 1 - prawdopodobieństwo Y): "))
    if mode == 0:
        X = float(input("Podaj czas ukończenia X: "))
        p = probability_finish_in_time(exp_length, stddev, X)
        print(f"Prawdopodobieństwo ukończenia w czasie {X:.2f} to {p:.4f} %")
    else:
        Y = float(input("Podaj prawdopodobieństwo Y: "))
        duration_Y = project_duration_for_probability(exp_length, stddev, Y / 100)
        print(f"Czas ukończenia z prawdopodobieństwem {Y:.4f}% to {duration_Y:.2f}")



if __name__ == "__main__":
    # main()
    filename = "data2.txt"
    generate_instance(filename)