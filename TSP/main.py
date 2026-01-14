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
8. Tabu Search (przeszukiwanie tabu)
9. Simulated Annealing (symulowane wyżarzanie)

Użycie:
    python main.py              - uruchom demonstrację algorytmów
    python main.py --benchmark  - uruchom benchmarki z wykresami
    python main.py --experiments - uruchom eksperymenty badawcze (tylko wybrane algorytmy)
"""
import sys
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
from algorithms.bruteforce import tsp_bruteforce
from algorithms.branch_and_bound import tsp_branch_and_bound
from algorithms.dynamic_programming import tsp_dynamic_programming
from algorithms.nearest_neighbor import tsp_nearest_neighbor, tsp_nearest_neighbor_best
from algorithms.sequential import tsp_123
from algorithms.farthest_insertion import tsp_farthest_insertion
from algorithms.two_opt import tsp_2opt
from algorithms.tabu_search import tsp_tabu_search
from algorithms.simulated_annealing import tsp_simulated_annealing_fast


def run_demo_random_matrix():
    """Demonstracja algorytmów na losowej macierzy kosztów."""
    print("=" * 60)
    print("DEMONSTRACJA NA LOSOWEJ MACIERZY KOSZTÓW")
    print("=" * 60)
    
    # Generuj macierz testową
    size = 10
    test_matrix, _ = generate_tsp_data(size, seed=42)
    print(f"\nMacierz testowa ({size}x{size}):")
    print_matrix(test_matrix)
    
    results = {}
    
    # Brute Force
    print("\n--- Brute Force ---")
    start_time = time.time()
    bf_cost, bf_path = tsp_bruteforce(test_matrix)
    bf_time = time.time() - start_time
    print(f"Koszt: {bf_cost}")
    print(f"Ścieżka: {bf_path}")
    print(f"Czas: {bf_time:.6f} s")
    results['Brute Force'] = (bf_cost, bf_path, bf_time)
    
    # Branch and Bound
    print("\n--- Branch and Bound ---")
    start_time = time.time()
    bb_cost, bb_path = tsp_branch_and_bound(test_matrix)
    bb_time = time.time() - start_time
    print(f"Koszt: {bb_cost}")
    print(f"Ścieżka: {bb_path}")
    print(f"Czas: {bb_time:.6f} s")
    results['Branch and Bound'] = (bb_cost, bb_path, bb_time)
    
    # Programowanie dynamiczne
    print("\n--- Programowanie Dynamiczne (Held-Karp) ---")
    start_time = time.time()
    dp_cost, dp_path = tsp_dynamic_programming(test_matrix)
    dp_time = time.time() - start_time
    print(f"Koszt: {dp_cost}")
    print(f"Ścieżka: {dp_path}")
    print(f"Czas: {dp_time:.6f} s")
    results['Dynamic Programming'] = (dp_cost, dp_path, dp_time)
    
    # Algorytm 123
    print("\n--- Algorytm 123 (sekwencyjny) ---")
    start_time = time.time()
    seq_cost, seq_path = tsp_123(test_matrix)
    seq_time = time.time() - start_time
    print(f"Koszt: {seq_cost}")
    print(f"Ścieżka: {seq_path}")
    print(f"Czas: {seq_time:.6f} s")
    results['Algorytm 123'] = (seq_cost, seq_path, seq_time)
    
    # Nearest Neighbor
    print("\n--- Nearest Neighbor ---")
    start_time = time.time()
    nn_cost, nn_path = tsp_nearest_neighbor(test_matrix)
    nn_time = time.time() - start_time
    print(f"Koszt: {nn_cost}")
    print(f"Ścieżka: {nn_path}")
    print(f"Czas: {nn_time:.6f} s")
    results['Nearest Neighbor'] = (nn_cost, nn_path, nn_time)
    
    # Nearest Neighbor Best
    print("\n--- Nearest Neighbor Best ---")
    start_time = time.time()
    nnb_cost, nnb_path = tsp_nearest_neighbor_best(test_matrix)
    nnb_time = time.time() - start_time
    print(f"Koszt: {nnb_cost}")
    print(f"Ścieżka: {nnb_path}")
    print(f"Czas: {nnb_time:.6f} s")
    results['Nearest Neighbor Best'] = (nnb_cost, nnb_path, nnb_time)
    
    # Farthest Insertion
    print("\n--- Farthest Insertion ---")
    start_time = time.time()
    fi_cost, fi_path = tsp_farthest_insertion(test_matrix)
    fi_time = time.time() - start_time
    print(f"Koszt: {fi_cost}")
    print(f"Ścieżka: {fi_path}")
    print(f"Czas: {fi_time:.6f} s")
    results['Farthest Insertion'] = (fi_cost, fi_path, fi_time)
    
    # 2-opt (z NN jako początkowa trasa)
    print("\n--- 2-opt (z Nearest Neighbor) ---")
    start_time = time.time()
    opt2_cost, opt2_path = tsp_2opt(test_matrix, nn_path)
    opt2_time = time.time() - start_time
    print(f"Koszt: {opt2_cost}")
    print(f"Ścieżka: {opt2_path}")
    print(f"Czas: {opt2_time:.6f} s")
    results['2-opt'] = (opt2_cost, opt2_path, opt2_time)
    
    # Weryfikacja rozwiązań
    print("\n" + "=" * 60)
    print("WERYFIKACJA ROZWIĄZAŃ")
    print("=" * 60)
    for name, (cost, path, _) in results.items():
        status = "OK" if verify_solution(test_matrix, path, cost) else "BŁĄD"
        print(f"{name}: {status}")
    
    # Porównanie kosztów
    print("\n" + "=" * 60)
    print("PORÓWNANIE KOSZTÓW")
    print("=" * 60)
    optimal_cost = dp_cost  # DP daje rozwiązanie optymalne
    print(f"Koszt optymalny: {optimal_cost}")
    print()
    for name, (cost, _, exec_time) in results.items():
        if optimal_cost > 0:
            diff = cost - optimal_cost
            diff_pct = 100 * diff / optimal_cost
            print(f"{name:25s}: {cost:5d} (różnica: {diff:+4d}, {diff_pct:+6.1f}%) - {exec_time:.6f}s")
        else:
            print(f"{name:25s}: {cost:5d} - {exec_time:.6f}s")
    
    return results


def run_demo_metaheuristics():
    """Demonstracja metaheurystyk na losowej macierzy kosztów."""
    print("\n" + "=" * 60)
    print("DEMONSTRACJA METAHEURYSTYK (Tabu Search & Simulated Annealing)")
    print("=" * 60)
    
    # Generuj macierz testową
    size = 20
    test_matrix, _ = generate_tsp_data(size, seed=42)
    print(f"\nMacierz testowa ({size}x{size})")
    
    results = {}
    
    # Nearest Neighbor jako baseline
    print("\n--- Nearest Neighbor (baseline) ---")
    start_time = time.time()
    nn_cost, nn_path = tsp_nearest_neighbor(test_matrix)
    nn_time = time.time() - start_time
    print(f"Koszt: {nn_cost}")
    print(f"Czas: {nn_time:.6f} s")
    results['Nearest Neighbor'] = (nn_cost, nn_path, nn_time)
    
    # Tabu Search
    print("\n--- Tabu Search ---")
    print("Parametry: max_iterations=200, tabu_size=10")
    start_time = time.time()
    ts_cost, ts_path = tsp_tabu_search(test_matrix, nn_path, max_iterations=200, tabu_size=10)
    ts_time = time.time() - start_time
    print(f"Koszt: {ts_cost}")
    print(f"Czas: {ts_time:.6f} s")
    results['Tabu Search'] = (ts_cost, ts_path, ts_time)
    
    # Simulated Annealing
    print("\n--- Simulated Annealing ---")
    start_time = time.time()
    sa_cost, sa_path = tsp_simulated_annealing_fast(test_matrix, nn_path)
    sa_time = time.time() - start_time
    print(f"Koszt: {sa_cost}")
    print(f"Czas: {sa_time:.6f} s")
    results['Simulated Annealing'] = (sa_cost, sa_path, sa_time)
    
    # Porównanie
    print("\n" + "=" * 60)
    print("PORÓWNANIE METAHEURYSTYK")
    print("=" * 60)
    baseline = nn_cost
    best = min(r[0] for r in results.values())
    print(f"Koszt bazowy (NN): {baseline}")
    print(f"Najlepszy koszt: {best}")
    print()
    for name, (cost, _, exec_time) in results.items():
        improvement = baseline - cost
        improvement_pct = 100 * improvement / baseline if baseline > 0 else 0
        diff_from_best = cost - best
        diff_from_best_pct = 100 * diff_from_best / best if best > 0 else 0
        print(f"{name:25s}: {cost:5d} (poprawa vs NN: {improvement_pct:+6.1f}%, " 
              f"różnica od best: {diff_from_best_pct:+5.1f}%) - {exec_time:.6f}s")
    
    return results


def run_demo_coordinates():
    """Demonstracja algorytmów na danych ze współrzędnymi."""
    print("\n" + "=" * 60)
    print("DEMONSTRACJA NA DANYCH ZE WSPÓŁRZĘDNYMI")
    print("=" * 60)
    
    coords_data = """data:
40
97 35   57 36   29 23   57 39   18  7   92  7   29 41   26 42   94 11   55 26   49 47   98 11   29 25   96  7   64 37   26 31   93  9   28  1   15 26   74 47   75 16   10 44   30 48    8 43   34 45   31 46   95 29   55 38   84 45   60  4    3 16    7 21   81 16   37 30   27 28   66 43    2 46    8 46   53 18   36  3   
"""

    coords_matrix, coords = load_coordinates_raw(coords_data)
    print(f"\nWczytano {len(coords)} miast ze współrzędnymi")
    
    results = {}
    
    # Algorytm 123
    print("\n--- Algorytm 123 ---")
    start_time = time.time()
    seq_cost, seq_path = tsp_123(coords_matrix)
    elapsed = time.time() - start_time
    print(f"Koszt: {seq_cost}, Czas: {elapsed:.6f} s")
    results['Algorytm 123'] = (seq_cost, seq_path, elapsed)

    # Nearest Neighbor
    print("\n--- Nearest Neighbor ---")
    start_time = time.time()
    nn_cost, nn_path = tsp_nearest_neighbor(coords_matrix)
    elapsed = time.time() - start_time
    print(f"Koszt: {nn_cost}, Czas: {elapsed:.6f} s")
    results['Nearest Neighbor'] = (nn_cost, nn_path, elapsed)

    # Nearest Neighbor Best
    print("\n--- Nearest Neighbor Best ---")
    start_time = time.time()
    nnb_cost, nnb_path = tsp_nearest_neighbor_best(coords_matrix)
    elapsed = time.time() - start_time
    print(f"Koszt: {nnb_cost}, Czas: {elapsed:.6f} s")
    results['Nearest Neighbor Best'] = (nnb_cost, nnb_path, elapsed)

    # Farthest Insertion
    print("\n--- Farthest Insertion ---")
    start_time = time.time()
    fi_cost, fi_path = tsp_farthest_insertion(coords_matrix)
    elapsed = time.time() - start_time
    print(f"Koszt: {fi_cost}, Czas: {elapsed:.6f} s")
    results['Farthest Insertion'] = (fi_cost, fi_path, elapsed)

    # 2-opt
    print("\n--- 2-opt (z Nearest Neighbor) ---")
    start_time = time.time()
    opt2_cost, opt2_path = tsp_2opt(coords_matrix, nn_path)
    elapsed = time.time() - start_time
    print(f"Koszt: {opt2_cost}, Czas: {elapsed:.6f} s")
    results['2-opt'] = (opt2_cost, opt2_path, elapsed)

    # Porównanie
    print(f"\n--- Porównanie (n={len(coords)}) ---")
    baseline = seq_cost
    for name, (cost, _, exec_time) in results.items():
        improvement = baseline - cost
        improvement_pct = 100 * improvement / baseline if baseline > 0 else 0
        print(f"{name:25s}: {cost:5d} (poprawa: {improvement:+4d}, {improvement_pct:+6.1f}%)")
    
    return results


def run_benchmarks():
    """Uruchamia pełne benchmarki z wykresami."""
    from benchmark import run_all_benchmarks
    run_all_benchmarks()


def run_experiments():
    """Uruchamia eksperymenty badawcze."""
    from run_experiments import run_experiments as run_exp
    run_exp()


def print_help():
    """Wyświetla pomoc."""
    print(__doc__)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        arg = sys.argv[1].lower()
        if arg in ['--benchmark', '-b', 'benchmark']:
            run_benchmarks()
        elif arg in ['--experiments', '-e', 'experiments']:
            run_experiments()
        elif arg in ['--help', '-h', 'help']:
            print_help()
        else:
            print(f"Nieznany argument: {arg}")
            print_help()
    else:
        # Domyślnie uruchom demonstracje
        run_demo_random_matrix()
        run_demo_metaheuristics()
        run_demo_coordinates()
        
        print("\n" + "=" * 60)
        print("Aby uruchomić benchmarki z wykresami:")
        print("  python main.py --benchmark")
        print()
        print("Aby uruchomić eksperymenty badawcze:")
        print("  python main.py --experiments")
        print("=" * 60)

