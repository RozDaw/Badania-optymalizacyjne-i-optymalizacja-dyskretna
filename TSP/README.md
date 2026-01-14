# Problem komiwojażera (TSP) - Implementacja i badania

## Opis

Ten folder zawiera implementację różnych algorytmów rozwiązywania problemu komiwojażera (Traveling Salesman Problem, TSP) wraz z narzędziami do ich testowania i porównywania.

## Zaimplementowane algorytmy

### Algorytmy dokładne (dla małych instancji):
1. **Brute Force** - przegląd zupełny wszystkich permutacji
2. **Branch and Bound** - metoda podziału i ograniczeń
3. **Programowanie Dynamiczne** - algorytm Held-Karp

### Heurystyki konstrukcyjne:
4. **Algorytm sekwencyjny (123)** - odwiedzanie miast w kolejności numeracji (baseline)
5. **Nearest Neighbor** - algorytm najbliższego sąsiada
6. **Farthest Insertion** - algorytm wstawiania najdalszego

### Algorytmy poprawy:
7. **2-opt** - metoda lokalnego przeszukiwania (dla symetrycznego TSP)

### Metaheurystyki:
8. **Tabu Search** - przeszukiwanie tabu z pamięcią krótkookresową
9. **Simulated Annealing** - symulowane wyżarzanie

## Struktura projektu

```
TSP/
├── algorithms/           # Implementacje algorytmów
│   ├── sequential.py
│   ├── nearest_neighbor.py
│   ├── farthest_insertion.py
│   ├── two_opt.py
│   ├── tabu_search.py
│   ├── simulated_annealing.py
│   ├── bruteforce.py
│   ├── branch_and_bound.py
│   └── dynamic_programming.py
├── data_utils.py         # Narzędzia do generowania i wczytywania danych
├── main.py               # Główny moduł demonstracyjny
├── benchmark.py          # Moduł do benchmarkingu (wszystkie algorytmy)
├── run_experiments.py    # Skrypt do badań (wybrane algorytmy)
├── sprawozdanie/         # Sprawozdanie LaTeX
│   └── main.tex
└── README.md             # Ten plik
```

## Użycie

### Demonstracja algorytmów

Uruchom podstawową demonstrację wszystkich algorytmów:

```bash
python3 main.py
```

Demonstracja pokazuje:
- Algorytmy dokładne na małej macierzy (10 miast)
- Metaheurystyki na średniej macierzy (20 miast)
- Wszystkie algorytmy na danych z współrzędnymi (40 miast)

### Eksperymenty badawcze

Uruchom eksperymenty zgodnie z wymaganiami zadania (bez BnB, BF, DP):

```bash
python3 run_experiments.py
```

lub

```bash
python3 main.py --experiments
```

Eksperymenty obejmują algorytmy:
- Sekwencyjny
- Nearest Neighbor
- Farthest Insertion
- 2-opt
- Tabu Search
- Simulated Annealing

Wyniki zapisywane są w folderze `experiments/`:
- `results.json` - dane w formacie JSON
- `results_table.tex` - tabele LaTeX
- `time_comparison.png` - wykres porównawczy czasów
- `cost_comparison.png` - wykres porównawczy kosztów
- `time_comparison_log.png` - wykres w skali logarytmicznej

### Pełne benchmarki

Uruchom benchmarki wszystkich algorytmów z generowaniem wykresów:

```bash
python3 benchmark.py
```

lub

```bash
python3 main.py --benchmark
```

## Uwagi techniczne

### Asymetryczny TSP

Generowane macierze kosztów są **asymetryczne** (matrix[i][j] != matrix[j][i]), co odpowiada rzeczywistym scenariuszom z jednokierunkowymi ulicami lub różnymi kosztami przejazdu w różnych kierunkach.

**Konsekwencje:**
- Algorytm **2-opt** może dawać słabe wyniki (jest zaprojektowany dla symetrycznego TSP)
- **Tabu Search** i **Simulated Annealing** używają operatora **swap** (zamiana dwóch miast) zamiast 2-opt
- Operator swap działa poprawnie zarówno dla symetrycznego jak i asymetrycznego TSP

### Parametry metaheurystyk

#### Tabu Search
- `max_iterations` - liczba iteracji (domyślnie 1000)
- `tabu_size` - rozmiar listy tabu (domyślnie 10)
- Zalecane: tabu_size = 5-15, max_iterations = 500-5000

#### Simulated Annealing
- `initial_temp` - temperatura początkowa (adaptacyjna domyślnie)
- `cooling_rate` - współczynnik chłodzenia (domyślnie 0.995)
- `min_temp` - temperatura minimalna (domyślnie 0.1)
- Zalecane: cooling_rate = 0.995-0.999

## Sprawozdanie

Sprawozdanie LaTeX znajduje się w folderze `sprawozdanie/`:

```bash
cd sprawozdanie
pdflatex main.tex
pdflatex main.tex  # Drugi raz dla referencji
```

Sprawozdanie zawiera:
- Opis teoretyczny wszystkich algorytmów
- Pseudokody i złożoności obliczeniowe
- Analizę wyników eksperymentów
- Porównania wydajności i jakości rozwiązań
- Wnioski i zalecenia praktyczne
- Bibliografia

## Wymagania

- Python 3.7+
- matplotlib (do wykresów)
- numpy (opcjonalnie, dla niektórych obliczeń)

Instalacja zależności:

```bash
pip install matplotlib numpy
```

## Autorzy

- Konrad Pempera - 263948
- Dawid Różański - 263524

## Przykładowe wyniki

Przykładowe wyniki dla n=20:

| Algorytm | Czas [s] | Koszt | Względem NN |
|----------|----------|-------|-------------|
| Sekwencyjny | 0.0001 | 1250 | +250% |
| Nearest Neighbor | 0.0003 | 314 | 0% |
| Farthest Insertion | 0.0015 | 380 | +21% |
| 2-opt | 0.0010 | ~670* | +114%* |
| Tabu Search | 0.045 | 277 | -12% |
| Simulated Annealing | 0.038 | 314 | 0% |

*2-opt daje gorsze wyniki dla asymetrycznego TSP

## Dalsze usprawnienia

Możliwe kierunki rozwoju:
1. Implementacja Lin-Kernighan dla lepszej jakości
2. Algorytmy genetyczne
3. Ant Colony Optimization
4. Równoległe przetwarzanie metaheurystyk
5. Hybrydowe podejścia (GA + lokalne przeszukiwanie)
