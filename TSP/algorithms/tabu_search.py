"""
Algorytm Tabu Search dla TSP (dla asymetrycznego TSP).
"""
import random


def tsp_tabu_search(matrix, initial_path=None, max_iterations=1000, tabu_size=10):
    """
    Rozwiązuje TSP metodą przeszukiwania tabu (Tabu Search).
    
    Używa operatora swap (zamiana dwóch miast) który działa dla asymetrycznego TSP.
    
    Tabu Search to algorytm metaheurystyczny, który wykorzystuje lokalną
    pamięć przeszukiwania (listę tabu) do unikania cykli i eksploracji
    nowych obszarów przestrzeni rozwiązań.
    
    Algorytm działa w następujący sposób:
    1. Rozpoczyna od początkowej trasy
    2. W każdej iteracji:
       - Sprawdza sąsiedztwo aktualnego rozwiązania (zamiany swap)
       - Wybiera najlepszy ruch, który nie jest na liście tabu
       - Dodaje ruch do listy tabu
       - Aktualizuje najlepsze znalezione rozwiązanie
    3. Kończy po osiągnięciu maksymalnej liczby iteracji
    
    Parametry:
        matrix: macierz kosztów przejść między miastami (może być asymetryczna)
        initial_path: opcjonalna początkowa trasa (lista indeksów miast).
                     Jeśli None, generuje losową permutację.
        max_iterations: maksymalna liczba iteracji algorytmu
        tabu_size: rozmiar listy tabu (liczba zabronionych ruchów)
    
    Złożoność czasowa: O(max_iterations * n^2) gdzie n to liczba miast
    
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
    
    # Inicjalizacja początkowej trasy
    if initial_path is None:
        # Losowa permutacja miast
        path = list(range(n))
        random.shuffle(path)
        path.append(path[0])  # Zamknij cykl
    else:
        path = list(initial_path)
    
    # Oblicz koszt trasy
    def calculate_cost(tour):
        cost = 0
        for i in range(len(tour) - 1):
            cost += matrix[tour[i]][tour[i + 1]]
        return cost
    
    # Oblicz zmianę kosztu przy zamianie dwóch miast
    def calculate_swap_delta(tour, i, j):
        """
        Oblicza zmianę kosztu przy zamianie tour[i] z tour[j].
        Zakłada i < j i że nie zamieniamy pierwszego/ostatniego elementu.
        """
        if i == 0 or j == len(tour) - 1:
            return float('inf')
        if i >= j:
            return float('inf')
            
        old_cost = 0
        new_cost = 0
        
        if j == i + 1:
            # Sąsiednie miasta
            old_cost = matrix[tour[i-1]][tour[i]] + matrix[tour[i]][tour[j]] + matrix[tour[j]][tour[j+1]]
            new_cost = matrix[tour[i-1]][tour[j]] + matrix[tour[j]][tour[i]] + matrix[tour[i]][tour[j+1]]
        else:
            # Nie sąsiadują
            old_cost = (matrix[tour[i-1]][tour[i]] + matrix[tour[i]][tour[i+1]] +
                       matrix[tour[j-1]][tour[j]] + matrix[tour[j]][tour[j+1]])
            new_cost = (matrix[tour[i-1]][tour[j]] + matrix[tour[j]][tour[i+1]] +
                       matrix[tour[j-1]][tour[i]] + matrix[tour[i]][tour[j+1]])
        
        return new_cost - old_cost
    
    current_cost = calculate_cost(path)
    best_path = list(path)
    best_cost = current_cost
    
    # Lista tabu
    tabu_list = []
    
    # Główna pętla
    for iteration in range(max_iterations):
        best_move = None
        best_move_cost = float('inf')
        best_move_delta = float('inf')
        
        # Sprawdź wszystkie możliwe zamiany
        for i in range(1, n):
            for j in range(i + 1, n):
                move = (i, j)
                delta = calculate_swap_delta(path, i, j)
                
                if delta == float('inf'):
                    continue
                
                new_cost = current_cost + delta
                
                is_tabu = move in tabu_list
                aspiration_criterion = new_cost < best_cost
                
                if (not is_tabu or aspiration_criterion) and new_cost < best_move_cost:
                    best_move = move
                    best_move_cost = new_cost
                    best_move_delta = delta
        
        if best_move is None:
            break
        
        # Wykonaj zamianę
        i, j = best_move
        path[i], path[j] = path[j], path[i]
        current_cost = best_move_cost
        
        # Aktualizuj listę tabu
        tabu_list.append(best_move)
        if len(tabu_list) > tabu_size:
            tabu_list.pop(0)
        
        # Aktualizuj najlepsze rozwiązanie
        if current_cost < best_cost:
            best_cost = current_cost
            best_path = list(path)
    
    final_cost = calculate_cost(best_path)
    return final_cost, best_path


def tsp_tabu_search_with_restart(matrix, initial_path=None, max_iterations=1000, 
                                  tabu_size=10, restart_interval=200):
    """
    Rozwiązuje TSP metodą Tabu Search z okresowym restartem.
    """
    n = len(matrix)
    if n == 0:
        return 0, []
    if n == 1:
        return 0, [0, 0]
    if n == 2:
        return matrix[0][1] + matrix[1][0], [0, 1, 0]
    
    best_overall_cost = float('inf')
    best_overall_path = None
    
    num_restarts = max(1, max_iterations // restart_interval)
    iterations_per_restart = max_iterations // num_restarts
    
    for restart in range(num_restarts):
        if restart == 0 and initial_path is not None:
            start_path = initial_path
        else:
            start_path = list(range(n))
            random.shuffle(start_path)
            start_path.append(start_path[0])
        
        cost, path = tsp_tabu_search(matrix, start_path, iterations_per_restart, tabu_size)
        
        if cost < best_overall_cost:
            best_overall_cost = cost
            best_overall_path = path
    
    return best_overall_cost, best_overall_path
