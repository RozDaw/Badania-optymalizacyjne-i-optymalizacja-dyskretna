"""
TSP (Traveling Salesman Problem) - implementacje algorytmów:
1. Bruteforce (przegląd zupełny)
2. Branch and Bound (metoda podziału i ograniczeń)
3. Programowanie dynamiczne (algorytm Held-Karp)
4. K-Nearest Neighbor (heurystyka najbliższego sąsiada)
"""
import heapq
import itertools
import time
import sys


# ============================================================
# GENEROWANIE DANYCH TSP
# ============================================================
def tsp_rand(size, seed):
    """
    Generuje macierz kosztów dla problemu TSP.
    Wykorzystuje pseudolosowy generator z podanym seedem.
    """
    print(f"data: {size}")
    matrix = []
    for a in range(size):
        row = []
        for b in range(size):
            seed = (seed * 69069 + 1) & 0xFFFFFFFF
            d = (seed % 99 + 1) * (a != b)
            print('{:2d}'.format(d), end=" ")
            row.append(d)
        print()
        matrix.append(row)
    print()
    return matrix, seed


def generate_tsp_data(size, seed):
    """
    Generuje macierz kosztów dla problemu TSP.
    Zwraca macierz kosztów bez drukowania.
    """
    matrix = []
    for a in range(size):
        row = []
        for b in range(size):
            seed = (seed * 69069 + 1) & 0xFFFFFFFF
            d = (seed % 99 + 1) * (a != b)
            row.append(d)
        matrix.append(row)
    return matrix, seed


# ============================================================
# WCZYTYWANIE MACIERZY KOSZTÓW
# ============================================================
def load_cost_matrix(filename):
    """
    Wczytuje macierz kosztów z pliku tekstowego.
    Format pliku:
    data: N
    d11 d12 ... d1N
    d21 d22 ... d2N
    ...
    dN1 dN2 ... dNN
    """
    with open(filename, 'r') as f:
        lines = f.read().strip().splitlines()

    # Pierwsza linia: "data: N"
    first_line = lines[0].strip()
    if first_line.startswith("data:"):
        n = int(first_line.split(":")[1].strip())
    else:
        n = int(first_line)

    matrix = []
    for i in range(1, n + 1):
        row = list(map(int, lines[i].split()))
        matrix.append(row)

    return matrix


def load_cost_matrix_raw(text):
    """
    Wczytuje macierz kosztów z tekstu.
    Format:
    data: N
    d11 d12 ... d1N
    ...
    """
    lines = text.strip().splitlines()

    first_line = lines[0].strip()
    if first_line.startswith("data:"):
        n = int(first_line.split(":")[1].strip())
    else:
        n = int(first_line)

    matrix = []
    for i in range(1, n + 1):
        row = list(map(int, lines[i].split()))
        matrix.append(row)

    return matrix


def save_cost_matrix(filename, matrix):
    """
    Zapisuje macierz kosztów do pliku.
    """
    n = len(matrix)
    with open(filename, 'w') as f:
        f.write(f"data: {n}\n")
        for row in matrix:
            f.write(' '.join('{:2d}'.format(d) for d in row) + '\n')


# ============================================================
# ALGORYTM BRUTE FORCE (PRZEGLĄD ZUPEŁNY)
# ============================================================
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


# ============================================================
# ALGORYTM BRANCH AND BOUND
# ============================================================
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


# ============================================================
# ALGORYTM PROGRAMOWANIA DYNAMICZNEGO (HELD-KARP)
# ============================================================
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


# ============================================================
# ALGORYTM K-NEAREST NEIGHBOR (HEURYSTYKA NAJBLIŻSZEGO SĄSIADA)
# ============================================================
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


# ============================================================
# FUNKCJE POMOCNICZE
# ============================================================
def print_matrix(matrix):
    """Wyświetla macierz kosztów."""
    for row in matrix:
        print(' '.join('{:2d}'.format(d) for d in row))


def verify_solution(matrix, path, expected_cost):
    """Weryfikuje poprawność rozwiązania."""
    if not path:
        return expected_cost == 0

    cost = 0
    for i in range(len(path) - 1):
        cost += matrix[path[i]][path[i + 1]]

    return cost == expected_cost


# ============================================================
# MAIN
# ============================================================
if __name__ == "__main__":
    print("=" * 60)
    print("GENEROWANIE DANYCH TSP")
    print("=" * 60)

    # Generujemy dane zgodnie z wymaganiami
    for n in range(10, 21):
        tsp_rand(n, n)

    print("\n" + "=" * 60)
    print("TESTOWANIE ALGORYTMÓW TSP")
    print("=" * 60)

    # Test na małym przykładzie
    test_matrix, _ = generate_tsp_data(10, 10)
    print("\nMacierz testowa (10x10):")
    print_matrix(test_matrix)

    # Bruteforce
    print("\n--- Brute Force ---")
    start_time = time.time()
    bf_cost, bf_path = tsp_bruteforce(test_matrix)
    bf_time = time.time() - start_time
    print(f"Koszt: {bf_cost}")
    print(f"Ścieżka: {bf_path}")
    print(f"Czas: {bf_time:.6f} s")

    # Branch and Bound
    print("\n--- Branch and Bound ---")
    start_time = time.time()
    bb_cost, bb_path = tsp_branch_and_bound(test_matrix)
    bb_time = time.time() - start_time
    print(f"Koszt: {bb_cost}")
    print(f"Ścieżka: {bb_path}")
    print(f"Czas: {bb_time:.6f} s")

    # Programowanie dynamiczne
    print("\n--- Programowanie Dynamiczne (Held-Karp) ---")
    start_time = time.time()
    dp_cost, dp_path = tsp_dynamic_programming(test_matrix)
    dp_time = time.time() - start_time
    print(f"Koszt: {dp_cost}")
    print(f"Ścieżka: {dp_path}")
    print(f"Czas: {dp_time:.6f} s")

    # Nearest Neighbor (KNN)
    print("\n--- Nearest Neighbor (KNN) ---")
    start_time = time.time()
    nn_cost, nn_path = tsp_nearest_neighbor(test_matrix)
    nn_time = time.time() - start_time
    print(f"Koszt: {nn_cost}")
    print(f"Ścieżka: {nn_path}")
    print(f"Czas: {nn_time:.6f} s")

    # Nearest Neighbor Best (KNN ze wszystkich startów)
    print("\n--- Nearest Neighbor Best (KNN wszystkie starty) ---")
    start_time = time.time()
    nnb_cost, nnb_path = tsp_nearest_neighbor_best(test_matrix)
    nnb_time = time.time() - start_time
    print(f"Koszt: {nnb_cost}")
    print(f"Ścieżka: {nnb_path}")
    print(f"Czas: {nnb_time:.6f} s")

    # Weryfikacja
    print("\n--- Weryfikacja ---")
    print(f"Brute Force: {'OK' if verify_solution(test_matrix, bf_path, bf_cost) else 'BŁĄD'}")
    print(f"Branch and Bound: {'OK' if verify_solution(test_matrix, bb_path, bb_cost) else 'BŁĄD'}")
    print(f"Dynamic Programming: {'OK' if verify_solution(test_matrix, dp_path, dp_cost) else 'BŁĄD'}")
    print(f"Nearest Neighbor: {'OK' if verify_solution(test_matrix, nn_path, nn_cost) else 'BŁĄD'}")
    print(f"Nearest Neighbor Best: {'OK' if verify_solution(test_matrix, nnb_path, nnb_cost) else 'BŁĄD'}")

    if bf_cost == bb_cost == dp_cost:
        print("\nWszystkie algorytmy dokładne zwróciły ten sam koszt optymalny!")
        print(f"Koszt optymalny: {dp_cost}")
        print(f"Koszt Nearest Neighbor: {nn_cost} (różnica: {nn_cost - dp_cost}, {100*(nn_cost - dp_cost)/dp_cost:.1f}%)")
        print(f"Koszt Nearest Neighbor Best: {nnb_cost} (różnica: {nnb_cost - dp_cost}, {100*(nnb_cost - dp_cost)/dp_cost:.1f}%)")
    else:
        print(f"\nUWAGA: Różne koszty! BF={bf_cost}, BB={bb_cost}, DP={dp_cost}")

    # Porównanie czasów dla różnych rozmiarów
    print("\n" + "=" * 60)
    print("PORÓWNANIE CZASÓW WYKONANIA")
    print("=" * 60)

    sizes_bruteforce = [5, 6, 7, 8, 9, 10] # max 12
    sizes_bb = [5,6,7,8,9,10,11,12,13,14,16,17,18,19,20,21,22]
    sizes_dp = [5,6,7,8,9,10,11,12,13,14,16,17,18,19,20,21,22]

    print("\n--- Brute Force (małe instancje) ---")
    for size in sizes_bruteforce:
        matrix, _ = generate_tsp_data(size, size)
        start_time = time.time()
        cost, path = tsp_bruteforce(matrix)
        elapsed = time.time() - start_time
        print(f"n={size}: koszt={cost}, czas={elapsed:.6f} s")

    print("\n--- Branch and Bound ---")
    for size in sizes_bb:
        matrix, _ = generate_tsp_data(size, size)
        start_time = time.time()
        cost, path = tsp_branch_and_bound(matrix)
        elapsed = time.time() - start_time
        print(f"n={size}: koszt={cost}, czas={elapsed:.6f} s")

    print("\n--- Programowanie Dynamiczne ---")
    for size in sizes_dp:
        matrix, _ = generate_tsp_data(size, size)
        start_time = time.time()
        cost, path = tsp_dynamic_programming(matrix)
        elapsed = time.time() - start_time
        print(f"n={size}: koszt={cost}, czas={elapsed:.6f} s")

    # KNN może działać na znacznie większych instancjach
    sizes_nn = [5, 10, 20, 50, 100, 200, 500, 1000]
    
    print("\n--- Nearest Neighbor (KNN) ---")
    for size in sizes_nn:
        matrix, _ = generate_tsp_data(size, size)
        start_time = time.time()
        cost, path = tsp_nearest_neighbor(matrix)
        elapsed = time.time() - start_time
        print(f"n={size}: koszt={cost}, czas={elapsed:.6f} s")

    print("\n--- Nearest Neighbor Best (wszystkie starty) ---")
    for size in sizes_nn:
        matrix, _ = generate_tsp_data(size, size)
        start_time = time.time()
        cost, path = tsp_nearest_neighbor_best(matrix)
        elapsed = time.time() - start_time
        print(f"n={size}: koszt={cost}, czas={elapsed:.6f} s")

    # Demonstracja wczytywania macierzy
    print("\n" + "=" * 60)
    print("DEMONSTRACJA WCZYTYWANIA MACIERZY")
    print("=" * 60)

    sample_data = """data: 10
 0 24  4 40 96  6 59 40 90 76 
 4  0 95 14 65 37 26 20 11 38 
17 62  0 96 60 61 52 41  7 81 
82 82 52  0 39 11 12 43 10 29 
57 73 67 80  0 27 67 43  1 16 
89 85  1 49 24  0 23 86 53 97 
90 96  8 75  6 15  0 79 46  7 
90 60 87  6 12 46 98  0 14 48 
35 79 77 83 15 41 85  1  0 17 
34 45  5 17 92 38 86 62 53  0"""

    loaded_matrix = load_cost_matrix_raw(sample_data)
    print("\nWczytana macierz:")
    print_matrix(loaded_matrix)

    print("\n--- Rozwiązanie dla wczytanej macierzy ---")
    start_time = time.time()
    dp_cost, dp_path = tsp_dynamic_programming(loaded_matrix)
    elapsed = time.time() - start_time
    print(f"Koszt (DP): {dp_cost}")
    print(f"Ścieżka: {dp_path}")
    print(f"Czas: {elapsed:.6f} s")

    start_time = time.time()
    nn_cost, nn_path = tsp_nearest_neighbor(loaded_matrix)
    elapsed = time.time() - start_time
    print(f"\nKoszt (NN): {nn_cost}")
    print(f"Ścieżka: {nn_path}")
    print(f"Czas: {elapsed:.6f} s")

    start_time = time.time()
    nnb_cost, nnb_path = tsp_nearest_neighbor_best(loaded_matrix)
    elapsed = time.time() - start_time
    print(f"\nKoszt (NN Best): {nnb_cost}")
    print(f"Ścieżka: {nnb_path}")
    print(f"Czas: {elapsed:.6f} s")
