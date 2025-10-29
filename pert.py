import math
from collections import defaultdict, deque
from random import Random
import numpy as np
from belman_ford import *

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

def generate_instance(filename, N=10, M=10 ):
    # N, M, dur, dep, X, Y = parse_input_file(filename)
    time = 5
    probability = 50
    rand = Random()

    durations = []
    dependencies = []
    for _ in range(N):
        prob = rand.randint(1,9)
        higher = rand.randint(1,9)
        lower = rand.randint(1,9)
        #sort prob, higher, lower
        if lower > prob:
            lower, prob = prob, lower
        if lower > higher:
            lower, higher = higher, lower
        if prob > higher:
            prob, higher = higher, prob
        durations.append((lower,prob,higher))

    for _ in range(M): # generate edges without repetitions
        a = rand.randint(1,N)
        b = rand.randint(1,N)
        while a == b or (a,b) in dependencies:
            a = rand.randint(1,N)
            b = rand.randint(1,N)
        if a > b:
            a, b = b, a
        dependencies.append((a,b))

    with open("gen"+filename, "w") as f:
        f.write(f"{N} {M}\n")
        for d in durations:
            f.write(f"{d[0]} {d[1]} {d[2]}   ")
        f.write("\n")
        for dep in dependencies:
            f.write(f"{dep[0]} {dep[1]}   ")
        f.write(f"\n{time} {probability}\n")

def get_random_instance(durations):
    times = []
    for dur in durations:
        times.append(np.random.normal(loc= dur['expected'], scale=math.sqrt(dur['variance'])))
    return times

def main(filename):
    N, M, durations, dependencies, time, probability = parse_input_file(filename)

    critical_path, exp_length, stddev, project_time, ES, EF, LS, LF = cpm_pert(N, durations, dependencies)
    print(f"Ścieżka krytyczna: {len(critical_path)}:", ' '.join(str(i + 1) for i in critical_path))
    print(f"Przewidywany czas: {exp_length:.2f} {stddev:.2f}")
    mode = int(input("Wybierz tryb (0 - czas X, 1 - prawdopodobieństwo Y): "))
    if mode == 0:
        time = float(input("Podaj czas ukończenia X: "))
        p = probability_finish_in_time(exp_length, stddev, time)
        print(f"Prawdopodobieństwo ukończenia w czasie {time:.2f} to {p:.4f} %")
    else:
        probability = float(input("Podaj prawdopodobieństwo Y: "))
        duration_Y = project_duration_for_probability(exp_length, stddev, probability / 100)
        print(f"Czas ukończenia z prawdopodobieństwem {probability:.4f}% to {duration_Y:.2f}")



if __name__ == "__main__":
    filename = "data2.txt"
    # generate_instance(filename,10,10)
    # filename = "gendata2.txt"
    main(filename)
    N, M, durations, dependencies, X, Y = parse_input_file("data2.txt")



    belman_times = []
    for _ in range(10000):
        times = get_random_instance(durations)
        x,y,z = belman_ford_run(N, M, times, dependencies)
        belman_times.append(z)
    # narysuj z tego histogram
    import matplotlib
    matplotlib.use('TkAgg')
    import matplotlib.pyplot as plt
    plt.hist(belman_times, bins=30, alpha=0.7, color='blue')
    plt.show()

