import heapq
import math
import time


def load_data(file_name):
    with open(file_name, 'r') as file:
        cols, rows = map(int, file.readline().split())
        grid = [list(map(int, file.readline().split())) for _ in range(rows)]
    return rows, cols, grid

def generate_random_data(rows,cols):
    N = cols
    M = rows
    import random
    grid = []
    start_index = (random.randint(0, N-1), random.randint(0, M-1))
    end_index = (random.randint(0, N-1), random.randint(0, M-1))
    for i in range(N):
        row = []
        for j in range(M):
            if (i == start_index[0] and j == start_index[1]):
                row.append(2)  # Start
            elif (i == end_index[0] and j == end_index[1]):
                row.append(3)  # End
            else:
                cell = random.choices([0, 1], weights=[0.7, 0.3])[0]  # 70% free, 30% wall
                row.append(cell)
        grid.append(row)
    filename = f"generated_data_{N}-{M}.txt"
    with open(filename, 'w') as file:
        file.write(f"{M} {N}\n")
        for row in grid:
            file.write(' '.join(map(str, row)) + '\n')
    return rows, cols, grid

def build_graph(rows, cols, grid):
    graph = {}
    start = None
    end = None
    for i in range(rows):
        for j in range(cols):
            if grid[i][j] == 2:
                start = (i, j)
            elif grid[i][j] == 3:
                end = (i, j)
            if grid[i][j] != 1:  # Skip walls
                neighbors = []
                for di, dj in [(-1, 0), (1, 0), (0, -1), (0, 1)]:  # Up, Down, Left, Right
                    ni, nj = i + di, j + dj
                    if 0 <= ni < rows and 0 <= nj < cols:  # Ensure indices are within bounds
                        if grid[ni][nj] != 1:  # Check if the neighbor is not a wall
                            neighbors.append(((ni, nj), 1))  # Weight is 1
                graph[(i, j)] = neighbors
    return graph, start, end


def bellman_ford(graph, start, end):
    distances = {node: math.inf for node in graph}
    distances[start] = 0

    for _ in range(len(graph) - 1):
        for node in graph:
            for neighbor, weight in graph[node]:
                if distances[node] + weight < distances[neighbor]:
                    distances[neighbor] = distances[node] + weight

    # Check for negative weight cycles
    for node in graph:
        for neighbor, weight in graph[node]:
            if distances[node] + weight < distances[neighbor]:
                raise ValueError("Graph contains a negative weight cycle")

    return distances[end]

def dijkstra(graph, start, end):
    pq = [(0, start)]  # (distance, node)
    distances = {node: math.inf for node in graph}
    distances[start] = 0
    visited = set()

    while pq:
        current_distance, current_node = heapq.heappop(pq)
        if current_node in visited:
            continue
        visited.add(current_node)

        if current_node == end:
            return current_distance

        for neighbor, weight in graph[current_node]:
            distance = current_distance + weight
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                heapq.heappush(pq, (distance, neighbor))

    return math.inf  # No path found

import heapq
import math

def a_star(graph, start, end):
    def heuristic(a, b):
        # Euklidesowa heurystyka dla wierzchołków z współrzędnymi (x, y)
        return math.sqrt((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2)

    open_set = [(0, start)]  # (f_score, node)
    g_score = {node: math.inf for node in graph}
    f_score = {node: math.inf for node in graph}
    came_from = {}
    closed_set = set()

    g_score[start] = 0
    f_score[start] = heuristic(start, end)

    while open_set:
        current_f, current_node = heapq.heappop(open_set)

        # Jeśli już odwiedzony, pomijamy
        if current_node in closed_set:
            continue
        closed_set.add(current_node)

        # Jeśli dotarliśmy do celu, zwróć koszt ścieżki
        if current_node == end:
            return g_score[end]

        for neighbor, weight in graph[current_node]:
            if neighbor in closed_set:
                continue

            tentative_g = g_score[current_node] + weight
            if tentative_g < g_score[neighbor]:
                came_from[neighbor] = current_node
                g_score[neighbor] = tentative_g
                f_score[neighbor] = tentative_g + heuristic(neighbor, end)
                heapq.heappush(open_set, (f_score[neighbor], neighbor))

    return math.inf  # Brak ścieżki
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
    # rs = [100,1000,2000,3000,4000,5000,6000,7000,8000,9000,10000]
    rs = [100,200,300,400,500,600,700,800,900,1000]
    belman_results = []
    dijkstra_results = []
    a_start_results = []
    legend_entry = ["Dijkstra","A*"]

    repetitions = 10
    for rows in rs:
        dijkstra_time = 0
        a_star_time = 0
        belman_time = 0
        cols = rows
        print(rows)
        for rep in range(repetitions):
            rows, cols, grid = generate_random_data(rows, cols)
            graph, start, end = build_graph(rows, cols, grid)
            start_time = time.time()
            dijkstra_length = dijkstra(graph, start, end)
            dijkstra_time += time.time() - start_time
            # start_time = time.time()
            # bellman_ford_length = bellman_ford(graph, start, end)
            # bellman_ford_time = time.time() - start_time
            # print("Bellman-Ford length:", bellman_ford_length, "Time:", bellman_ford_time)
            start_time = time.time()
            a_star_length = a_star(graph, start, end)
            a_star_time += time.time() - start_time
            if dijkstra_length != a_star_length:
                print("Błąd: różne długości ścieżek!", dijkstra_length, a_star_length)

        dijkstra_results.append((cols, dijkstra_time))
        a_start_results.append((cols, a_star_time))
    create_latex_chart("shortest_path_chart.tex","Porównanie czasów działania algorytmów znajdowania najkrótszej ścieżki","fig:shortest_path_chart","Czas [s]","Liczba wierzchołków",[dijkstra_results,a_start_results],legend_entry)

