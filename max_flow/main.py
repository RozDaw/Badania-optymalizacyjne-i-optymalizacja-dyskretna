import time
from collections import deque
import copy
import matplotlib
matplotlib.use('tkAgg')
import matplotlib.pyplot as plt

import random


# ============================================================
# GENEROWANIE GRAFU W FORMACIE TAKIM JAK W ZADANIU
# ============================================================
def generate_random_graph(n, max_capacity=20, density=0.3):
    """
    n – liczba wierzchołków
    max_capacity – maksymalna przepustowość na krawędzi
    density – prawdopodobieństwo istnienia krawędzi (0..1)
    """
    graph = [[0] * n for _ in range(n)]

    for i in range(n):
        for j in range(n):
            if i == j:
                continue  # brak pętli
            if random.random() < density:
                graph[i][j] = random.randint(1, max_capacity)
            else:
                graph[i][j] = 0

    return graph


# ============================================================
# ZAPIS GRAFU DO PLIKU
# ============================================================
def save_graph_to_file(filename, graph):
    n = len(graph)
    with open(filename, "w") as f:
        f.write(str(n) + "\n")
        for row in graph:
            f.write(" ".join(map(str, row)) + "\n")


# ============================================================
# WCZYTYWANIE GRAFU Z PLIKU
# ============================================================
def load_graph_from_file(filename):
    with open(filename, "r") as f:
        lines = f.read().strip().splitlines()

    n = int(lines[0].strip())
    graph = []
    for i in range(1, n + 1):
        row = list(map(int, lines[i].split()))
        graph.append(row)

    return graph

def bfs(capacity, flow, s, t, parent):
    n = len(capacity)
    visited = [False] * n
    queue = deque([s])
    visited[s] = True

    while queue:
        u = queue.popleft()
        for v in range(n):
            if not visited[v] and capacity[u][v] - flow[u][v] > 0:
                parent[v] = u
                visited[v] = True
                if v == t:
                    return True
                queue.append(v)
    return visited[t]


def edmonds_karp(capacity, s, t):
    n = len(capacity)
    flow = [[0] * n for _ in range(n)]
    parent = [-1] * n
    max_flow = 0

    while bfs(capacity, flow, s, t, parent):
        path_flow = float('inf')
        v = t
        while v != s:
            u = parent[v]
            path_flow = min(path_flow, capacity[u][v] - flow[u][v])
            v = u

        v = t
        while v != s:
            u = parent[v]
            flow[u][v] += path_flow
            flow[v][u] -= path_flow
            v = u

        max_flow += path_flow

    return max_flow, flow


# ============================================================
# 2️⃣  ALGORYTM DINICA (Dinic's Algorithm)
# ============================================================
def bfs_level_graph(cap, flow, s, t, level):
    n = len(cap)
    for i in range(n):
        level[i] = -1

    queue = deque([s])
    level[s] = 0

    while queue:
        u = queue.popleft()
        for v in range(n):
            if level[v] < 0 and cap[u][v] - flow[u][v] > 0:
                level[v] = level[u] + 1
                queue.append(v)

    return level[t] >= 0


def send_flow(u, t, f, cap, flow, level, next_edge):
    if u == t:
        return f

    n = len(cap)
    for v in range(next_edge[u], n):
        if level[v] == level[u] + 1 and cap[u][v] - flow[u][v] > 0:
            curr_flow = min(f, cap[u][v] - flow[u][v])
            temp = send_flow(v, t, curr_flow, cap, flow, level, next_edge)

            if temp > 0:
                flow[u][v] += temp
                flow[v][u] -= temp
                return temp

        next_edge[u] += 1

    return 0


def dinic(capacity, s, t):
    n = len(capacity)
    flow = [[0] * n for _ in range(n)]
    level = [-1] * n
    max_flow = 0

    while bfs_level_graph(capacity, flow, s, t, level):
        next_edge = [0] * n

        while True:
            pushed = send_flow(s, t, float('inf'), capacity, flow, level, next_edge)
            if pushed <= 0:
                break
            max_flow += pushed

    return max_flow, flow


# ============================================================
# 3️⃣  DEKOMPOZYCJA PRZEPŁYWU NA ŚCIEŻKI
# ============================================================
def decompose_flow(flow, s, t):
    n = len(flow)
    paths = []
    residual = copy.deepcopy(flow)

    while True:
        parent = [-1] * n
        visited = [False] * n
        stack = [s]
        visited[s] = True

        found = False
        while stack:
            u = stack.pop()
            if u == t:
                found = True
                break
            for v in range(n):
                if not visited[v] and residual[u][v] > 0:
                    visited[v] = True
                    parent[v] = u
                    stack.append(v)

        if not found:
            break

        v = t
        path = []
        min_f = float('inf')
        while v != s:
            u = parent[v]
            path.append(v)
            min_f = min(min_f, residual[u][v])
            v = u
        path.append(s)
        path.reverse()

        v = t
        while v != s:
            u = parent[v]
            residual[u][v] -= min_f
            v = u

        paths.append((min_f, path))

    return paths
# ============================================================
# 3️⃣  ALGORYTM FORDA–FULKERSONA (DFS)
# ============================================================

def dfs_ff(u, t, f, capacity, flow, visited):
    if u == t:
        return f

    visited[u] = True
    n = len(capacity)

    for v in range(n):
        if not visited[v] and capacity[u][v] - flow[u][v] > 0:
            curr_flow = min(f, capacity[u][v] - flow[u][v])
            temp = dfs_ff(v, t, curr_flow, capacity, flow, visited)
            if temp > 0:
                flow[u][v] += temp
                flow[v][u] -= temp
                return temp

    return 0


def ford_fulkerson(capacity, s, t):
    n = len(capacity)
    flow = [[0] * n for _ in range(n)]
    max_flow = 0

    while True:
        visited = [False] * n
        pushed = dfs_ff(s, t, float('inf'), capacity, flow, visited)
        if pushed == 0:
            break
        max_flow += pushed

    return max_flow, flow


sizes = [20, 40, 60, 80, 100, 120, ]   # możesz dodać więcej np. do 500
times_ek = []
times_dinic = []
times_ff = []
n=20
while n < 100:
    print(f"\nBadanie dla n = {n}...")

    g = generate_random_graph(n)

    # Edmonds–Karp
    start = time.time()
    edmonds_karp(g, 0, n - 1)
    times_ek.append(time.time() - start)

    # Dinic
    start = time.time()
    dinic(g, 0, n - 1)
    times_dinic.append(time.time() - start)

    # Ford–Fulkerson
    start = time.time()
    ford_fulkerson(g, 0, n - 1)
    times_ff.append(time.time() - start)
    n+=20

# ============================================================
# RYSOWANIE WYKRESU
# ============================================================

plt.figure(figsize=(10, 6))
plt.plot(sizes, times_ek, label="Edmonds–Karp")
plt.plot(sizes, times_dinic, label="Dinic")
plt.plot(sizes, times_ff, label="Ford–Fulkerson")

plt.xlabel("n (liczba wierzchołków)")
plt.ylabel("czas wykonania [s]")
plt.title("Porównanie algorytmów maksymalnego przepływu")
plt.legend()
plt.grid(True)
plt.show()
