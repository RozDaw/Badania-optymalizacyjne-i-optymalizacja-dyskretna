"""
Algorytm programowania dynamicznego (Held-Karp) dla TSP.
"""


def tsp_dynamic_programming(matrix):
    """
    Rozwiązuje TSP metodą programowania dynamicznego (algorytm Held-Karp).
    Złożoność czasowa: O(n^2 * 2^n)
    Złożoność pamięciowa: O(n * 2^n)
    """
    n = len(matrix)
    if n == 0:
        return 0, []
    if n == 1:
        return 0, [0, 0]
    if n == 2:
        return matrix[0][1] + matrix[1][0], [0, 1, 0]

    INF = float('inf')

    # dp[mask][i] = minimalny koszt dotarcia do wierzchołka i,
    # odwiedzając wierzchołki w masce 'mask', zaczynając od 0
    # mask jest maską bitową, gdzie bit i oznacza czy wierzchołek i został odwiedzony
    dp = [[INF] * n for _ in range(1 << n)]
    parent = [[-1] * n for _ in range(1 << n)]

    # Bazowy przypadek: zaczynamy od wierzchołka 0
    # mask=1 oznacza że tylko wierzchołek 0 jest odwiedzony (bit 0 ustawiony)
    dp[1][0] = 0

    for mask in range(1 << n):
        for last in range(n):
            if dp[mask][last] == INF:
                continue
            if not (mask & (1 << last)):
                continue

            # Próbujemy przejść do każdego nieodwiedzonego wierzchołka
            for next_v in range(n):
                if mask & (1 << next_v):
                    continue

                new_mask = mask | (1 << next_v)
                new_cost = dp[mask][last] + matrix[last][next_v]

                if new_cost < dp[new_mask][next_v]:
                    dp[new_mask][next_v] = new_cost
                    parent[new_mask][next_v] = last

    # Znajdujemy minimalny koszt powrotu do wierzchołka 0
    full_mask = (1 << n) - 1
    min_cost = INF
    last_vertex = -1

    for i in range(1, n):
        cost = dp[full_mask][i] + matrix[i][0]
        if cost < min_cost:
            min_cost = cost
            last_vertex = i

    # Odtwarzamy ścieżkę
    path = []
    mask = full_mask
    curr = last_vertex

    while curr != -1:
        path.append(curr)
        prev = parent[mask][curr]
        mask = mask ^ (1 << curr)
        curr = prev

    path.reverse()
    path.append(0)  # powrót do startu

    return min_cost, path


