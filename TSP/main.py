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


# ============================================================
# MAIN
# ============================================================
if __name__ == "__main__":
#     print("=" * 60)
#     print("GENEROWANIE DANYCH TSP")
#     print("=" * 60)
#
#     # Generujemy dane zgodnie z wymaganiami
#     for n in range(10, 21):
#         tsp_rand(n, n)
#
#     print("\n" + "=" * 60)
#     print("TESTOWANIE ALGORYTMÓW TSP")
#     print("=" * 60)
#
#     # Test na małym przykładzie
#     test_matrix, _ = generate_tsp_data(10, 10)
#     print("\nMacierz testowa (10x10):")
#     print_matrix(test_matrix)
#
#     # Bruteforce
#     print("\n--- Brute Force ---")
#     start_time = time.time()
#     bf_cost, bf_path = tsp_bruteforce(test_matrix)
#     bf_time = time.time() - start_time
#     print(f"Koszt: {bf_cost}")
#     print(f"Ścieżka: {bf_path}")
#     print(f"Czas: {bf_time:.6f} s")
#
#     # Branch and Bound
#     print("\n--- Branch and Bound ---")
#     start_time = time.time()
#     bb_cost, bb_path = tsp_branch_and_bound(test_matrix)
#     bb_time = time.time() - start_time
#     print(f"Koszt: {bb_cost}")
#     print(f"Ścieżka: {bb_path}")
#     print(f"Czas: {bb_time:.6f} s")
#
#     # Programowanie dynamiczne
#     print("\n--- Programowanie Dynamiczne (Held-Karp) ---")
#     start_time = time.time()
#     dp_cost, dp_path = tsp_dynamic_programming(test_matrix)
#     dp_time = time.time() - start_time
#     print(f"Koszt: {dp_cost}")
#     print(f"Ścieżka: {dp_path}")
#     print(f"Czas: {dp_time:.6f} s")
#
#     # Nearest Neighbor (KNN)
#     print("\n--- Nearest Neighbor (KNN) ---")
#     start_time = time.time()
#     nn_cost, nn_path = tsp_nearest_neighbor(test_matrix)
#     nn_time = time.time() - start_time
#     print(f"Koszt: {nn_cost}")
#     print(f"Ścieżka: {nn_path}")
#     print(f"Czas: {nn_time:.6f} s")
#
#     # Nearest Neighbor Best (KNN ze wszystkich startów)
#     print("\n--- Nearest Neighbor Best (KNN wszystkie starty) ---")
#     start_time = time.time()
#     nnb_cost, nnb_path = tsp_nearest_neighbor_best(test_matrix)
#     nnb_time = time.time() - start_time
#     print(f"Koszt: {nnb_cost}")
#     print(f"Ścieżka: {nnb_path}")
#     print(f"Czas: {nnb_time:.6f} s")
#
#     # Algorytm 123 (trasa sekwencyjna)
#     print("\n--- Algorytm 123 (trasa sekwencyjna) ---")
#     start_time = time.time()
#     seq_cost, seq_path = tsp_123(test_matrix)
#     seq_time = time.time() - start_time
#     print(f"Koszt: {seq_cost}")
#     print(f"Ścieżka: {seq_path}")
#     print(f"Czas: {seq_time:.6f} s")
#
#     # Weryfikacja
#     print("\n--- Weryfikacja ---")
#     print(f"Brute Force: {'OK' if verify_solution(test_matrix, bf_path, bf_cost) else 'BŁĄD'}")
#     print(f"Branch and Bound: {'OK' if verify_solution(test_matrix, bb_path, bb_cost) else 'BŁĄD'}")
#     print(f"Dynamic Programming: {'OK' if verify_solution(test_matrix, dp_path, dp_cost) else 'BŁĄD'}")
#     print(f"Nearest Neighbor: {'OK' if verify_solution(test_matrix, nn_path, nn_cost) else 'BŁĄD'}")
#     print(f"Nearest Neighbor Best: {'OK' if verify_solution(test_matrix, nnb_path, nnb_cost) else 'BŁĄD'}")
#     print(f"Algorytm 123: {'OK' if verify_solution(test_matrix, seq_path, seq_cost) else 'BŁĄD'}")
#
#     if bf_cost == bb_cost == dp_cost:
#         print("\nWszystkie algorytmy dokładne zwróciły ten sam koszt optymalny!")
#         print(f"Koszt optymalny: {dp_cost}")
#         if dp_cost > 0:
#             print(f"Koszt Algorytm 123: {seq_cost} (różnica: {seq_cost - dp_cost}, {100*(seq_cost - dp_cost)/dp_cost:.1f}%)")
#             print(f"Koszt Nearest Neighbor: {nn_cost} (różnica: {nn_cost - dp_cost}, {100*(nn_cost - dp_cost)/dp_cost:.1f}%)")
#             print(f"Koszt Nearest Neighbor Best: {nnb_cost} (różnica: {nnb_cost - dp_cost}, {100*(nnb_cost - dp_cost)/dp_cost:.1f}%)")
#         else:
#             print(f"Koszt Algorytm 123: {seq_cost}")
#             print(f"Koszt Nearest Neighbor: {nn_cost}")
#             print(f"Koszt Nearest Neighbor Best: {nnb_cost}")
#     else:
#         print(f"\nUWAGA: Różne koszty! BF={bf_cost}, BB={bb_cost}, DP={dp_cost}")
#         optimal_cost = min(bf_cost, bb_cost, dp_cost)
#         print(f"Najlepszy koszt: {optimal_cost}")
#         if optimal_cost > 0:
#             print(f"Koszt Algorytm 123: {seq_cost} (różnica: {seq_cost - optimal_cost}, {100*(seq_cost - optimal_cost)/optimal_cost:.1f}%)")
#             print(f"Koszt Nearest Neighbor: {nn_cost} (różnica: {nn_cost - optimal_cost}, {100*(nn_cost - optimal_cost)/optimal_cost:.1f}%)")
#             print(f"Koszt Nearest Neighbor Best: {nnb_cost} (różnica: {nnb_cost - optimal_cost}, {100*(nnb_cost - optimal_cost)/optimal_cost:.1f}%)")
#         else:
#             print(f"Koszt Algorytm 123: {seq_cost}")
#             print(f"Koszt Nearest Neighbor: {nn_cost}")
#             print(f"Koszt Nearest Neighbor Best: {nnb_cost}")
#
#     # Porównanie czasów dla różnych rozmiarów
#     print("\n" + "=" * 60)
#     print("PORÓWNANIE CZASÓW WYKONANIA")
#     print("=" * 60)
#
#     sizes_bruteforce = [5, 6, 7, 8, 9, 10] # max 12
#     sizes_bb = [5,6,7,8,9,10,11,12,13,14,16,17]
#     sizes_dp = [5,6,7,8,9,10,11,12,13,14,16,17]
#
#     print("\n--- Brute Force (małe instancje) ---")
#     for size in sizes_bruteforce:
#         matrix, _ = generate_tsp_data(size, size)
#         start_time = time.time()
#         cost, path = tsp_bruteforce(matrix)
#         elapsed = time.time() - start_time
#         print(f"n={size}: koszt={cost}, czas={elapsed:.6f} s")
#
#     print("\n--- Branch and Bound ---")
#     for size in sizes_bb:
#         matrix, _ = generate_tsp_data(size, size)
#         start_time = time.time()
#         cost, path = tsp_branch_and_bound(matrix)
#         elapsed = time.time() - start_time
#         print(f"n={size}: koszt={cost}, czas={elapsed:.6f} s")
#
#     print("\n--- Programowanie Dynamiczne ---")
#     for size in sizes_dp:
#         matrix, _ = generate_tsp_data(size, size)
#         start_time = time.time()
#         cost, path = tsp_dynamic_programming(matrix)
#         elapsed = time.time() - start_time
#         print(f"n={size}: koszt={cost}, czas={elapsed:.6f} s")
#
#     # KNN może działać na znacznie większych instancjach
#     sizes_nn = [5, 10, 20, 50, 100, 200, 500, 1000]
#
#     print("\n--- Nearest Neighbor (KNN) ---")
#     for size in sizes_nn:
#         matrix, _ = generate_tsp_data(size, size)
#         start_time = time.time()
#         cost, path = tsp_nearest_neighbor(matrix)
#         elapsed = time.time() - start_time
#         print(f"n={size}: koszt={cost}, czas={elapsed:.6f} s")
#
#     print("\n--- Nearest Neighbor Best (wszystkie starty) ---")
#     for size in sizes_nn:
#         matrix, _ = generate_tsp_data(size, size)
#         start_time = time.time()
#         cost, path = tsp_nearest_neighbor_best(matrix)
#         elapsed = time.time() - start_time
#         print(f"n={size}: koszt={cost}, czas={elapsed:.6f} s")
#
#     # Demonstracja wczytywania macierzy
#     print("\n" + "=" * 60)
#     print("DEMONSTRACJA WCZYTYWANIA MACIERZY")
#     print("=" * 60)
#
#     sample_data = """data: 10
#  0 24  4 40 96  6 59 40 90 76
#  4  0 95 14 65 37 26 20 11 38
# 17 62  0 96 60 61 52 41  7 81
# 82 82 52  0 39 11 12 43 10 29
# 57 73 67 80  0 27 67 43  1 16
# 89 85  1 49 24  0 23 86 53 97
# 90 96  8 75  6 15  0 79 46  7
# 90 60 87  6 12 46 98  0 14 48
# 35 79 77 83 15 41 85  1  0 17
# 34 45  5 17 92 38 86 62 53  0"""
#
#     loaded_matrix = load_cost_matrix_raw(sample_data)
#     print("\nWczytana macierz:")
#     print_matrix(loaded_matrix)
#
#     print("\n--- Rozwiązanie dla wczytanej macierzy ---")
#     start_time = time.time()
#     dp_cost, dp_path = tsp_dynamic_programming(loaded_matrix)
#     elapsed = time.time() - start_time
#     print(f"Koszt (DP): {dp_cost}")
#     print(f"Ścieżka: {dp_path}")
#     print(f"Czas: {elapsed:.6f} s")
#
#     start_time = time.time()
#     nn_cost, nn_path = tsp_nearest_neighbor(loaded_matrix)
#     elapsed = time.time() - start_time
#     print(f"\nKoszt (NN): {nn_cost}")
#     print(f"Ścieżka: {nn_path}")
#     print(f"Czas: {elapsed:.6f} s")
#
#     start_time = time.time()
#     nnb_cost, nnb_path = tsp_nearest_neighbor_best(loaded_matrix)
#     elapsed = time.time() - start_time
#     print(f"\nKoszt (NN Best): {nnb_cost}")
#     print(f"Ścieżka: {nnb_path}")
#     print(f"Czas: {elapsed:.6f} s")
#
#     start_time = time.time()
#     seq_cost, seq_path = tsp_123(loaded_matrix)
#     elapsed = time.time() - start_time
#     print(f"\nKoszt (Algorytm 123): {seq_cost}")
#     print(f"Ścieżka: {seq_path}")
#     print(f"Czas: {elapsed:.6f} s")
#
#     # Demonstracja wczytywania współrzędnych
#     print("\n" + "=" * 60)
#     print("DEMONSTRACJA WCZYTYWANIA WSPÓŁRZĘDNYCH")
#     print("=" * 60)

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

    # 2-opt
    start_time = time.time()
    opt2_cost, opt2_path = tsp_2opt(coords_matrix, nn_path)
    elapsed = time.time() - start_time
    print(f"\n2-opt (z NN):")
    print(f"Koszt: {opt2_cost}")
    print(f"Ścieżka: {opt2_path}")
    print(f"Czas: {elapsed:.6f} s")

    # Porównanie
    print(f"\n--- Porównanie dla danych ze współrzędnymi (n={len(coords)}) ---")
    print(f"Algorytm 123: {seq_cost}")
    print(f"Nearest Neighbor: {nn_cost} (poprawa o {seq_cost - nn_cost}, {100*(seq_cost - nn_cost)/seq_cost:.1f}%)")
    print(f"Nearest Neighbor Best: {nnb_cost} (poprawa o {seq_cost - nnb_cost}, {100*(seq_cost - nnb_cost)/seq_cost:.1f}%)")
    print(f"Farthest Insertion: {fi_cost} (poprawa o {seq_cost - fi_cost}, {100*(seq_cost - fi_cost)/seq_cost:.1f}%)")
    print(f"2-opt (z NN): {opt2_cost} (poprawa o {nn_cost - opt2_cost}, {100*(nn_cost - opt2_cost)/nn_cost:.1f}% względem NN)")
