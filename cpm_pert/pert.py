import math
import time
from collections import defaultdict, deque
from random import Random
import numpy as np
from belman_ford import *
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
from scipy.special import erfinv

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
    # for _ in range(N):
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
    # current = end_task
    # prev = defaultdict(list)
    # for a, b in dependencies:
    #     prev[b].append(a)
    # while True:
    #     critical_path.append(current)
    #     found = False
    #     for p in prev[current]:
    #         if ES[p] + durations[p]['expected'] == ES[current]:
    #             current = p
    #             found = True
    #             break
    #     if not found:
    #         break
    # critical_path.reverse()
    #
    exp_length = 0.0
    variance = 0.0
    # for idx in critical_path:
    #     exp_length += durations[idx]['expected']
    #     variance += durations[idx]['variance']
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
        z = sqrt(2) * erfinv(2 * Y - 1)
        return exp_length + stddev * z
    except ImportError:
        print("Scipy is required for this function.")
        return None


def generate_instance(filename, N=10, M=10):
    # N, M, dur, dep, X, Y = parse_input_file(filename)
    time = 5
    probability = 50
    rand = Random()

    durations = []
    dependencies = []
    for _ in range(N):
        prob = rand.randint(1, 9)
        higher = rand.randint(1, 9)
        lower = rand.randint(1, 9)
        #sort prob, higher, lower
        if lower > prob:
            lower, prob = prob, lower
        if lower > higher:
            lower, higher = higher, lower
        if prob > higher:
            prob, higher = higher, prob
        if prob == higher:
            higher+=1
        durations.append((lower, prob, higher))

    for _ in range(M):
        a = rand.randint(1, N)
        b = rand.randint(1, N)
        while a == b or (a, b) in dependencies:
            a = rand.randint(1, N)
            b = rand.randint(1, N)
        if a > b:
            a, b = b, a
        dependencies.append((a, b))

    with open("data\\gen" + filename, "w") as f:
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
        times.append(np.random.triangular(left=dur['min'], mode=dur['prob'], right=dur['max']))
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

def time_measure(number_of_repetition = 1000, bf_only_n = False, bf_only_m = False, pert_only_n = False, pert_only_m = False):
    N = [10, 100, 1000, 10000, 20000, 30000,40000,50000,60000,70000,80000,90000, 100000]
    M = [1000, 10000, 20000, 30000,40000,50000,60000,70000,80000,90000, 100000]
    results_bf_only_n = []
    results_bf_only_m = []
    results_pert_only_n = []
    results_pert_only_m = []
    if bf_only_n or pert_only_n:
        for n in N: # belmann - ford
            nn, M, durations, dependencies, X, Y = parse_input_file(f"data\\gen_n_{n}.txt")
            end_time = 0
            if bf_only_n:
                times = get_random_instance(durations)
                for _ in range(number_of_repetition):
                    start_time = time.time()
                    belman_ford_run(nn,M, times, dependencies)
                    end_time += time.time()-start_time
                results_bf_only_n.append((n,end_time))
            if pert_only_n:
                for _ in range(number_of_repetition):
                    start_time = time.time()
                    cpm_pert(nn, durations, dependencies)
                    end_time += time.time() - start_time
                results_pert_only_n.append((n, end_time))

    if bf_only_m or pert_only_m:
        n = 1000
        for m in M:
            nn, mm, durations, dependencies, X, Y = parse_input_file(f"data\\gen_n_{n}_m_{m}.txt")
            end_time = 0
            if bf_only_m:
                times = get_random_instance(durations)
                for _ in range(number_of_repetition):
                    start_time = time.time()
                    belman_ford_run(nn, mm, times, dependencies)
                    end_time += time.time() - start_time
                results_bf_only_m.append((m,end_time))
            if pert_only_m:
                for _ in range(number_of_repetition):
                    start_time = time.time()
                    cpm_pert(nn, durations, dependencies)
                    end_time += time.time() - start_time
                results_pert_only_m.append((m, end_time))

    if bf_only_n:
        return results_bf_only_n
    if bf_only_m:
        return results_bf_only_m
    if pert_only_n:
        return results_pert_only_n
    if pert_only_m:
        return results_pert_only_m

def create_latex_chart(filename,caption,label, y_label, x_label, data, legend_entry):
    if data.__len__() != legend_entry.__len__():
        print("Długość danych i legendy muszą być takie same")
        return
    with open(filename, "w") as f:
        f.write("\\begin{figure}[H]\n")
        f.write("\\centering\n")
        f.write("\\begin{tikzpicture}\n")
        f.write("\\begin{axis}[\n")
        f.write(f"xlabel = {{{x_label}}},\n")
        f.write(f"ylabel = {{{y_label}}},\n")
        f.write("legend pos = north west,\n")
        f.write("grid = both,\n")
        f.write("width=0.7\\linewidth,\n")
        f.write("]\n")
        for i in range(data.__len__()):
            f.write("\\addplot + [mark = *, thick] coordinates\n")
            f.write("    {\n")
            for e in data[i]:
                f.write(f"{e}")
            f.write("};\n")
            f.write("\\addlegendentry\n")
            f.write(f"{{{legend_entry[i]}}}\n")
        f.write("\\end{axis}\n")
        f.write("\\end{tikzpicture}\n")
        f.write(f"\\caption\n{{{caption}}}\n")
        f.write(f"\\label{{{label}}}\n")
        f.write("\\end{figure}\n")

if __name__ == "__main__":
    # filename = "data\\data2.txt"
    # N, M, durations, dependencies, X, Y = parse_input_file(filename)
    # #
    # belman_times = []
    # for _ in range(1000000):
    #     times = get_random_instance(durations)
    #     x, y, z = belman_ford_run(N, M, times, dependencies)
    #     belman_times.append(z)
    #
    # # histogram
    #
    # plt.hist(belman_times, bins=30, alpha=0.7, color='blue')
    # mu = sum(belman_times) / len(belman_times)
    # sigma = math.sqrt(sum((x - mu) ** 2 for x in belman_times) / len(belman_times))
    # xmin, xmax = plt.xlim()
    # x = np.linspace(xmin, xmax, 100)
    # p = (1 / (sigma * np.sqrt(2 * np.pi))) * np.exp(-0.5 * ((x - mu) / sigma) ** 2)
    # plt.plot(x, p * len(belman_times) * (xmax - xmin) / 30, 'k', linewidth=2)
    # plt.title('Histogram czasów trwania projektu')
    #
    # plt.show()


    number_of_repetition = 100
    results_bf_only_n = time_measure(number_of_repetition, bf_only_n=True)
    print("BF only n:", results_bf_only_n)

    results_pert_only_n = time_measure(number_of_repetition,pert_only_n=True)
    print("Pert only n:", results_pert_only_n)

    results = [results_bf_only_n, results_pert_only_n]
    legend = ["Belman-Ford varying N", "PERT varying N"]
    filename = "time_measurements_n_x.tex"
    caption = "Porównanie czasów wykonania algorytmów Belman-Ford i PERT w zależności od liczby wierzchołków N"
    label = "fig:time_measurements_n"
    y_label = "Czas wykonania [s]"
    x_label = "Liczba wierzcholkow N"
    create_latex_chart(filename, caption, label, y_label, x_label, results, legend)

    results_bf_only_m = time_measure(number_of_repetition, bf_only_m=True)
    print("BF only m:", results_bf_only_m)
    results_pert_only_m = time_measure(number_of_repetition, pert_only_m=True)
    print("Pert only m:", results_pert_only_m)

    results = [results_bf_only_m, results_pert_only_m]
    legend = ["Belman-Ford varying M", "PERT varying M"]
    filename = "time_measurements_m_x.tex"
    caption = "Porównanie czasów wykonania algorytmów Belman-Ford i PERT przy stałym N=1000 i różnej liczbie krawędzi M"
    label = "fig:time_measurements_m"
    y_label = "Czas wykonania [s]"
    x_label = "Liczba krawędzi M"
    create_latex_chart(filename, caption, label, y_label, x_label, results, legend)
