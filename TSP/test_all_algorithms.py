"""
Skrypt do testowania wszystkich sześciu algorytmów TSP.
Testuje algorytmy dla różnych rozmiarów instancji z powtórzeniami.
Wyniki zapisuje do pliku CSV.
"""
import os
import sys
import time
import csv
import matplotlib.pyplot as plt

# Dodaj ścieżkę do modułów algorytmów
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'algorithms'))

from data_utils import generate_tsp_data
from algorithms.sequential import tsp_123
from algorithms.nearest_neighbor import tsp_nearest_neighbor
from algorithms.farthest_insertion import tsp_farthest_insertion
from algorithms.two_opt import tsp_2opt
from algorithms.tabu_search import tsp_tabu_search
from algorithms.simulated_annealing import tsp_simulated_annealing_fast


# Lista wszystkich algorytmów do testowania
ALGORITHMS = [
    ("Sekwencyjny", tsp_123, False),
    ("Najbliższy Sąsiad", tsp_nearest_neighbor, False),
    ("Wstawianie Najdalsze", tsp_farthest_insertion, False),
    ("2-opt", tsp_2opt, True),  # Wymaga początkowej ścieżki
    ("Tabu Search", tsp_tabu_search, False),
    ("Simulated Annealing", tsp_simulated_annealing_fast, False),
]

# Rozmiary instancji do testowania
SIZES = [5, 10, 50, 75, 100, 150, 200, 300, 400, 500]

# Parametry testów
REPETITIONS = 5
TIMEOUT = 5.0  # sekundy


def test_algorithm(algorithm_func, algorithm_name, sizes, seed_base=42, 
                   timeout=TIMEOUT, repetitions=REPETITIONS, use_initial_path=False):
    """
    Testuje pojedynczy algorytm dla różnych rozmiarów instancji.
    
    Parametry:
        algorithm_func: funkcja algorytmu do testowania
        algorithm_name: nazwa algorytmu (dla logów)
        sizes: lista rozmiarów instancji
        seed_base: bazowy seed dla generatora
        timeout: maksymalny czas na pojedynczy test (sekundy)
        repetitions: liczba powtórzeń dla każdego rozmiaru
        use_initial_path: czy algorytm wymaga początkowej ścieżki
    
    Zwraca:
        dict z wynikami: {'sizes': [...], 'avg_times': [...], 'avg_costs': [...], 'success': bool}
    """
    results = {
        'algorithm': algorithm_name,
        'sizes': [],
        'avg_times': [],
        'avg_costs': [],
        'success': True
    }
    
    print(f"\n{'='*60}")
    print(f"TEST: {algorithm_name}")
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
                
                # Sprawdź timeout
                if elapsed > timeout:
                    print(f"  Powtórzenie {rep+1}/{repetitions}: przekroczono timeout ({timeout}s)")
                    print(f"  Przerwano testy dla n={size} i wyższych rozmiarów")
                    results['success'] = False
                    return results
                
                times_for_size.append(elapsed)
                costs_for_size.append(cost)
                print(f"  Powtórzenie {rep+1}/{repetitions}: {elapsed:.6f}s, koszt: {cost}")
                
            except Exception as e:
                print(f"  Powtórzenie {rep+1}/{repetitions}: błąd - {e}")
                print(f"  Przerwano testy dla n={size} i wyższych rozmiarów")
                results['success'] = False
                return results
        
        # Oblicz średni czas i średni koszt
        avg_time = sum(times_for_size) / len(times_for_size)
        avg_cost = sum(costs_for_size) / len(costs_for_size)
        results['sizes'].append(size)
        results['avg_times'].append(avg_time)
        results['avg_costs'].append(avg_cost)
        print(f"  Średni czas: {avg_time:.6f}s, średni koszt: {avg_cost:.1f}")
    
    return results


def plot_time_comparison(all_results, filename="test_times.png", 
                        title="Porównanie czasów wykonania algorytmów TSP"):
    """
    Rysuje i zapisuje wykres porównawczy czasów wykonania wszystkich algorytmów.
    """
    plt.figure(figsize=(12, 8))
    
    for result in all_results:
        name = result['algorithm']
        sizes = result['sizes']
        avg_times = result['avg_times']
        
        if sizes and avg_times:
            plt.plot(sizes, avg_times, 
                    marker='o', linewidth=2, markersize=6, 
                    label=name, alpha=0.8)
    
    plt.xlabel('Rozmiar instancji (n)', fontsize=14)
    plt.ylabel('Średni czas wykonania [s]', fontsize=14)
    plt.title(title, fontsize=16)
    plt.legend(loc='upper left', fontsize=11)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    
    # Zapisz wykres do pliku
    plt.savefig(filename, dpi=300)
    plt.close()
    print(f"Zapisano wykres czasów do: {filename}")


def plot_cost_comparison(all_results, filename="test_costs.png",
                         title="Porównanie kosztów rozwiązań algorytmów TSP"):
    """
    Rysuje i zapisuje wykres porównawczy kosztów rozwiązań wszystkich algorytmów.
    """
    plt.figure(figsize=(12, 8))
    
    for result in all_results:
        name = result['algorithm']
        sizes = result['sizes']
        avg_costs = result['avg_costs']
        
        if sizes and avg_costs:
            plt.plot(sizes, avg_costs, 
                    marker='o', linewidth=2, markersize=6, 
                    label=name, alpha=0.8)
    
    plt.xlabel('Rozmiar instancji (n)', fontsize=14)
    plt.ylabel('Średni koszt trasy', fontsize=14)
    plt.title(title, fontsize=16)
    plt.yscale('log')  # Skala logarytmiczna na osi Y
    plt.legend(loc='upper left', fontsize=11)
    plt.grid(True, alpha=0.3, which='both')  # Siatka dla obu skal (liniowej i logarytmicznej)
    plt.tight_layout()
    
    # Zapisz wykres do pliku
    plt.savefig(filename, dpi=300)
    plt.close()
    print(f"Zapisano wykres kosztów do: {filename}")


def save_results_to_csv(all_results, times_filename="test_times.csv", 
                       costs_filename="test_costs.csv"):
    """
    Zapisuje wyniki testów do dwóch plików CSV: jeden dla czasów, jeden dla kosztów.
    
    Format CSV:
    Algorytm, n=5, n=10, n=50, n=75, n=100, n=150, n=200, n=300, n=400, n=500
    """
    # Znajdź wszystkie rozmiary (może być różna liczba dla różnych algorytmów)
    all_sizes = set()
    for result in all_results:
        all_sizes.update(result['sizes'])
    all_sizes = sorted(all_sizes)
    
    # Zapisz czasy do CSV
    with open(times_filename, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        
        # Nagłówki
        header = ['Algorytm'] + [f'n={size}' for size in all_sizes]
        writer.writerow(header)
        
        # Dane dla każdego algorytmu
        for result in all_results:
            row = [result['algorithm']]
            for size in all_sizes:
                if size in result['sizes']:
                    idx = result['sizes'].index(size)
                    avg_time = result['avg_times'][idx]
                    row.append(f"{avg_time:.6f}")
                else:
                    row.append("-")  # Brak danych (timeout lub błąd)
            writer.writerow(row)
    
    # Zapisz koszty do CSV
    with open(costs_filename, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        
        # Nagłówki
        header = ['Algorytm'] + [f'n={size}' for size in all_sizes]
        writer.writerow(header)
        
        # Dane dla każdego algorytmu
        for result in all_results:
            row = [result['algorithm']]
            for size in all_sizes:
                if size in result['sizes']:
                    idx = result['sizes'].index(size)
                    avg_cost = result['avg_costs'][idx]
                    row.append(f"{avg_cost:.1f}")
                else:
                    row.append("-")  # Brak danych (timeout lub błąd)
            writer.writerow(row)
    
    print(f"\n{'='*60}")
    print(f"Wyniki czasów zapisane do: {times_filename}")
    print(f"Wyniki kosztów zapisane do: {costs_filename}")
    print(f"{'='*60}")


def run_all_tests():
    """
    Główna funkcja przeprowadzająca wszystkie testy.
    """
    print("\n" + "="*70)
    print("TESTY WSZYSTKICH ALGORYTMÓW TSP")
    print("="*70)
    print(f"Rozmiary instancji: {SIZES}")
    print(f"Liczba powtórzeń: {REPETITIONS}")
    print(f"Timeout: {TIMEOUT}s")
    print("="*70)
    
    all_results = []
    
    # Testuj każdy algorytm
    for algorithm_name, algorithm_func, use_initial_path in ALGORITHMS:
        result = test_algorithm(
            algorithm_func,
            algorithm_name,
            SIZES,
            seed_base=42,
            timeout=TIMEOUT,
            repetitions=REPETITIONS,
            use_initial_path=use_initial_path
        )
        all_results.append(result)
    
    # Zapisz wyniki do CSV
    save_results_to_csv(all_results)
    
    # Generuj wykresy
    print("\n" + "="*70)
    print("GENEROWANIE WYKRESÓW")
    print("="*70)
    plot_time_comparison(all_results)
    plot_cost_comparison(all_results)
    
    # Podsumowanie
    print("\n" + "="*70)
    print("PODSUMOWANIE")
    print("="*70)
    for result in all_results:
        status = "✓ Zakończono" if result['success'] else "✗ Przerwano"
        print(f"{result['algorithm']}: {status} ({len(result['sizes'])} rozmiarów)")
    
    print("\n" + "="*70)
    print("TESTY ZAKOŃCZONE")
    print("="*70)
    
    return all_results


if __name__ == "__main__":
    run_all_tests()

