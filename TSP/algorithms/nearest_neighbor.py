"""
Algorytm K-Nearest Neighbor (heurystyka najbliższego sąsiada) dla TSP.
"""


def tsp_nearest_neighbor(matrix, start=0):
    """
    Rozwiązuje TSP metodą najbliższego sąsiada (Nearest Neighbor Heuristic).
    Jest to algorytm zachłanny, który w każdym kroku wybiera najbliższe
    nieodwiedzone miasto.
    
    Parametry:
        matrix: macierz kosztów przejść między miastami
        start: indeks miasta początkowego (domyślnie 0)
    
    Złożoność czasowa: O(n^2)
    
    Uwaga: Algorytm nie gwarantuje optymalnego rozwiązania, ale jest szybki
    i daje przybliżone rozwiązanie.
    """
    n = len(matrix)
    if n == 0:
        return 0, []
    if n == 1:
        return 0, [0, 0]
    if n == 2:
        return matrix[0][1] + matrix[1][0], [0, 1, 0]
    
    visited = [False] * n
    path = [start]
    visited[start] = True
    total_cost = 0
    current = start
    
    # Odwiedzamy wszystkie pozostałe miasta
    for _ in range(n - 1):
        nearest = -1
        min_dist = float('inf')
        
        # Szukamy najbliższego nieodwiedzonego miasta
        for j in range(n):
            if not visited[j] and matrix[current][j] < min_dist:
                min_dist = matrix[current][j]
                nearest = j
        
        # Przechodzimy do najbliższego miasta
        visited[nearest] = True
        path.append(nearest)
        total_cost += min_dist
        current = nearest
    
    # Powrót do miasta początkowego
    total_cost += matrix[current][start]
    path.append(start)
    
    return total_cost, path


def tsp_nearest_neighbor_best(matrix):
    """
    Rozwiązuje TSP metodą najbliższego sąsiada, próbując wszystkie
    możliwe miasta startowe i wybierając najlepsze rozwiązanie.
    
    Złożoność czasowa: O(n^3)
    
    Zwraca najlepszy wynik spośród wszystkich możliwych punktów startowych.
    """
    n = len(matrix)
    if n == 0:
        return 0, []
    if n == 1:
        return 0, [0, 0]
    
    best_cost = float('inf')
    best_path = None
    
    for start in range(n):
        cost, path = tsp_nearest_neighbor(matrix, start)
        if cost < best_cost:
            best_cost = cost
            best_path = path
    
    return best_cost, best_path


