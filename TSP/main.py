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

from TSP.algorithms.TSPSolver import  simulated_annealing
# Import funkcji pomocniczych
from data_utils import (
    tsp_rand,
    generate_tsp_data,
    load_cost_matrix,
    load_cost_matrix_raw,
    save_cost_matrix,
    load_coordinates_raw,
    print_matrix,
    verify_solution, generuj_macierz
)

# Import algorytmów
from algorithms.bruteforce import tsp_bruteforce
from algorithms.branch_and_bound import tsp_branch_and_bound
from algorithms.dynamic_programming import tsp_dynamic_programming
from algorithms.nearest_neighbor import tsp_nearest_neighbor, tsp_nearest_neighbor_best
from algorithms.sequential import tsp_123
from algorithms.farthest_insertion import tsp_farthest_insertion
from algorithms.two_opt import tsp_2opt
from algorithms.tabu_search import  tabu_search
from algorithms.simulated_annealing import tsp_simulated_annealing_fast



def run_comparison(seed, n, sequential = True, NN = True, farthest = True, opt2 = True, tabu = True, sa = True, isLogging = True):
    """Demonstracja metaheurystyk na losowej macierzy kosztów."""
    print("\n" + "=" * 60)
    print("Porównanie metod pod względem jakosci rozwiązań oraz czasu wykonania")
    print("=" * 60)


    size = n
    test_matrix, _ = generate_tsp_data(size, seed=seed)
    test_matrix = generuj_macierz(size, seed)
    print(f"\nMacierz testowa ({size}x{size})")

    results = {}
    if sequential:
    # Sequential
        print("\n--- Algorytm 123 ---")
        start_time = time.time()
        seq_cost, seq_path = tsp_123(test_matrix)
        seq_time = time.time() - start_time
        print(f"Koszt: {seq_cost}")
        print(f"Czas: {seq_time:.6f} s")
        results['Algorytm 123'] = (seq_cost, seq_time)

    if NN or opt2 or tabu or sa:
        if NN:
            print("\n--- Nearest Neighbor (baseline) ---")
            start_time = time.time()
        nn_cost, nn_path = tsp_nearest_neighbor(test_matrix)

        if NN:
            nn_time = time.time() - start_time
            print(f"Koszt: {nn_cost}")
            print(f"Czas: {nn_time:.6f} s")
            results['Nearest Neighbor'] = (nn_cost, nn_time)

    if farthest:
        # Farthest Insertion
        print("\n--- Farthest Insertion ---")
        start_time = time.time()
        fi_cost, fi_path = tsp_farthest_insertion(test_matrix)
        fi_time = time.time() - start_time
        print(f"Koszt: {fi_cost}")
        print(f"Czas: {fi_time:.6f} s")
        results['Farthest Insertion'] = (fi_cost, fi_time)

    if opt2:
        # 2-opt (z NN jako początkowa trasa)
        print("\n--- 2-opt (z Nearest Neighbor) ---")
        start_time = time.time()
        opt2_cost, opt2_path = tsp_2opt(test_matrix, nn_path)
        opt2_time = time.time() - start_time
        print(f"Koszt: {opt2_cost}")
        print(f"Czas: {opt2_time:.6f} s")
        results['2-opt'] = (opt2_cost, opt2_time)

    if tabu:
        # Tabu Search
        print("\n--- Tabu Search ---")
        max_iterations = n
        if n == 500:
            max_iterations = 50
        tabu_size = n // 2
        print(f"Parametry: max_iterations={max_iterations*100}, tabu_size={tabu_size}")
        start_time = time.time()
        # ts_cost, ts_path = tsp_tabu_search(test_matrix, nn_path, max_iterations=2000, tabu_size=30)
        _, ts_cost= tabu_search(nn_path, test_matrix, max_iter=max_iterations*100, kadencja_tabu=tabu_size)
        ts_time = time.time() - start_time
        print(f"Koszt: {ts_cost}")
        print(f"Czas: {ts_time:.6f} s")
        results['Tabu Search'] = (ts_cost, ts_time)

    if sa:
        print("\n--- SA ---")
        start_time = time.time()
        _, sa_cost = simulated_annealing(nn_path, test_matrix, temp_pocz=2000, temp_konc=0.01, alpha=0.9995)
        sa_time = time.time() - start_time
        print(f"Koszt: {sa_cost}")
        print(f"Czas: {sa_time:.6f} s")
        results['Simulated Annealing'] = (sa_cost, sa_time)
        # # Simulated Annealing
        # tspInstance = TSPInstance(distance_matrix=test_matrix)
        # solver = SimulatedAnnealingSolver()
        #
        # print("\n--- Simulated Annealing ---")
        # start_time = time.time()
        # x, y = solver.solve(tsp_instance=tspInstance, initial_solution=nn_path)
        # sa_time = time.time() - start_time
        # print(f"Koszt: {y}")
        # print(f"Czas: {sa_time:.6f} s")
        # results['Simulated Annealing'] = (int(y), sa_time)
    if isLogging:
        with open(f"comparison_results.csv", "a") as f:
            f.write("Metoda,n,seed,Koszt,Czas\n")
            for name, (cost, exec_time) in results.items():
                f.write(f"{name},{n},{seed},{cost},{exec_time:.6f}\n")

        print("\n" + "=" * 60)
        print("PORÓWNANIE")
        print("=" * 60)
        best = min(r[0] for r in results.values())


        for name, (cost, exec_time) in results.items():
            improvement = nn_cost - cost
            improvement_pct = 100 * improvement / nn_cost if nn_cost > 0 else 0
            diff_from_best = cost - best
            diff_from_best_pct = 100 * diff_from_best / best if best > 0 else 0
            print(f"{name:25s}: {cost:5d} (poprawa vs NN: {improvement_pct:+6.1f}%, "
                  f"różnica od best: {diff_from_best_pct:+5.1f}%) - {exec_time:.6f}s")

    return results




if __name__ == "__main__":
    if len(sys.argv) > 1:
        arg = sys.argv[1].lower()
    else:
        # for n in [5,10,50,75,100,200,300,400,500]:
        #     for i in range(1,10):
        #         run_comparison(i*10,n, sequential=False, farthest=False, opt2=False, tabu=True, sa=False, isLogging=True)
        run_comparison(1 * 10, 500, sequential=False, farthest=False, opt2=False, tabu=True, sa=False, isLogging=True)
