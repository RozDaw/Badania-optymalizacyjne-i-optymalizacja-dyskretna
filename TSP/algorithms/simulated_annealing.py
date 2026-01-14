"""
Algorytm Simulated Annealing dla TSP (dla asymetrycznego TSP).
"""
import random
import math


def tsp_simulated_annealing(matrix, initial_path=None, initial_temp=1000, 
                            cooling_rate=0.995, min_temp=0.1):
    """
    Rozwiązuje TSP metodą symulowanego wyżarzania (Simulated Annealing).
    
    Używa operatora swap (zamiana dwóch miast) który działa dla asymetrycznego TSP.
    
    Simulated Annealing to metaheurystyka inspirowana procesem wyżarzania metali.
    Algorytm akceptuje gorsze rozwiązania z pewnym prawdopodobieństwem, które
    maleje wraz z "temperaturą", co pozwala na ucieczkę z lokalnych optimów.
    
    Parametry:
        matrix: macierz kosztów przejść między miastami (może być asymetryczna)
        initial_path: opcjonalna początkowa trasa
        initial_temp: początkowa temperatura
        cooling_rate: współczynnik chłodzenia (0 < cooling_rate < 1)
        min_temp: minimalna temperatura (kryterium stopu)
    
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
        path = list(range(n))
        random.shuffle(path)
        path.append(path[0])
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
        """Oblicza zmianę kosztu przy zamianie tour[i] z tour[j]."""
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
    
    temperature = initial_temp
    
    # Główna pętla algorytmu
    while temperature > min_temp:
        # Generuj losowe ruchy swap (wybierz dwa różne miasta)
        i = random.randint(1, n - 1)
        j = random.randint(1, n - 1)
        
        # Upewnij się, że i < j i różne
        if i == j:
            temperature *= cooling_rate
            continue
        if i > j:
            i, j = j, i
        
        # Oblicz zmianę kosztu
        delta = calculate_swap_delta(path, i, j)
        
        # Kryterium akceptacji
        accept = False
        if delta < 0:
            accept = True
        else:
            probability = math.exp(-delta / temperature)
            if random.random() < probability:
                accept = True
        
        if accept:
            path[i], path[j] = path[j], path[i]
            current_cost += delta
            
            if current_cost < best_cost:
                best_cost = current_cost
                best_path = list(path)
        
        temperature *= cooling_rate
    
    final_cost = calculate_cost(best_path)
    return final_cost, best_path


def tsp_simulated_annealing_adaptive(matrix, initial_path=None, max_iterations=10000):
    """
    Rozwiązuje TSP metodą Simulated Annealing z adaptacyjnymi parametrami.
    
    Parametry:
        matrix: macierz kosztów przejść między miastami
        initial_path: opcjonalna początkowa trasa
        max_iterations: maksymalna liczba iteracji algorytmu
    
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
    
    # Inicjalizacja
    if initial_path is None:
        path = list(range(n))
        random.shuffle(path)
        path.append(path[0])
    else:
        path = list(initial_path)
    
    def calculate_cost(tour):
        cost = 0
        for i in range(len(tour) - 1):
            cost += matrix[tour[i]][tour[i + 1]]
        return cost
    
    def calculate_swap_delta(tour, i, j):
        if i == 0 or j == len(tour) - 1 or i >= j:
            return float('inf')
        
        old_cost = 0
        new_cost = 0
        
        if j == i + 1:
            old_cost = matrix[tour[i-1]][tour[i]] + matrix[tour[i]][tour[j]] + matrix[tour[j]][tour[j+1]]
            new_cost = matrix[tour[i-1]][tour[j]] + matrix[tour[j]][tour[i]] + matrix[tour[i]][tour[j+1]]
        else:
            old_cost = (matrix[tour[i-1]][tour[i]] + matrix[tour[i]][tour[i+1]] +
                       matrix[tour[j-1]][tour[j]] + matrix[tour[j]][tour[j+1]])
            new_cost = (matrix[tour[i-1]][tour[j]] + matrix[tour[j]][tour[i+1]] +
                       matrix[tour[j-1]][tour[i]] + matrix[tour[i]][tour[j+1]])
        
        return new_cost - old_cost
    
    current_cost = calculate_cost(path)
    best_path = list(path)
    best_cost = current_cost
    
    # Adaptacyjne parametry
    avg_edge_cost = sum(sum(row) for row in matrix) / (n * n)
    initial_temp = avg_edge_cost * n * 0.5
    min_temp = 0.01
    cooling_rate = (min_temp / initial_temp) ** (1.0 / max_iterations)
    
    temperature = initial_temp
    
    for iteration in range(max_iterations):
        # Generuj losowe ruchy swap (wybierz dwa różne miasta)
        i = random.randint(1, n - 1)
        j = random.randint(1, n - 1)
        
        if i == j:
            temperature *= cooling_rate
            continue
        if i > j:
            i, j = j, i
        
        delta = calculate_swap_delta(path, i, j)
        
        accept = delta < 0 or random.random() < math.exp(-delta / temperature)
        
        if accept:
            path[i], path[j] = path[j], path[i]
            current_cost += delta
            
            if current_cost < best_cost:
                best_cost = current_cost
                best_path = list(path)
        
        temperature *= cooling_rate
        
        if temperature < min_temp:
            break
    
    final_cost = calculate_cost(best_path)
    return final_cost, best_path


def tsp_simulated_annealing_fast(matrix, initial_path=None):
    """
    Szybka wersja Simulated Annealing z mniejszą liczbą iteracji.
    
    Parametry:
        matrix: macierz kosztów przejść między miastami
        initial_path: opcjonalna początkowa trasa
    
    Zwraca:
        (koszt_najlepszej_trasy, najlepsza_trasa)
    """
    n = len(matrix)
    max_iterations = min(5000, n * 100)
    return tsp_simulated_annealing_adaptive(matrix, initial_path, max_iterations)
