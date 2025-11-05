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
    return grid

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

def a_star(graph, start, end):
    def heuristic(a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])  # Manhattan distance

    open_set = [(0, start)]  # (f_score, node)
    g_score = {node: math.inf for node in graph}
    g_score[start] = 0
    f_score = {node: math.inf for node in graph}
    f_score[start] = heuristic(start, end)
    came_from = {}

    while open_set:
        current_f, current_node = heapq.heappop(open_set)

        if current_node == end:
            return g_score[end]

        for neighbor, weight in graph[current_node]:
            tentative_g_score = g_score[current_node] + weight
            if tentative_g_score < g_score[neighbor]:
                came_from[neighbor] = current_node
                g_score[neighbor] = tentative_g_score
                f_score[neighbor] = tentative_g_score + heuristic(neighbor, end)
                if neighbor not in [i[1] for i in open_set]:
                    heapq.heappush(open_set, (f_score[neighbor], neighbor))

    return math.inf  # No path found

if __name__ == "__main__":
    rows = 100
    cols = 500
    generate_random_data(rows, cols)
    rows, cols, grid = load_data(f'generated_data_{cols}-{rows}.txt')
    graph, start, end = build_graph(rows, cols, grid)
    print(cols," x ", rows)
    start_time = time.time()
    dijkstra_length = dijkstra(graph, start, end)
    dijkstra_time = time.time() - start_time
    print("Dijkstra length:", dijkstra_length, "Time:", dijkstra_time)
    # start_time = time.time()
    # bellman_ford_length = bellman_ford(graph, start, end)
    # bellman_ford_time = time.time() - start_time
    # print("Bellman-Ford length:", bellman_ford_length, "Time:", bellman_ford_time)
    start_time = time.time()
    a_star_length = a_star(graph, start, end)
    a_star_time = time.time() - start_time
    print("A* length:", a_star_length, "Time:", a_star_time)

