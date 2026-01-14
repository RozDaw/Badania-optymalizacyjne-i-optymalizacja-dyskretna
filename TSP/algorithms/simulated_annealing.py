"""
Algorytm Simulated Annealing dla TSP.
"""
import random
import math


def tsp_simulated_annealing(matrix, initial_path=None, initial_temp=1000, 
                            cooling_rate=0.995, min_temp=0.1):
    """
    Rozwiązuje TSP metodą symulowanego wyżarzania (Simulated Annealing).
    
    Simulated Annealing to metaheurystyka inspirowana procesem wyżarzania metali.
    Algorytm akceptuje gorsze rozwiązania z pewnym prawdopodobieństwem, które
    maleje wraz z "temperaturą", co pozwala na ucieczkę z lokalnych optimów.
    
    Algorytm działa w następujący sposób:
    1. Rozpoczyna od początkowej trasy i wysokiej temperatury
    2. W każdej iteracji:
       - Generuje nowe rozwiązanie w sąsiedztwie (zamiana 2-opt)
       - Jeśli nowe rozwiązanie jest lepsze, akceptuje je
       - Jeśli gorsze, akceptuje z prawdopodobieństwem exp(-delta/T)
       - Obniża temperaturę zgodnie ze schematem chłodzenia
    3. Kończy gdy temperatura spadnie poniżej minimalnej
    
    Parametry:
        matrix: macierz kosztów przejść między miastami
        initial_path: opcjonalna początkowa trasa (lista indeksów miast).
                     Jeśli None, generuje losową permutację.
        initial_temp: początkowa temperatura
        cooling_rate: współczynnik chłodzenia (0 < cooling_rate < 1)
        min_temp: minimalna temperatura (kryterium stopu)
    
    Złożoność czasowa: O(n^2 * liczba_iteracji), gdzie n to liczba miast
    
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
    
    # Parametry algorytmu
    temperature = initial_temp
    
    # Główna pętla algorytmu
    while temperature > min_temp:
        # Generuj nowe rozwiązanie przez zamianę 2-opt
        # Wybierz losowe i i j takie, że i < j
        i = random.randint(0, n - 2)
        j = random.randint(i + 2, min(n, len(path) - 1))
        
        # Oblicz zmianę kosztu dla tej zamiany
        a0 = path[i]
        a1 = path[i + 1]
        b0 = path[j]
        b1 = path[j + 1] if j + 1 < len(path) else path[0]
        
        delta = (matrix[a0][b0] + matrix[a1][b1] - 
                matrix[a0][a1] - matrix[b0][b1])
        
        new_cost = current_cost + delta
        
        # Zdecyduj czy zaakceptować nowe rozwiązanie
        accept = False
        if delta < 0:
            # Nowe rozwiązanie jest lepsze - zawsze akceptuj
            accept = True
        else:
            # Nowe rozwiązanie jest gorsze - akceptuj z pewnym prawdopodobieństwem
            probability = math.exp(-delta / temperature)
            if random.random() < probability:
                accept = True
        
        if accept:
            # Wykonaj zamianę
            path[i + 1:j + 1] = reversed(path[i + 1:j + 1])
            current_cost = new_cost
            
            # Zaktualizuj najlepsze rozwiązanie
            if current_cost < best_cost:
                best_cost = current_cost
                best_path = list(path)
        
        # Obniż temperaturę
        temperature *= cooling_rate
    
    # Upewnij się, że zwracamy poprawny koszt
    final_cost = calculate_cost(best_path)
    return final_cost, best_path


def tsp_simulated_annealing_adaptive(matrix, initial_path=None, max_iterations=10000):
    """
    Rozwiązuje TSP metodą Simulated Annealing z adaptacyjnym schematem chłodzenia.
    
    Ta wersja automatycznie dostosowuje parametry temperatury na podstawie
    rozmiaru problemu i liczby iteracji.
    
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
    
    # Inicjalizacja początkowej trasy
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
    
    current_cost = calculate_cost(path)
    best_path = list(path)
    best_cost = current_cost
    
    # Adaptacyjne parametry temperatury
    # Temperatura początkowa zależna od średniego kosztu krawędzi
    avg_edge_cost = sum(sum(row) for row in matrix) / (n * n)
    initial_temp = avg_edge_cost * n * 0.5
    
    # Cooling rate dostosowany do liczby iteracji
    min_temp = 0.01
    cooling_rate = (min_temp / initial_temp) ** (1.0 / max_iterations)
    
    temperature = initial_temp
    
    for iteration in range(max_iterations):
        # Generuj nowe rozwiązanie
        i = random.randint(0, n - 2)
        j = random.randint(i + 2, min(n, len(path) - 1))
        
        if i >= j:
            continue
        
        # Oblicz zmianę kosztu
        a0 = path[i]
        a1 = path[i + 1]
        b0 = path[j]
        b1 = path[j + 1] if j + 1 < len(path) else path[0]
        
        delta = (matrix[a0][b0] + matrix[a1][b1] - 
                matrix[a0][a1] - matrix[b0][b1])
        
        new_cost = current_cost + delta
        
        # Kryterium akceptacji
        accept = delta < 0 or random.random() < math.exp(-delta / temperature)
        
        if accept:
            path[i + 1:j + 1] = reversed(path[i + 1:j + 1])
            current_cost = new_cost
            
            if current_cost < best_cost:
                best_cost = current_cost
                best_path = list(path)
        
        # Obniż temperaturę
        temperature *= cooling_rate
        
        # Dodatkowe kryterium stopu - jeśli temperatura zbyt niska
        if temperature < min_temp:
            break
    
    # Upewnij się, że zwracamy poprawny koszt
    final_cost = calculate_cost(best_path)
    return final_cost, best_path


def tsp_simulated_annealing_fast(matrix, initial_path=None):
    """
    Szybka wersja Simulated Annealing z mniejszą liczbą iteracji.
    Przydatna do szybkich testów i porównań.
    
    Parametry:
        matrix: macierz kosztów przejść między miastami
        initial_path: opcjonalna początkowa trasa
    
    Zwraca:
        (koszt_najlepszej_trasy, najlepsza_trasa)
    """
    n = len(matrix)
    # Dostosuj liczbę iteracji do rozmiaru problemu
    max_iterations = min(5000, n * 100)
    return tsp_simulated_annealing_adaptive(matrix, initial_path, max_iterations)
