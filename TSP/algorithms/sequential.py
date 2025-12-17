"""
Algorytm 123 (trasa sekwencyjna) dla TSP.
"""


def tsp_123(matrix):
    """
    Rozwiązuje TSP metodą trasy sekwencyjnej (algorytm 123).
    Tworzy trasę: 0 -> 1 -> 2 -> 3 -> ... -> n-1 -> 0
    
    Jest to najprostsza możliwa heurystyka - odwiedzamy miasta
    w kolejności ich numeracji.
    
    Złożoność czasowa: O(n)
    
    Uwaga: Algorytm nie próbuje optymalizować trasy, służy jako
    punkt odniesienia (baseline) do porównań z innymi algorytmami.
    """
    n = len(matrix)
    if n == 0:
        return 0, []
    if n == 1:
        return 0, [0, 0]
    
    # Tworzymy trasę sekwencyjną: 0 -> 1 -> 2 -> ... -> n-1 -> 0
    path = list(range(n)) + [0]
    
    # Obliczamy koszt trasy
    total_cost = 0
    for i in range(n):
        total_cost += matrix[path[i]][path[i + 1]]
    
    return total_cost, path


