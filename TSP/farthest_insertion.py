"""
Algorytm Farthest Insertion (wstawianie najdalszego) dla TSP.
"""


def tsp_farthest_insertion(matrix):
    """
    Rozwiązuje TSP metodą wstawiania najdalszego (Farthest Insertion).
    
    Algorytm działa w następujący sposób:
    1. Rozpoczyna od cyklu składającego się z dwóch najbardziej oddalonych od siebie miast
    2. W każdym kroku:
       - Znajduje miasto, które jest najdalej od aktualnego cyklu
       - Wstawia to miasto do cyklu w miejscu, które najmniej zwiększa długość trasy
    3. Powtarza krok 2 aż wszystkie miasta zostaną dodane do cyklu
    
    Złożoność czasowa: O(n^3)
    
    Uwaga: Jest to algorytm konstrukcyjny (heurystyczny), który nie gwarantuje
    znalezienia optymalnego rozwiązania, ale często daje dobre przybliżenie.
    """
    n = len(matrix)
    if n == 0:
        return 0, []
    if n == 1:
        return 0, [0, 0]
    if n == 2:
        return matrix[0][1] + matrix[1][0], [0, 1, 0]
    
    # Krok 1: Znajdź dwa najbardziej oddalone miasta
    max_dist = 0
    city_a = 0
    city_b = 1
    for i in range(n):
        for j in range(i + 1, n):
            if matrix[i][j] > max_dist:
                max_dist = matrix[i][j]
                city_a = i
                city_b = j
    
    # Rozpocznij cykl od dwóch najbardziej oddalonych miast
    tour = [city_a, city_b]
    in_tour = [False] * n
    in_tour[city_a] = True
    in_tour[city_b] = True
    
    # Krok 2: Dodawaj kolejne miasta do cyklu
    while len(tour) < n:
        # Znajdź miasto najdalej od aktualnego cyklu
        # (minimalna odległość do najbliższego miasta w cyklu jest maksymalna)
        max_min_dist = -1
        farthest_city = -1
        
        for i in range(n):
            if not in_tour[i]:
                # Oblicz minimalną odległość od miasta i do miast w cyklu
                min_dist = float('inf')
                for j in tour:
                    min_dist = min(min_dist, matrix[i][j])
                
                # Jeśli to miasto jest najdalej od cyklu, zapamiętaj je
                if min_dist > max_min_dist:
                    max_min_dist = min_dist
                    farthest_city = i
        
        # Znajdź najlepsze miejsce w cyklu do wstawienia najdalszego miasta
        # (takie które najmniej zwiększa długość trasy)
        best_position = 0
        min_increase = float('inf')
        
        for pos in range(len(tour)):
            # Oblicz koszt wstawienia miasta między tour[pos] i tour[(pos+1) % len(tour)]
            next_pos = (pos + 1) % len(tour)
            current_edge_cost = matrix[tour[pos]][tour[next_pos]]
            new_edges_cost = matrix[tour[pos]][farthest_city] + matrix[farthest_city][tour[next_pos]]
            increase = new_edges_cost - current_edge_cost
            
            if increase < min_increase:
                min_increase = increase
                best_position = pos + 1
        
        # Wstaw miasto w najlepszej pozycji
        tour.insert(best_position, farthest_city)
        in_tour[farthest_city] = True
    
    # Zamknij cykl (powrót do pierwszego miasta)
    tour.append(tour[0])
    
    # Oblicz całkowity koszt trasy
    total_cost = 0
    for i in range(len(tour) - 1):
        total_cost += matrix[tour[i]][tour[i + 1]]
    
    return total_cost, tour

