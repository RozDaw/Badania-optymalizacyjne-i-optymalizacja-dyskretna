"""
Algorytm 2-opt (poprawa dwu-optymalna) dla TSP.

Referencja: https://en.wikipedia.org/wiki/2-opt
"""


def tsp_2opt(matrix, initial_path=None, use_restart=False):
    """
    Rozwiązuje TSP metodą 2-opt (algorytm poprawy dwu-optymalnej).
    
    Algorytm 2-opt to metoda lokalnego przeszukiwania, która iteracyjnie
    poprawia istniejącą trasę poprzez usuwanie dwóch krawędzi i ponowne
    łączenie trasy w inny sposób (odwracając segment między nimi).
    
    Parametry:
        matrix: macierz kosztów przejść między miastami
        initial_path: opcjonalna początkowa trasa (lista indeksów miast).
                     Jeśli None, używa trasy sekwencyjnej.
        use_restart: jeśli True, używa random restart z kilkoma punktami startowymi
    
    Złożoność czasowa: O(n^2) na iterację, aż do zbieżności
    
    Zwraca:
        (koszt_najlepszej_trasy, najlepsza_trasa)
    """
    n = len(matrix)
    if n == 0:
        return 0, []
    if n == 1:
        return 0, [0, 0]
    if n == 2:
        return matrix[0][1] + matrix[1][0], [0, 1, 0]
    
    # Random restart dla większych n - próbuj z kilkoma punktami startowymi
    if use_restart and n > 20:
        import random
        best_cost = float('inf')
        best_tour = None
        
        # Użyj podanego punktu startowego jako pierwszy
        if initial_path is not None:
            if len(initial_path) > n and initial_path[-1] == initial_path[0]:
                start_tour = list(initial_path[:-1])
            else:
                start_tour = list(initial_path)
            cost, tour = _tsp_2opt_single(matrix, start_tour)
            if cost < best_cost:
                best_cost = cost
                best_tour = tour
        else:
            # Jeśli nie podano, użyj sekwencyjnej
            start_tour = list(range(n))
            cost, tour = _tsp_2opt_single(matrix, start_tour)
            if cost < best_cost:
                best_cost = cost
                best_tour = tour
        
        # Dodatkowe losowe punkty startowe
        num_restarts = min(3, max(1, n // 20))
        for _ in range(num_restarts):
            random_tour = list(range(n))
            random.shuffle(random_tour)
            cost, tour = _tsp_2opt_single(matrix, random_tour)
            if cost < best_cost:
                best_cost = cost
                best_tour = tour
        
        return best_cost, best_tour + [best_tour[0]]
    
    # Standardowe wykonanie
    if initial_path is None:
        tour = list(range(n))
    else:
        if len(initial_path) > n and initial_path[-1] == initial_path[0]:
            tour = list(initial_path[:-1])
        else:
            tour = list(initial_path)
    
    cost, result_tour = _tsp_2opt_single(matrix, tour)
    return cost, result_tour + [result_tour[0]]


def _tsp_2opt_single(matrix, tour):
    """
    Wykonuje pojedyncze uruchomienie 2-opt na danej trasie.
    """
    n = len(matrix)
    
    def calculate_tour_cost(t):
        """Oblicza koszt trasy (cyklu)."""
        cost = 0
        for i in range(len(t)):
            cost += matrix[t[i]][t[(i + 1) % len(t)]]
        return cost
    
    def two_opt_swap(t, i, j):
        """
        Wykonuje 2-opt swap: odwraca segment od i+1 do j (włącznie).
        """
        return t[:i+1] + t[i+1:j+1][::-1] + t[j+1:]
    
    current_cost = calculate_tour_cost(tour)
    initial_cost = current_cost
    best_tour = list(tour)
    best_cost = current_cost
    
    # Główna pętla 2-opt - kontynuuj dopóki są poprawy
    # Zwiększona liczba iteracji dla lepszych wyników (wolniejsze, ale lepsze)
    improved = True
    if n <= 50:
        max_iterations = n * n * 10  # Więcej iteracji dla średnich n
    elif n <= 100:
        max_iterations = n * n * 8
    elif n <= 200:
        max_iterations = n * n * 5
    else:
        max_iterations = n * n * 3
    iteration = 0
    
    while improved and iteration < max_iterations:
        improved = False
        iteration += 1
        
        # Znajdź najlepszą poprawę w tej iteracji
        best_delta = 0
        best_i, best_j = -1, -1
        
        for i in range(n - 1):
            for j in range(i + 2, n):
                # Nie zamieniaj jeśli i=0 i j=n-1 (to by odwróciło całą trasę)
                if i == 0 and j == n - 1:
                    continue
                
                # Wykonaj swap i oblicz nowy koszt
                new_tour = two_opt_swap(tour, i, j)
                new_cost = calculate_tour_cost(new_tour)
                delta = new_cost - current_cost
                
                if delta < best_delta:
                    best_delta = delta
                    best_i, best_j = i, j
        
        # Wykonaj najlepszą poprawę
        if best_delta < -1e-10:
            tour = two_opt_swap(tour, best_i, best_j)
            current_cost = calculate_tour_cost(tour)
            improved = True
            
            if current_cost < best_cost:
                best_cost = current_cost
                best_tour = list(tour)
    
    # Upewnij się, że koszt jest poprawnie obliczony
    final_cost = calculate_tour_cost(best_tour)
    
    # Zwróć najlepsze rozwiązanie (nie gorsze niż początkowe)
    if final_cost > initial_cost:
        return initial_cost, list(tour)
    
    return final_cost, best_tour
