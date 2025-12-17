"""
Algorytm Branch and Bound (metoda podziału i ograniczeń) dla TSP.
"""
import heapq


def tsp_branch_and_bound(matrix):
    """
    Rozwiązuje TSP metodą podziału i ograniczeń (Branch and Bound).
    Wykorzystuje dolne ograniczenie oparte na minimalnych krawędziach.
    """
    n = len(matrix)
    if n == 0:
        return 0, []
    if n == 1:
        return 0, [0, 0]
    if n == 2:
        return matrix[0][1] + matrix[1][0], [0, 1, 0]

    INF = float('inf')

    def calc_initial_bound(path, visited):
        """Oblicza początkowe dolne ograniczenie."""
        bound = 0
        # Dla każdego nieodwiedzonego wierzchołka - minimalna krawędź wychodząca
        for v in range(n):
            if v not in visited:
                possible = [matrix[v][j] for j in range(n) if j != v and (j not in visited or j == 0)]
                if possible:
                    bound += min(possible)
        return bound

    best_cost = INF
    best_path = None

    # Używamy kolejki priorytetowej dla lepszego przycinania
    # (lower_bound, cost, path, visited)
    initial_visited = frozenset([0])
    initial_bound = calc_initial_bound([0], initial_visited)
    heap = [(initial_bound, 0, [0], initial_visited)]

    while heap:
        bound, cost, path, visited = heapq.heappop(heap)

        if bound >= best_cost:
            continue

        if len(path) == n:
            # Sprawdzamy powrót do wierzchołka 0
            total_cost = cost + matrix[path[-1]][0]
            if total_cost < best_cost:
                best_cost = total_cost
                best_path = path + [0]
            continue

        curr = path[-1]

        # Rozgałęziamy do wszystkich nieodwiedzonych wierzchołków
        for j in range(n):
            if j not in visited:
                new_cost = cost + matrix[curr][j]
                new_path = path + [j]
                new_visited = visited | frozenset([j])

                # Obliczamy dolne ograniczenie
                new_bound = new_cost

                # Dodajemy minimalne krawędzie dla nieodwiedzonych
                for v in range(n):
                    if v not in new_visited:
                        possible = [matrix[v][k] for k in range(n) if k != v and (k not in new_visited or k == 0)]
                        if possible:
                            new_bound += min(possible)

                # Dodajemy minimalną krawędź powrotną z ostatniego wierzchołka
                if len(new_visited) < n:
                    remaining = [k for k in range(n) if k not in new_visited]
                    if remaining:
                        new_bound += min(matrix[j][k] for k in remaining)
                else:
                    # Ostatni wierzchołek - dodajemy powrót do 0
                    new_bound += matrix[j][0]

                if new_bound < best_cost:
                    heapq.heappush(heap, (new_bound, new_cost, new_path, new_visited))

    return best_cost, best_path


