"""
Moduł do benchmarkowania algorytmów TSP i generowania wykresów.
"""
import os
import time
import matplotlib.pyplot as plt

from data_utils import generate_tsp_data
from bruteforce import tsp_bruteforce
from branch_and_bound import tsp_branch_and_bound
from dynamic_programming import tsp_dynamic_programming
from nearest_neighbor import tsp_nearest_neighbor, tsp_nearest_neighbor_best
from sequential import tsp_123
from farthest_insertion import tsp_farthest_insertion
from two_opt import tsp_2opt


def ensure_output_dir(dirname="benchmarks"):
    """Tworzy folder na wykresy jeśli nie istnieje."""
    if not os.path.exists(dirname):
        os.makedirs(dirname)
    return dirname


def benchmark_algorithm(algorithm_func, sizes, seed_base=42, timeout=60, use_initial_path=False):
    """
    Benchmarkuje pojedynczy algorytm dla różnych rozmiarów instancji.
    
    Parametry:
        algorithm_func: funkcja algorytmu do testowania
        sizes: lista rozmiarów instancji
        seed_base: bazowy seed dla generatora
        timeout: maksymalny czas na pojedynczy test (sekundy)
        use_initial_path: czy algorytm wymaga początkowej ścieżki (dla 2-opt)
    
    Zwraca:
        dict z kluczami 'sizes' i 'times'
    """
    times = []
    actual_sizes = []
    
    for size in sizes:
        matrix, _ = generate_tsp_data(size, seed_base + size)
        
        try:
            if use_initial_path:
                # Dla 2-opt używamy ścieżki z nearest neighbor
                _, initial_path = tsp_nearest_neighbor(matrix)
                start_time = time.time()
                algorithm_func(matrix, initial_path)
                elapsed = time.time() - start_time
            else:
                start_time = time.time()
                algorithm_func(matrix)
                elapsed = time.time() - start_time
            
            if elapsed > timeout:
                print(f"  n={size}: przekroczono timeout ({timeout}s)")
                break
                
            times.append(elapsed)
            actual_sizes.append(size)
            print(f"  n={size}: {elapsed:.6f} s")
            
        except Exception as e:
            print(f"  n={size}: błąd - {e}")
            break
    
    return {'sizes': actual_sizes, 'times': times}


def plot_single_benchmark(results, algorithm_name, output_dir="benchmarks"):
    """Rysuje i zapisuje wykres dla pojedynczego algorytmu."""
    ensure_output_dir(output_dir)
    
    plt.figure(figsize=(10, 6))
    plt.plot(results['sizes'], results['times'], 'o-', linewidth=2, markersize=8)
    plt.xlabel('Rozmiar instancji (n)', fontsize=12)
    plt.ylabel('Czas wykonania [s]', fontsize=12)
    plt.title(f'Benchmark: {algorithm_name}', fontsize=14)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    
    filename = os.path.join(output_dir, f"benchmark_{algorithm_name.lower().replace(' ', '_').replace('-', '_')}.png")
    plt.savefig(filename, dpi=150)
    plt.close()
    print(f"  Zapisano wykres: {filename}")
    return filename


def plot_comparison(all_results, output_dir="benchmarks", title="Porównanie algorytmów TSP"):
    """Rysuje wykres porównawczy wszystkich algorytmów."""
    ensure_output_dir(output_dir)
    
    plt.figure(figsize=(12, 8))
    
    for name, results in all_results.items():
        if results['sizes']:
            plt.plot(results['sizes'], results['times'], 'o-', linewidth=2, markersize=6, label=name)
    
    plt.xlabel('Rozmiar instancji (n)', fontsize=12)
    plt.ylabel('Czas wykonania [s]', fontsize=12)
    plt.title(title, fontsize=14)
    plt.legend(loc='upper left')
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    
    filename = os.path.join(output_dir, "benchmark_comparison.png")
    plt.savefig(filename, dpi=150)
    plt.close()
    print(f"Zapisano wykres porównawczy: {filename}")
    return filename


def plot_comparison_log(all_results, output_dir="benchmarks", title="Porównanie algorytmów TSP (skala log)"):
    """Rysuje wykres porównawczy w skali logarytmicznej."""
    ensure_output_dir(output_dir)
    
    plt.figure(figsize=(12, 8))
    
    for name, results in all_results.items():
        if results['sizes'] and results['times']:
            plt.plot(results['sizes'], results['times'], 'o-', linewidth=2, markersize=6, label=name)
    
    plt.xlabel('Rozmiar instancji (n)', fontsize=12)
    plt.ylabel('Czas wykonania [s]', fontsize=12)
    plt.title(title, fontsize=14)
    plt.yscale('log')
    plt.legend(loc='upper left')
    plt.grid(True, alpha=0.3, which='both')
    plt.tight_layout()
    
    filename = os.path.join(output_dir, "benchmark_comparison_log.png")
    plt.savefig(filename, dpi=150)
    plt.close()
    print(f"Zapisano wykres porównawczy (log): {filename}")
    return filename


def run_all_benchmarks(output_dir="benchmarks"):
    """
    Uruchamia benchmarki dla wszystkich algorytmów i generuje wykresy.
    """
    ensure_output_dir(output_dir)
    all_results = {}
    
    # Algorytmy dokładne (małe instancje)
    print("\n" + "=" * 60)
    print("BENCHMARK: Brute Force")
    print("=" * 60)
    sizes_bf = [4, 5, 6, 7, 8, 9, 10, 11]
    results_bf = benchmark_algorithm(tsp_bruteforce, sizes_bf, timeout=30)
    plot_single_benchmark(results_bf, "Brute Force", output_dir)
    all_results["Brute Force"] = results_bf
    
    print("\n" + "=" * 60)
    print("BENCHMARK: Branch and Bound")
    print("=" * 60)
    sizes_bb = [4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
    results_bb = benchmark_algorithm(tsp_branch_and_bound, sizes_bb, timeout=30)
    plot_single_benchmark(results_bb, "Branch and Bound", output_dir)
    all_results["Branch and Bound"] = results_bb
    
    print("\n" + "=" * 60)
    print("BENCHMARK: Programowanie Dynamiczne (Held-Karp)")
    print("=" * 60)
    sizes_dp = [4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]
    results_dp = benchmark_algorithm(tsp_dynamic_programming, sizes_dp, timeout=30)
    plot_single_benchmark(results_dp, "Dynamic Programming", output_dir)
    all_results["Dynamic Programming"] = results_dp
    
    # Algorytmy heurystyczne (większe instancje)
    print("\n" + "=" * 60)
    print("BENCHMARK: Algorytm 123 (sekwencyjny)")
    print("=" * 60)
    # Dokładniejsze zagęszczenie największych rozmiarów (bez dużych skoków x2)
    sizes_heuristic = [10, 50, 100, 200, 500, 1000, 1500, 2000, 3000, 4000]
    results_123 = benchmark_algorithm(tsp_123, sizes_heuristic, timeout=60)
    plot_single_benchmark(results_123, "Algorytm 123", output_dir)
    all_results["Algorytm 123"] = results_123
    
    print("\n" + "=" * 60)
    print("BENCHMARK: Nearest Neighbor")
    print("=" * 60)
    results_nn = benchmark_algorithm(tsp_nearest_neighbor, sizes_heuristic, timeout=60)
    plot_single_benchmark(results_nn, "Nearest Neighbor", output_dir)
    all_results["Nearest Neighbor"] = results_nn
    
    print("\n" + "=" * 60)
    print("BENCHMARK: Nearest Neighbor Best")
    print("=" * 60)
    # Unikamy podwajania w ostatnim kroku (500 -> 1000)
    sizes_nnb = [10, 50, 100, 200, 500, 750, 1000]
    results_nnb = benchmark_algorithm(tsp_nearest_neighbor_best, sizes_nnb, timeout=60)
    plot_single_benchmark(results_nnb, "Nearest Neighbor Best", output_dir)
    all_results["Nearest Neighbor Best"] = results_nnb
    
    print("\n" + "=" * 60)
    print("BENCHMARK: Farthest Insertion")
    print("=" * 60)
    sizes_fi = [10, 50, 100, 200, 500, 750, 1000]
    results_fi = benchmark_algorithm(tsp_farthest_insertion, sizes_fi, timeout=60)
    plot_single_benchmark(results_fi, "Farthest Insertion", output_dir)
    all_results["Farthest Insertion"] = results_fi
    
    print("\n" + "=" * 60)
    print("BENCHMARK: 2-opt")
    print("=" * 60)
    sizes_2opt = [10, 50, 100, 200, 500, 750, 1000]
    results_2opt = benchmark_algorithm(tsp_2opt, sizes_2opt, timeout=60, use_initial_path=True)
    plot_single_benchmark(results_2opt, "2-opt", output_dir)
    all_results["2-opt"] = results_2opt
    
    # Wykresy porównawcze
    print("\n" + "=" * 60)
    print("GENEROWANIE WYKRESÓW PORÓWNAWCZYCH")
    print("=" * 60)
    
    # Porównanie algorytmów dokładnych
    exact_results = {
        "Brute Force": results_bf,
        "Branch and Bound": results_bb,
        "Dynamic Programming": results_dp
    }
    plot_comparison(exact_results, output_dir, "Porównanie algorytmów dokładnych")
    
    # Porównanie algorytmów heurystycznych
    heuristic_results = {
        "Algorytm 123": results_123,
        "Nearest Neighbor": results_nn,
        "Nearest Neighbor Best": results_nnb,
        "Farthest Insertion": results_fi,
        "2-opt": results_2opt
    }
    
    plt.figure(figsize=(12, 8))
    for name, results in heuristic_results.items():
        if results['sizes']:
            plt.plot(results['sizes'], results['times'], 'o-', linewidth=2, markersize=6, label=name)
    plt.xlabel('Rozmiar instancji (n)', fontsize=12)
    plt.ylabel('Czas wykonania [s]', fontsize=12)
    plt.title('Porównanie algorytmów heurystycznych', fontsize=14)
    plt.legend(loc='upper left')
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    filename = os.path.join(output_dir, "benchmark_heuristic_comparison.png")
    plt.savefig(filename, dpi=150)
    plt.close()
    print(f"Zapisano wykres: {filename}")
    
    # Wykres wszystkich algorytmów (skala log)
    plot_comparison_log(all_results, output_dir, "Porównanie wszystkich algorytmów (skala log)")
    
    print("\n" + "=" * 60)
    print(f"Wszystkie wykresy zapisane w folderze: {output_dir}/")
    print("=" * 60)
    
    return all_results


def run_quick_benchmark(output_dir="benchmarks"):
    """
    Szybki benchmark z mniejszymi instancjami (do szybkiego testowania).
    """
    ensure_output_dir(output_dir)
    all_results = {}
    
    print("\n" + "=" * 60)
    print("SZYBKI BENCHMARK")
    print("=" * 60)
    
    # Brute Force
    print("\nBrute Force:")
    sizes_bf = [4, 5, 6, 7, 8, 9]
    results_bf = benchmark_algorithm(tsp_bruteforce, sizes_bf, timeout=10)
    plot_single_benchmark(results_bf, "Brute Force", output_dir)
    all_results["Brute Force"] = results_bf
    
    # Branch and Bound
    print("\nBranch and Bound:")
    sizes_bb = [4, 5, 6, 7, 8, 9, 10, 11, 12]
    results_bb = benchmark_algorithm(tsp_branch_and_bound, sizes_bb, timeout=10)
    plot_single_benchmark(results_bb, "Branch and Bound", output_dir)
    all_results["Branch and Bound"] = results_bb
    
    # Dynamic Programming
    print("\nDynamic Programming:")
    sizes_dp = [4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
    results_dp = benchmark_algorithm(tsp_dynamic_programming, sizes_dp, timeout=10)
    plot_single_benchmark(results_dp, "Dynamic Programming", output_dir)
    all_results["Dynamic Programming"] = results_dp
    
    # Heurystyki (zagęszczone największe wartości)
    sizes_h = [10, 50, 100, 200, 300, 400, 500]
    
    print("\nAlgorytm 123:")
    results_123 = benchmark_algorithm(tsp_123, sizes_h, timeout=10)
    plot_single_benchmark(results_123, "Algorytm 123", output_dir)
    all_results["Algorytm 123"] = results_123
    
    print("\nNearest Neighbor:")
    results_nn = benchmark_algorithm(tsp_nearest_neighbor, sizes_h, timeout=10)
    plot_single_benchmark(results_nn, "Nearest Neighbor", output_dir)
    all_results["Nearest Neighbor"] = results_nn
    
    print("\nNearest Neighbor Best:")
    results_nnb = benchmark_algorithm(tsp_nearest_neighbor_best, sizes_h, timeout=10)
    plot_single_benchmark(results_nnb, "Nearest Neighbor Best", output_dir)
    all_results["Nearest Neighbor Best"] = results_nnb
    
    print("\nFarthest Insertion:")
    results_fi = benchmark_algorithm(tsp_farthest_insertion, sizes_h, timeout=10)
    plot_single_benchmark(results_fi, "Farthest Insertion", output_dir)
    all_results["Farthest Insertion"] = results_fi
    
    print("\n2-opt:")
    results_2opt = benchmark_algorithm(tsp_2opt, sizes_h, timeout=10, use_initial_path=True)
    plot_single_benchmark(results_2opt, "2-opt", output_dir)
    all_results["2-opt"] = results_2opt
    
    # Wykres porównawczy
    plot_comparison_log(all_results, output_dir)
    
    print(f"\nWykresy zapisane w: {output_dir}/")
    return all_results


if __name__ == "__main__":
    # Uruchom szybki benchmark jako domyślny
    run_quick_benchmark()

