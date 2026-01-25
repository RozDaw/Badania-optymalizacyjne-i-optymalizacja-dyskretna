"""
Algorytm Simulated Annealing dla TSP.

Referencja: https://en.wikipedia.org/wiki/Simulated_annealing
"""
import random
import math


def tsp_simulated_annealing(matrix, initial_path=None, initial_temp=10000, 
                            cooling_rate=0.9995, min_temp=1e-8):
    """
    Rozwiązuje TSP metodą symulowanego wyżarzania (Simulated Annealing).
    
    Simulated Annealing to metaheurystyka inspirowana procesem wyżarzania metali.
    Algorytm akceptuje gorsze rozwiązania z pewnym prawdopodobieństwem, które
    maleje wraz z "temperaturą", co pozwala na ucieczkę z lokalnych optimów.
    
    Parametry:
        matrix: macierz kosztów przejść między miastami
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
        tour = list(range(n))
        random.shuffle(tour)
    else:
        # Usuń ostatni element jeśli jest powtórzeniem pierwszego
        if len(initial_path) > n and initial_path[-1] == initial_path[0]:
            tour = list(initial_path[:-1])
        else:
            tour = list(initial_path)
    
    def calculate_tour_cost(t):
        """Oblicza koszt trasy (cyklu)."""
        cost = 0
        for i in range(len(t)):
            cost += matrix[t[i]][t[(i + 1) % len(t)]]
        return cost
    
    def two_opt_swap(t, i, j):
        """Wykonuje 2-opt swap: odwraca segment od i+1 do j."""
        return t[:i+1] + t[i+1:j+1][::-1] + t[j+1:]
    
    def get_neighbor_2opt(t):
        """Generuje sąsiada przez losowy 2-opt move."""
        i = random.randint(0, len(t) - 2)
        j = random.randint(i + 1, len(t) - 1)
        # Unikaj odwracania całej trasy
        if i == 0 and j == len(t) - 1:
            j = len(t) - 2
        return two_opt_swap(t, i, j)
    
    current_tour = tour
    current_cost = calculate_tour_cost(current_tour)
    
    best_tour = list(current_tour)
    best_cost = current_cost
    initial_cost = current_cost  # Zapamiętaj początkowy koszt
    
    temperature = initial_temp
    
    while temperature > min_temp:
        # Generuj sąsiada (2-opt move)
        new_tour = get_neighbor_2opt(current_tour)
        new_cost = calculate_tour_cost(new_tour)
        
        delta = new_cost - current_cost
        
        # Kryterium akceptacji Metropolis
        if delta < 0:
            # Zawsze akceptuj lepsze rozwiązanie
            current_tour = new_tour
            current_cost = new_cost
            
            if current_cost < best_cost:
                best_tour = list(current_tour)
                best_cost = current_cost
        else:
            # Akceptuj gorsze rozwiązanie z prawdopodobieństwem exp(-delta/T)
            probability = math.exp(-delta / temperature)
            if random.random() < probability:
                current_tour = new_tour
                current_cost = new_cost
        
        # Chłodzenie
        temperature *= cooling_rate
    
    # Zawsze zwróć najlepsze znalezione (nie gorsze niż początkowe)
    if best_cost > initial_cost:
        return initial_cost, tour + [tour[0]]
    
    return best_cost, best_tour + [best_tour[0]]


def tsp_simulated_annealing_adaptive(matrix, initial_path=None, max_iterations=50000):
    """
    Rozwiązuje TSP metodą Simulated Annealing z adaptacyjnymi parametrami.
    
    Po zakończeniu SA, stosuje lokalną optymalizację 2-opt dla poprawy wyniku.
    
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
    
    # Inicjalizacja - użyj Nearest Neighbor jeśli nie podano rozwiązania początkowego
    if initial_path is None:
        from algorithms.nearest_neighbor import tsp_nearest_neighbor
        _, initial_path = tsp_nearest_neighbor(matrix)
    
    # Usuń ostatni element jeśli jest powtórzeniem pierwszego
    if len(initial_path) > n and initial_path[-1] == initial_path[0]:
        tour = list(initial_path[:-1])
    else:
        tour = list(initial_path)
    
    def calculate_tour_cost(t):
        """Oblicza koszt trasy (cyklu)."""
        cost = 0
        for i in range(len(t)):
            cost += matrix[t[i]][t[(i + 1) % len(t)]]
        return cost
    
    def two_opt_swap(t, i, j):
        """Wykonuje 2-opt swap: odwraca segment od i+1 do j."""
        return t[:i+1] + t[i+1:j+1][::-1] + t[j+1:]
    
    def get_neighbor_2opt(t):
        """Generuje sąsiada przez losowy 2-opt move."""
        i = random.randint(0, len(t) - 2)
        j = random.randint(i + 1, len(t) - 1)
        if i == 0 and j == len(t) - 1:
            j = len(t) - 2
        return two_opt_swap(t, i, j)
    
    def get_best_neighbor_sample(t, num_samples):
        """Znajduje najlepszego sąsiada z próbki wszystkich możliwych 2-opt moves."""
        best_tour = None
        best_cost = float('inf')
        best_delta = float('inf')
        
        # Próbka możliwych 2-opt moves
        possible_moves = []
        for i in range(len(t) - 1):
            for j in range(i + 2, len(t)):
                if not (i == 0 and j == len(t) - 1):
                    possible_moves.append((i, j))
        
        # Losowa próbka
        if len(possible_moves) > num_samples:
            sample_moves = random.sample(possible_moves, num_samples)
        else:
            sample_moves = possible_moves
        
        current_cost = calculate_tour_cost(t)
        for i, j in sample_moves:
            new_tour = two_opt_swap(t, i, j)
            new_cost = calculate_tour_cost(new_tour)
            delta = new_cost - current_cost
            
            if delta < best_delta:
                best_tour = new_tour
                best_cost = new_cost
                best_delta = delta
        
        return best_tour, best_cost, best_delta
    
    def local_search_2opt(t):
        """Lokalna optymalizacja 2-opt - znajduje lokalne optimum."""
        current = list(t)
        current_cost = calculate_tour_cost(current)
        improved = True
        
        while improved:
            improved = False
            best_delta = 0
            best_i, best_j = -1, -1
            
            for i in range(n - 1):
                for j in range(i + 2, n):
                    if i == 0 and j == n - 1:
                        continue
                    new_tour = two_opt_swap(current, i, j)
                    new_cost = calculate_tour_cost(new_tour)
                    delta = new_cost - current_cost
                    
                    if delta < best_delta:
                        best_delta = delta
                        best_i, best_j = i, j
            
            if best_delta < -1e-10:
                current = two_opt_swap(current, best_i, best_j)
                current_cost += best_delta
                improved = True
        
        return current, calculate_tour_cost(current)
    
    current_tour = tour
    current_cost = calculate_tour_cost(current_tour)
    initial_cost = current_cost
    
    best_tour = list(current_tour)
    best_cost = current_cost
    
    # Adaptacyjne parametry - wystarczająca eksploracja dla dobrych wyników
    avg_cost = sum(sum(row) for row in matrix) / (n * n)
    # Temperatura początkowa - wystarczająca do eksploracji
    initial_temp = avg_cost * n * 50
    min_temp = 0.05  # Wyższa minimalna temperatura - lepsza eksploracja
    
    if max_iterations > 0:
        cooling_rate = (min_temp / initial_temp) ** (1.0 / max_iterations)
    else:
        cooling_rate = 0.9999
    
    temperature = initial_temp
    
    # Licznik iteracji bez poprawy best_cost
    no_improvement_count = 0
    max_no_improvement = max_iterations // 3  # Daj więcej czasu na eksplorację
    
    for iteration in range(max_iterations):
        # Strategia: znajdź najlepszego sąsiada z próbki wszystkich możliwych 2-opt moves
        # Więcej próbek dla lepszej eksploracji, ale zbalansowane dla szybkości
        if n <= 50:
            num_samples = min(150, max(60, int(n * 3)))
        elif n <= 100:
            num_samples = min(80, max(40, n))
        elif n <= 200:
            num_samples = min(60, max(30, n // 2))
        else:
            num_samples = min(50, max(25, n // 3))
        
        new_tour, new_cost, delta = get_best_neighbor_sample(current_tour, num_samples)
        
        if new_tour is None:
            # Jeśli nie znaleziono sąsiada, użyj losowego
            new_tour = get_neighbor_2opt(current_tour)
            new_cost = calculate_tour_cost(new_tour)
            delta = new_cost - current_cost
        
        # Akceptuj nowe rozwiązanie zgodnie z kryterium Metropolis
        if new_tour is not None:
            if delta < 0:
                # Zawsze akceptuj lepsze rozwiązanie
                current_tour = new_tour
                current_cost = new_cost
                
                if current_cost < best_cost:
                    best_tour = list(current_tour)
                    best_cost = current_cost
                    no_improvement_count = 0
                else:
                    no_improvement_count += 1
            elif temperature > 0:
                # Akceptuj gorsze rozwiązanie z prawdopodobieństwem Metropolis
                probability = math.exp(-delta / max(temperature, 0.001))
                if random.random() < probability:
                    current_tour = new_tour
                    current_cost = new_cost
                    no_improvement_count += 1
                else:
                    no_improvement_count += 1
            else:
                no_improvement_count += 1
        else:
            no_improvement_count += 1
        
        # Chłodzenie
        temperature *= cooling_rate
        
        # Przerwij jeśli temperatura zbyt niska lub długo brak poprawy
        if temperature < min_temp:
            break
        if no_improvement_count > max_no_improvement and best_cost < initial_cost:
            # Jeśli już znaleźliśmy poprawę, możemy przerwać wcześniej
            break
    
    # Zastosuj lokalną optymalizację 2-opt tylko jeśli SA znalazło lepsze rozwiązanie
    # Jeśli best_cost == initial_cost, to SA nie znalazło poprawy i lokalna optymalizacja
    # może tylko przywrócić lokalne optimum (które już mamy), więc pomijamy ją
    if best_cost < initial_cost:
        # SA znalazło lepsze rozwiązanie - zastosuj lokalną optymalizację
        optimized_tour, optimized_cost = local_search_2opt(best_tour)
        
        if optimized_cost < best_cost:
            best_tour = optimized_tour
            best_cost = optimized_cost
    
    # Zawsze zwróć najlepsze znalezione (nie gorsze niż początkowe)
    if best_cost > initial_cost:
        return initial_cost, tour + [tour[0]]
    
    return best_cost, best_tour + [best_tour[0]]


def tsp_simulated_annealing_fast(matrix, initial_path=None):
    """
    Szybka wersja Simulated Annealing z lokalną optymalizacją 2-opt.
    
    Używa SA do eksploracji przestrzeni rozwiązań, a następnie 2-opt
    do lokalnej optymalizacji.
    
    Parametry:
        matrix: macierz kosztów przejść między miastami
        initial_path: opcjonalna początkowa trasa (jeśli None, użyje Nearest Neighbor)
    
    Zwraca:
        (koszt_najlepszej_trasy, najlepsza_trasa)
    """
    n = len(matrix)
    # Zwiększona liczba iteracji dla lepszej eksploracji
    # Dla większych n potrzebujemy więcej czasu na znalezienie lepszych rozwiązań
    # Zbalansowana liczba iteracji - wystarczająca do znalezienia poprawy, ale szybka
    # Dla większych n mniej iteracji, aby zmieścić się w timeout
    if n <= 50:
        max_iterations = max(5000, n * n * 2)
    elif n <= 100:
        max_iterations = max(5000, n * n // 2)  # Więcej iteracji dla n=100
    elif n <= 200:
        max_iterations = max(5000, n * n // 4)
    else:
        max_iterations = min(8000, max(6000, n * n // 6))
    return tsp_simulated_annealing_adaptive(matrix, initial_path, max_iterations)
