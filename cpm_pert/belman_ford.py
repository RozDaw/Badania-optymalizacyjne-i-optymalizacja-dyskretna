from random import Random


class Task:
    def __init__(self, id, duration):
        self.id = id
        self.duration = duration
        self.earliest_start = 0
        self.latest_start = float('inf')
        self.earliest_finish = duration
        self.latest_finish = float('inf')

def create_data_file(N = 10, M = 10):
    durations = []
    rand = Random()
    for _ in range(N):
        durations.append(rand.randint(1, 100))
    dependencies = []
    for _ in range(M):
        u = rand.randint(1, N)
        v = rand.randint(1, N)
        while v == u or (u, v) in dependencies:
            v = rand.randint(1, N)
        dependencies.append((u, v))

    with open(f"g_data_{N}_{M}.txt", "w") as f:
        f.write(f"{N} {M}\n")
        f.write(" ".join(map(str, durations)) + "\n")
        dep_strings = ["{} {}".format(u, v) for u, v in dependencies]
        f.write("  ".join(dep_strings) + "\n")

def load_data():
    with open("data.txt") as f:
        N, M = map(int, f.readline().strip().split())
        durations = list(map(int, f.readline().strip().split()))
        dependencies_line = f.readline().strip()
        dependencies = [
          tuple(map(int, pair.split()))
          for pair in dependencies_line.split("  ")  # Rozdzielanie po dwóch spacjach
        ]


    adj = [[] for _ in range(N)]
    indegree = [0] * N
    for u, v in dependencies:
        u -= 1
        v -= 1
        adj[u].append(v)
        indegree[v] += 1

    return N, M, durations, dependencies, adj, indegree



def cpm_with_path(N, durations, dependencies):
    ES = [0] * N
    from collections import defaultdict
    prev = defaultdict(list)
    for a, b in dependencies:
        a_idx = a - 1
        b_idx = b - 1
        prev[b_idx].append(a_idx)

    # Najwcześniejsze rozpoczęcia
    for _ in range(N - 1):
        change = False
        for a, b in dependencies:
            a_idx = a - 1
            b_idx = b - 1
            if ES[a_idx] + durations[a_idx] > ES[b_idx]:
                ES[b_idx] = ES[a_idx] + durations[a_idx]
                change = True
        if change:
            break

    end_task = max(range(N), key=lambda i: ES[i] + durations[i])
    project_end = ES[end_task] + durations[end_task]

    path = []
    current = end_task
    while True:
        path.append(current + 1)
        found = False
        for p in prev[current]:
            if ES[p] + durations[p] == ES[current]:
                current = p
                found = True
                break
        if not found:
            break
    path.reverse()

    return ES, path, project_end

def belman_ford_run(N,M, durations, dependencies):
    ES, critical_path, project_end = cpm_with_path(N, durations, dependencies)
    # print("Najwcześniejsze rozpoczęcia:", ES)
    # print("Ścieżka krytyczna:", critical_path)
    # print("Czas trwania projektu:", project_end)
    return ES, critical_path, project_end