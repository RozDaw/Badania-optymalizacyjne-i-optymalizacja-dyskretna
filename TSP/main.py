"""
TSP (Traveling Salesman Problem) - główny moduł uruchomieniowy.

Dostępne algorytmy:
1. Bruteforce (przegląd zupełny)
2. Branch and Bound (metoda podziału i ograniczeń)
3. Programowanie dynamiczne (algorytm Held-Karp)
4. K-Nearest Neighbor (heurystyka najbliższego sąsiada)
5. Algorytm 123 (trasa sekwencyjna)
6. Farthest Insertion (algorytm wstawiania najdalszego)
7. 2-opt (algorytm poprawy dwu-optymalnej)
"""
import time

# Import funkcji pomocniczych
from data_utils import (
    tsp_rand,
    generate_tsp_data,
    load_cost_matrix,
    load_cost_matrix_raw,
    save_cost_matrix,
    load_coordinates_raw,
    print_matrix,
    verify_solution
)

# Import algorytmów
from bruteforce import tsp_bruteforce
from branch_and_bound import tsp_branch_and_bound
from dynamic_programming import tsp_dynamic_programming
from nearest_neighbor import tsp_nearest_neighbor, tsp_nearest_neighbor_best
from sequential import tsp_123
from farthest_insertion import tsp_farthest_insertion
from two_opt import tsp_2opt


if __name__ == "__main__":
    coords_data = """data:
40
97 35   57 36   29 23   57 39   18  7   92  7   29 41   26 42   94 11   55 26   49 47   98 11   29 25   96  7   64 37   26 31   93  9   28  1   15 26   74 47   75 16   10 44   30 48    8 43   34 45   31 46   95 29   55 38   84 45   60  4    3 16    7 21   81 16   37 30   27 28   66 43    2 46    8 46   53 18   36  3   
"""

    coords_matrix, coords = load_coordinates_raw(coords_data)
    print(f"\nWczytano {len(coords)} miast ze współrzędnymi:")
    for i, (x, y) in enumerate(coords):
        print(f"  Miasto {i}: ({x}, {y})")

    print("\n--- Rozwiązanie dla danych ze współrzędnymi ---")

    # Algorytm 123
    start_time = time.time()
    seq_cost, seq_path = tsp_123(coords_matrix)
    elapsed = time.time() - start_time
    print(f"\nAlgorytm 123:")
    print(f"Koszt: {seq_cost}")
    print(f"Ścieżka: {seq_path}")
    print(f"Czas: {elapsed:.6f} s")

    # Nearest Neighbor
    start_time = time.time()
    nn_cost, nn_path = tsp_nearest_neighbor(coords_matrix)
    elapsed = time.time() - start_time
    print(f"\nNearest Neighbor:")
    print(f"Koszt: {nn_cost}")
    print(f"Ścieżka: {nn_path}")
    print(f"Czas: {elapsed:.6f} s")

    # Nearest Neighbor Best
    start_time = time.time()
    nnb_cost, nnb_path = tsp_nearest_neighbor_best(coords_matrix)
    elapsed = time.time() - start_time
    print(f"\nNearest Neighbor Best:")
    print(f"Koszt: {nnb_cost}")
    print(f"Ścieżka: {nnb_path}")
    print(f"Czas: {elapsed:.6f} s")

    # Farthest Insertion
    start_time = time.time()
    fi_cost, fi_path = tsp_farthest_insertion(coords_matrix)
    elapsed = time.time() - start_time
    print(f"\nFarthest Insertion:")
    print(f"Koszt: {fi_cost}")
    print(f"Ścieżka: {fi_path}")
    print(f"Czas: {elapsed:.6f} s")

    # Porównanie
    print(f"\n--- Porównanie dla danych ze współrzędnymi (n={len(coords)}) ---")
    print(f"Algorytm 123: {seq_cost}")
    print(f"Nearest Neighbor: {nn_cost} (poprawa o {seq_cost - nn_cost}, {100*(seq_cost - nn_cost)/seq_cost:.1f}%)")
    print(f"Nearest Neighbor Best: {nnb_cost} (poprawa o {seq_cost - nnb_cost}, {100*(seq_cost - nnb_cost)/seq_cost:.1f}%)")
    print(f"Farthest Insertion: {fi_cost} (poprawa o {seq_cost - fi_cost}, {100*(seq_cost - fi_cost)/seq_cost:.1f}%)")
