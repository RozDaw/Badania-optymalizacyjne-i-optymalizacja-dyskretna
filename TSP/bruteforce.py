"""
Algorytm Brute Force (przegląd zupełny) dla TSP.
"""
import itertools


def tsp_bruteforce(matrix):
    """
    Rozwiązuje TSP metodą bruteforce (przegląd zupełny).
    Sprawdza wszystkie możliwe permutacje.
    Złożoność czasowa: O(n!)
    """
    n = len(matrix)
    if n == 0:
        return 0, []
    if n == 1:
        return 0, [0, 0]
    if n == 2:
        # Dla n=2 mamy tylko jedną możliwą trasę: 0 -> 1 -> 0
        return matrix[0][1] + matrix[1][0], [0, 1, 0]

    min_cost = float('inf')
    best_path = None

    # Generujemy wszystkie permutacje wierzchołków 1..n-1
    # (zaczynamy zawsze od wierzchołka 0)
    vertices = list(range(1, n))

    for perm in itertools.permutations(vertices):
        # Obliczamy koszt tej trasy
        cost = matrix[0][perm[0]]
        for i in range(len(perm) - 1):
            cost += matrix[perm[i]][perm[i + 1]]
        cost += matrix[perm[-1]][0]  # powrót do startu

        if cost < min_cost:
            min_cost = cost
            best_path = [0] + list(perm) + [0]

    return min_cost, best_path

