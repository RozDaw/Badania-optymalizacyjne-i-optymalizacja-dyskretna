"""
Algorytm Tabu Search dla TSP.
"""
import random


def tsp_tabu_search(matrix, initial_path=None, max_iterations=1000, tabu_size=10):
    """
    Rozwiązuje TSP metodą przeszukiwania tabu (Tabu Search).
    
    Tabu Search to algorytm metaheurystyczny, który wykorzystuje lokalną
    pamięć przeszukiwania (listę tabu) do unikania cykli i eksploracji
    nowych obszarów przestrzeni rozwiązań.
    
    Algorytm działa w następujący sposób:
    1. Rozpoczyna od początkowej trasy
    2. W każdej iteracji:
       - Sprawdza sąsiedztwo aktualnego rozwiązania (zamiany 2-opt)
       - Wybiera najlepszy ruch, który nie jest na liście tabu
       - Dodaje ruch do listy tabu
       - Aktualizuje najlepsze znalezione rozwiązanie
    3. Kończy po osiągnięciu maksymalnej liczby iteracji
    
    Parametry:
        matrix: macierz kosztów przejść między miastami
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
    
    # Oblicz koszt początkowej trasy
    def calculate_cost(tour):
        cost = 0
        for i in range(len(tour) - 1):
            cost += matrix[tour[i]][tour[i + 1]]
        return cost
    
    current_cost = calculate_cost(path)
    best_path = list(path)
    best_cost = current_cost
    
    # Lista tabu - przechowuje zabronione ruchy jako pary (i, j)
    tabu_list = []
    
    # Główna pętla algorytmu
    for iteration in range(max_iterations):
        # Znajdź najlepszy ruch w sąsiedztwie (2-opt)
        best_move = None
        best_move_cost = float('inf')
        best_move_delta = 0
        
        # Sprawdź wszystkie możliwe zamiany 2-opt
        # path ma długość n+1 (ostatni element = pierwszy)
        # Możemy odwracać segmenty od pozycji 1 do n-1
        for i in range(n - 1):
            for j in range(i + 2, n):
                # Sprawdź czy ten ruch nie jest na liście tabu
                move = (i, j)
                
                # Oblicz zmianę kosztu dla tego ruchu (2-opt)
                # Krawędzie przed zmianą: path[i]->path[i+1] i path[j]->path[j+1]
                # Krawędzie po zmianie: path[i]->path[j] i path[i+1]->path[j+1]
                a0 = path[i]
                a1 = path[i + 1]
                b0 = path[j]
                b1 = path[j + 1] if j + 1 < len(path) else path[0]
                
                delta = (matrix[a0][b0] + matrix[a1][b1] - 
                        matrix[a0][a1] - matrix[b0][b1])
                
                new_cost = current_cost + delta
                
                # Kryterium aspiracji: akceptuj ruch z listy tabu,
                # jeśli prowadzi do najlepszego dotychczas rozwiązania
                is_tabu = move in tabu_list
                aspiration_criterion = new_cost < best_cost
                
                if (not is_tabu or aspiration_criterion) and new_cost < best_move_cost:
                    best_move = move
                    best_move_cost = new_cost
                    best_move_delta = delta
        
        # Jeśli nie znaleziono żadnego ruchu (nie powinno się zdarzyć), przerwij
        if best_move is None:
            break
        
        # Wykonaj najlepszy znaleziony ruch (odwróć segment)
        i, j = best_move
        path[i + 1:j + 1] = reversed(path[i + 1:j + 1])
        current_cost = best_move_cost  # Użyj obliczonego kosztu zamiast delta
        
        # Zaktualizuj listę tabu
        tabu_list.append(best_move)
        if len(tabu_list) > tabu_size:
            tabu_list.pop(0)
        
        # Zaktualizuj najlepsze rozwiązanie
        if current_cost < best_cost:
            best_cost = current_cost
            best_path = list(path)
    
    # Upewnij się, że zwracamy poprawny koszt
    final_cost = calculate_cost(best_path)
    
    # Upewnij się, że zwracamy poprawny koszt
    final_cost = calculate_cost(best_path)
    
    return final_cost, best_path


def tsp_tabu_search_with_restart(matrix, initial_path=None, max_iterations=1000, 
                                  tabu_size=10, restart_interval=200):
    """
    Rozwiązuje TSP metodą Tabu Search z okresowym restartem.
    
    Ta wersja algorytmu wykonuje restart (rozpoczyna od nowej losowej trasy)
    co restart_interval iteracji, aby uniknąć ugrzęźnięcia w lokalnych optimach.
    
    Parametry:
        matrix: macierz kosztów przejść między miastami
        initial_path: opcjonalna początkowa trasa
        max_iterations: maksymalna liczba iteracji algorytmu
        tabu_size: rozmiar listy tabu
        restart_interval: liczba iteracji między restartami
    
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
    
    best_overall_cost = float('inf')
    best_overall_path = None
    
    # Liczba restartów
    num_restarts = max(1, max_iterations // restart_interval)
    iterations_per_restart = max_iterations // num_restarts
    
    for restart in range(num_restarts):
        # Dla pierwszego restartu użyj podanej trasy początkowej
        if restart == 0 and initial_path is not None:
            start_path = initial_path
        else:
            # Dla kolejnych restartów generuj losową permutację
            start_path = list(range(n))
            random.shuffle(start_path)
            start_path.append(start_path[0])
        
        # Uruchom Tabu Search
        cost, path = tsp_tabu_search(matrix, start_path, iterations_per_restart, tabu_size)
        
        # Zaktualizuj najlepsze rozwiązanie
        if cost < best_overall_cost:
            best_overall_cost = cost
            best_overall_path = path
    
    return best_overall_cost, best_overall_path
