"""
Skrypt do przeprowadzania badań algorytmów TSP.
Badane algorytmy: sekwencyjny, najbliższy sąsiad, wstawianie najdalsze, 
2-opt, Tabu Search i Simulated Annealing.
"""
import os
import sys
import time
import json
import matplotlib.pyplot as plt

# Dodaj ścieżkę do modułów algorytmów
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'algorithms'))

from data_utils import generate_tsp_data
from algorithms.sequential import tsp_123
from algorithms.nearest_neighbor import tsp_nearest_neighbor, tsp_nearest_neighbor_best
from algorithms.farthest_insertion import tsp_farthest_insertion
from algorithms.two_opt import tsp_2opt
from algorithms.tabu_search import tsp_tabu_search
from algorithms.simulated_annealing import tsp_simulated_annealing_fast


def ensure_output_dir(dirname="experiments"):
    """Tworzy folder na wyniki jeśli nie istnieje."""
    if not os.path.exists(dirname):
        os.makedirs(dirname)
    return dirname


def benchmark_algorithm(algorithm_func, algorithm_name, sizes, seed_base=42, 
                       timeout=120, repetitions=5, use_initial_path=False):
    """
    Benchmarkuje pojedynczy algorytm dla różnych rozmiarów instancji.
    
    Parametry:
        algorithm_func: funkcja algorytmu do testowania
        algorithm_name: nazwa algorytmu (dla logów)
        sizes: lista rozmiarów instancji
        seed_base: bazowy seed dla generatora
        timeout: maksymalny czas na pojedynczy test (sekundy)
        repetitions: liczba powtórzeń dla każdego rozmiaru
        use_initial_path: czy algorytm wymaga początkowej ścieżki
    
    Zwraca:
        dict z wynikami: sizes, times_avg, times_std, costs_avg, costs_std
    """
    times_all = {size: [] for size in sizes}
    costs_all = {size: [] for size in sizes}
    actual_sizes = []
    
    print(f"\n{'='*60}")
    print(f"BENCHMARK: {algorithm_name}")
    print(f"{'='*60}")
    
    for size in sizes:
        print(f"\nRozmiar n={size}:")
        times_for_size = []
        costs_for_size = []
        
        for rep in range(repetitions):
            matrix, _ = generate_tsp_data(size, seed_base + size * 100 + rep)
            
            try:
                if use_initial_path:
                    # Dla 2-opt używamy ścieżki z nearest neighbor
                    _, initial_path = tsp_nearest_neighbor(matrix)
                    start_time = time.time()
                    cost, path = algorithm_func(matrix, initial_path)
                    elapsed = time.time() - start_time
                else:
                    start_time = time.time()
                    cost, path = algorithm_func(matrix)
                    elapsed = time.time() - start_time
                
                if elapsed > timeout:
                    print(f"  Powtórzenie {rep+1}/{repetitions}: przekroczono timeout ({timeout}s)")
                    break
                
                times_for_size.append(elapsed)
                costs_for_size.append(cost)
                print(f"  Powtórzenie {rep+1}/{repetitions}: {elapsed:.4f}s, koszt: {cost}")
                
            except Exception as e:
                print(f"  Powtórzenie {rep+1}/{repetitions}: błąd - {e}")
                break
        
        # Jeśli udało się wykonać wszystkie powtórzenia
        if len(times_for_size) == repetitions:
            times_all[size] = times_for_size
            costs_all[size] = costs_for_size
            actual_sizes.append(size)
            
            avg_time = sum(times_for_size) / len(times_for_size)
            avg_cost = sum(costs_for_size) / len(costs_for_size)
            print(f"  Średnia: {avg_time:.4f}s, średni koszt: {avg_cost:.1f}")
        else:
            print(f"  Przerwano testy dla n={size}")
            break
    
    # Oblicz statystyki
    times_avg = []
    times_std = []
    costs_avg = []
    costs_std = []
    
    for size in actual_sizes:
        times = times_all[size]
        costs = costs_all[size]
        
        times_avg.append(sum(times) / len(times))
        costs_avg.append(sum(costs) / len(costs))
        
        if len(times) > 1:
            time_mean = times_avg[-1]
            cost_mean = costs_avg[-1]
            time_variance = sum((t - time_mean)**2 for t in times) / (len(times) - 1)
            cost_variance = sum((c - cost_mean)**2 for c in costs) / (len(costs) - 1)
            times_std.append(time_variance ** 0.5)
            costs_std.append(cost_variance ** 0.5)
        else:
            times_std.append(0)
            costs_std.append(0)
    
    return {
        'algorithm': algorithm_name,
        'sizes': actual_sizes,
        'times_avg': times_avg,
        'times_std': times_std,
        'costs_avg': costs_avg,
        'costs_std': costs_std,
        'raw_times': {size: times_all[size] for size in actual_sizes},
        'raw_costs': {size: costs_all[size] for size in actual_sizes}
    }


def plot_time_comparison(all_results, output_dir="experiments", 
                         title="Porównanie czasów wykonania algorytmów TSP"):
    """Rysuje wykres porównawczy czasów wykonania."""
    ensure_output_dir(output_dir)
    
    plt.figure(figsize=(12, 8))
    
    for results in all_results:
        name = results['algorithm']
        sizes = results['sizes']
        times_avg = results['times_avg']
        times_std = results['times_std']
        
        if sizes:
            plt.errorbar(sizes, times_avg, yerr=times_std, 
                        marker='o', linewidth=2, markersize=6, 
                        label=name, capsize=5, alpha=0.8)
    
    plt.xlabel('Rozmiar instancji (n)', fontsize=14)
    plt.ylabel('Czas wykonania [s]', fontsize=14)
    plt.title(title, fontsize=16)
    plt.legend(loc='upper left', fontsize=11)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    
    filename = os.path.join(output_dir, "time_comparison.png")
    plt.savefig(filename, dpi=300)
    plt.close()
    print(f"\nZapisano wykres: {filename}")
    return filename


def plot_cost_comparison(all_results, output_dir="experiments",
                         title="Porównanie jakości rozwiązań algorytmów TSP"):
    """Rysuje wykres porównawczy jakości rozwiązań."""
    ensure_output_dir(output_dir)
    
    plt.figure(figsize=(12, 8))
    
    for results in all_results:
        name = results['algorithm']
        sizes = results['sizes']
        costs_avg = results['costs_avg']
        costs_std = results['costs_std']
        
        if sizes:
            plt.errorbar(sizes, costs_avg, yerr=costs_std,
                        marker='o', linewidth=2, markersize=6,
                        label=name, capsize=5, alpha=0.8)
    
    plt.xlabel('Rozmiar instancji (n)', fontsize=14)
    plt.ylabel('Koszt trasy', fontsize=14)
    plt.title(title, fontsize=16)
    plt.legend(loc='upper left', fontsize=11)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    
    filename = os.path.join(output_dir, "cost_comparison.png")
    plt.savefig(filename, dpi=300)
    plt.close()
    print(f"Zapisano wykres: {filename}")
    return filename


def plot_time_log_scale(all_results, output_dir="experiments"):
    """Rysuje wykres czasów w skali logarytmicznej."""
    ensure_output_dir(output_dir)
    
    plt.figure(figsize=(12, 8))
    
    for results in all_results:
        name = results['algorithm']
        sizes = results['sizes']
        times_avg = results['times_avg']
        
        if sizes:
            plt.plot(sizes, times_avg, 
                    marker='o', linewidth=2, markersize=6, 
                    label=name, alpha=0.8)
    
    plt.xlabel('Rozmiar instancji (n)', fontsize=14)
    plt.ylabel('Czas wykonania [s] (skala log)', fontsize=14)
    plt.title('Porównanie czasów wykonania (skala logarytmiczna)', fontsize=16)
    plt.yscale('log')
    plt.legend(loc='upper left', fontsize=11)
    plt.grid(True, alpha=0.3, which='both')
    plt.tight_layout()
    
    filename = os.path.join(output_dir, "time_comparison_log.png")
    plt.savefig(filename, dpi=300)
    plt.close()
    print(f"Zapisano wykres: {filename}")
    return filename


def save_results_json(all_results, output_dir="experiments"):
    """Zapisuje wyniki do pliku JSON."""
    ensure_output_dir(output_dir)
    
    filename = os.path.join(output_dir, "results.json")
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(all_results, f, indent=2, ensure_ascii=False)
    print(f"Zapisano wyniki do: {filename}")


def save_results_tex_table(all_results, output_dir="experiments"):
    """Generuje tabelę LaTeX z wynikami."""
    ensure_output_dir(output_dir)
    
    # Znajdź wszystkie rozmiary
    all_sizes = set()
    for results in all_results:
        all_sizes.update(results['sizes'])
    all_sizes = sorted(all_sizes)
    
    filename = os.path.join(output_dir, "results_table.tex")
    with open(filename, 'w', encoding='utf-8') as f:
        f.write("\\begin{table}[h]\n")
        f.write("\\centering\n")
        f.write("\\caption{Wyniki eksperymentów - czas wykonania [s]}\n")
        f.write("\\begin{tabular}{|c|" + "c|" * len(all_results) + "}\n")
        f.write("\\hline\n")
        
        # Nagłówki
        f.write("$n$ & " + " & ".join(r['algorithm'] for r in all_results) + " \\\\\n")
        f.write("\\hline\n")
        
        # Dane
        for size in all_sizes:
            row = [str(size)]
            for results in all_results:
                if size in results['sizes']:
                    idx = results['sizes'].index(size)
                    time_avg = results['times_avg'][idx]
                    row.append(f"{time_avg:.4f}")
                else:
                    row.append("-")
            f.write(" & ".join(row) + " \\\\\n")
        
        f.write("\\hline\n")
        f.write("\\end{tabular}\n")
        f.write("\\label{tab:time_results}\n")
        f.write("\\end{table}\n")
        
        # Druga tabela - jakość rozwiązań
        f.write("\n\n")
        f.write("\\begin{table}[h]\n")
        f.write("\\centering\n")
        f.write("\\caption{Wyniki eksperymentów - koszt trasy}\n")
        f.write("\\begin{tabular}{|c|" + "c|" * len(all_results) + "}\n")
        f.write("\\hline\n")
        
        # Nagłówki
        f.write("$n$ & " + " & ".join(r['algorithm'] for r in all_results) + " \\\\\n")
        f.write("\\hline\n")
        
        # Dane
        for size in all_sizes:
            row = [str(size)]
            for results in all_results:
                if size in results['sizes']:
                    idx = results['sizes'].index(size)
                    cost_avg = results['costs_avg'][idx]
                    row.append(f"{cost_avg:.1f}")
                else:
                    row.append("-")
            f.write(" & ".join(row) + " \\\\\n")
        
        f.write("\\hline\n")
        f.write("\\end{tabular}\n")
        f.write("\\label{tab:cost_results}\n")
        f.write("\\end{table}\n")
    
    print(f"Zapisano tabele LaTeX do: {filename}")


def run_experiments():
    """
    Główna funkcja przeprowadzająca eksperymenty.
    """
    output_dir = ensure_output_dir("experiments")
    all_results = []
    
    # Rozmiary instancji do testowania
    # Dla algorytmów heurystycznych możemy testować większe instancje
    sizes_small = [10, 20, 30, 40, 50]
    sizes_medium = [10, 50, 100, 150, 200]
    sizes_large = [10, 50, 100, 200, 300, 500]
    
    # 1. Algorytm sekwencyjny (bardzo szybki - największe instancje)
    print("\n" + "="*70)
    print("Algorytm 1: Sekwencyjny (123)")
    print("="*70)
    results_seq = benchmark_algorithm(
        tsp_123, "Sekwencyjny", sizes_large, 
        timeout=60, repetitions=5
    )
    all_results.append(results_seq)
    
    # 2. Nearest Neighbor (szybki)
    print("\n" + "="*70)
    print("Algorytm 2: Najbliższy Sąsiad")
    print("="*70)
    results_nn = benchmark_algorithm(
        tsp_nearest_neighbor, "Najbliższy Sąsiad", sizes_large,
        timeout=60, repetitions=5
    )
    all_results.append(results_nn)
    
    # 3. Farthest Insertion (wolniejszy)
    print("\n" + "="*70)
    print("Algorytm 3: Wstawianie Najdalsze")
    print("="*70)
    results_fi = benchmark_algorithm(
        tsp_farthest_insertion, "Wstawianie Najdalsze", sizes_medium,
        timeout=60, repetitions=5
    )
    all_results.append(results_fi)
    
    # 4. 2-opt (wymaga początkowej ścieżki)
    print("\n" + "="*70)
    print("Algorytm 4: 2-opt")
    print("="*70)
    results_2opt = benchmark_algorithm(
        tsp_2opt, "2-opt", sizes_medium,
        timeout=60, repetitions=5, use_initial_path=True
    )
    all_results.append(results_2opt)
    
    # 5. Tabu Search
    print("\n" + "="*70)
    print("Algorytm 5: Tabu Search")
    print("="*70)
    results_tabu = benchmark_algorithm(
        tsp_tabu_search, "Tabu Search", sizes_small,
        timeout=120, repetitions=3
    )
    all_results.append(results_tabu)
    
    # 6. Simulated Annealing
    print("\n" + "="*70)
    print("Algorytm 6: Simulated Annealing")
    print("="*70)
    results_sa = benchmark_algorithm(
        tsp_simulated_annealing_fast, "Simulated Annealing", sizes_small,
        timeout=120, repetitions=3
    )
    all_results.append(results_sa)
    
    # Zapisz wyniki
    print("\n" + "="*70)
    print("ZAPISYWANIE WYNIKÓW")
    print("="*70)
    
    save_results_json(all_results, output_dir)
    save_results_tex_table(all_results, output_dir)
    
    # Generuj wykresy
    print("\n" + "="*70)
    print("GENEROWANIE WYKRESÓW")
    print("="*70)
    
    plot_time_comparison(all_results, output_dir)
    plot_cost_comparison(all_results, output_dir)
    plot_time_log_scale(all_results, output_dir)
    
    print("\n" + "="*70)
    print("EKSPERYMENTY ZAKOŃCZONE")
    print(f"Wszystkie wyniki zapisane w: {output_dir}/")
    print("="*70)
    
    return all_results


if __name__ == "__main__":
    run_experiments()
