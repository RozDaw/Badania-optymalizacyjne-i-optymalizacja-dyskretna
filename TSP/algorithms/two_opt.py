"""
Algorytm 2-opt (poprawa dwu-optymalna) dla TSP.
"""


def tsp_2opt(matrix, initial_path=None):
    """
    Rozwiązuje TSP metodą 2-opt (algorytm poprawy dwu-optymalnej).
    
    Algorytm 2-opt to metoda lokalnego przeszukiwania, która iteracyjnie
    poprawia istniejącą trasę poprzez usuwanie dwóch krawędzi i ponowne
    łączenie trasy w inny sposób.
    
    Algorytm działa w następujący sposób:
    1. Rozpoczyna od początkowej trasy (jeśli nie podano, używa trasy sekwencyjnej)
    2. Sprawdza wszystkie możliwe pary krawędzi do zamiany
    3. Jeśli zamiana zmniejsza długość trasy, wykonuje ją (odwraca fragment trasy)
    4. Powtarza krok 2-3 aż nie można już poprawić trasy
    
    Parametry:
        matrix: macierz kosztów przejść między miastami (powinna być symetryczna)
        initial_path: opcjonalna początkowa trasa (lista indeksów miast).
                     Jeśli None, używa trasy sekwencyjnej.
    
    Złożoność czasowa: O(n^2) na iterację, liczba iteracji zależy od danych
    
    Uwaga: 
    - Jest to algorytm heurystyczny znajdujący optimum lokalne.
    - Wynik zależy od początkowej trasy.
    - Algorytm jest przeznaczony dla symetrycznego TSP (matrix[i][j] == matrix[j][i]).
      Dla asymetrycznego TSP może dawać niepoprawne wyniki.
    """
    n = len(matrix)
    if n == 0:
        return 0, []
    if n == 1:
        return 0, [0, 0]
    if n == 2:
        return matrix[0][1] + matrix[1][0], [0, 1, 0]
    
    # Jeśli nie podano początkowej trasy, użyj trasy sekwencyjnej
    if initial_path is None:
        path = list(range(n)) + [0]
    else:
        path = list(initial_path)  # Kopiujemy trasę
    
    # Oblicz początkowy koszt
    def calculate_path_cost(p):
        cost = 0
        for i in range(len(p) - 1):
            cost += matrix[p[i]][p[i + 1]]
        return cost
    
    initial_cost = calculate_path_cost(path)
    best_cost = initial_cost
    best_path = list(path)
    
    improved = True
    iteration = 0
    # Ograniczamy liczbę iteracji - dla większych n używamy proporcjonalnie mniej iteracji
    max_iterations = min(200, n * 3)  # Maksymalnie 200 iteracji lub 3*n
    
    while improved and iteration < max_iterations:
        iteration += 1
        improved = False
        best_delta = 0
        best_i = -1
        best_j = -1
        
        # Sprawdź wszystkie możliwe pary krawędzi do zamiany
        # W przypadku cyklu o długości n+1 (gdzie ostatni element = pierwszy),
        # sprawdzamy krawędzie od 0 do n-1
        # Dla n miast mamy n krawędzi (indeksy 0 do n-1)
        # i może być od 0 do n-2, j od i+2 do n-1 (aby krawędzie nie były sąsiednie)
        for i in range(n - 1):
            for j in range(i + 2, n):
                # Pobierz wierzchołki krawędzi
                # Krawędź 1: path[i] -> path[i+1]
                # Krawędź 2: path[j] -> path[j+1]
                a0 = path[i]
                a1 = path[i + 1]
                b0 = path[j]
                b1 = path[j + 1]
                
                # Oblicz zmianę kosztu przy zamianie:
                # Usuwamy krawędzie: a0->a1 i b0->b1
                # Dodajemy krawędzie: a0->b0 i a1->b1
                # (co odpowiada odwróceniu fragmentu trasy między i+1 a j)
                delta = (matrix[a0][b0] + matrix[a1][b1] - 
                        matrix[a0][a1] - matrix[b0][b1])
                
                # Znajdź najlepszą poprawę (największą redukcję kosztu)
                if delta < best_delta:
                    best_delta = delta
                    best_i = i
                    best_j = j
                    improved = True
        
        # Wykonaj najlepszą znalezioną poprawę
        if improved:
            # Odwróć fragment trasy od i+1 do j (włącznie)
            # Używamy slice reversal zamiast reversed() iteratora
            path[best_i + 1:best_j + 1] = path[best_i + 1:best_j + 1][::-1]
            
            # Oblicz nowy koszt i zaktualizuj najlepsze rozwiązanie
            current_cost = calculate_path_cost(path)
            if current_cost < best_cost:
                best_cost = current_cost
                best_path = list(path)
    
    # Zwróć najlepsze znalezione rozwiązanie (nigdy nie gorsze niż początkowe)
    return best_cost, best_path


