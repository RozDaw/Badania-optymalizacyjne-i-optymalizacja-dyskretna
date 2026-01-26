# """
# Algorytm Tabu Search dla TSP.
#
# Referencja: https://en.wikipedia.org/wiki/Tabu_search
# """
# import random
# from collections import deque
#
#
# def tsp_tabu_search(matrix, initial_path=None, max_iterations=None, tabu_size=None):
#     """
#     Rozwiązuje TSP metodą przeszukiwania tabu (Tabu Search).
#
#     Tabu Search to algorytm metaheurystyczny, który wykorzystuje lokalną
#     pamięć przeszukiwania (listę tabu) do unikania cykli i eksploracji
#     nowych obszarów przestrzeni rozwiązań.
#
#     Używa 2-opt moves jako sąsiedztwa i sprawdza wszystkie możliwe ruchy
#     w każdej iteracji (best improvement strategy).
#
#     Parametry:
#         matrix: macierz kosztów przejść między miastami
#         initial_path: opcjonalna początkowa trasa
#         max_iterations: maksymalna liczba iteracji algorytmu
#         tabu_size: rozmiar listy tabu
#
#     Zwraca:
#         (koszt_najlepszej_trasy, najlepsza_trasa)
#     """
#     n = len(matrix)
#     if n == 0:
#         return 0, []
#     if n == 1:
#         return 0, [0, 0]
#     if n == 2:
#         return matrix[0][1] + matrix[1][0], [0, 1, 0]
#
#     # Inicjalizacja początkowej trasy
#     if initial_path is None:
#         # Użyj Nearest Neighbor jako dobrego rozwiązania początkowego
#         from algorithms.nearest_neighbor import tsp_nearest_neighbor
#         _, initial_path = tsp_nearest_neighbor(matrix)
#
#     # Usuń ostatni element jeśli jest powtórzeniem pierwszego
#     if len(initial_path) > n and initial_path[-1] == initial_path[0]:
#         tour = list(initial_path[:-1])
#     else:
#         tour = list(initial_path)
#
#     def calculate_tour_cost(t):
#         """Oblicza koszt trasy (cyklu)."""
#         cost = 0
#         for i in range(len(t)):
#             cost += matrix[t[i]][t[(i + 1) % len(t)]]
#         return cost
#
#     def two_opt_swap(t, i, j):
#         """Wykonuje 2-opt swap: odwraca segment od i+1 do j."""
#         return t[:i+1] + t[i+1:j+1][::-1] + t[j+1:]
#
#     # Parametry domyślne - adaptacyjne w zależności od rozmiaru
#     # Zwiększona liczba iteracji dla lepszych wyników (wolniejsze, ale lepsze)
#     if max_iterations is None:
#         if n > 200:
#             max_iterations = min(500, n * 5)
#         elif n > 100:
#             max_iterations = min(800, n * 8)
#         elif n > 50:
#             max_iterations = min(1000, n * 10)
#         else:
#             max_iterations = min(1500, n * 15)
#
#     if tabu_size is None:
#         tabu_size = max(7, min(n, 20))
#
#     current_tour = tour
#     current_cost = calculate_tour_cost(current_tour)
#     initial_cost = current_cost
#
#     best_tour = list(current_tour)
#     best_cost = current_cost
#
#     # Lista tabu - przechowuje pary (i, j) reprezentujące 2-opt moves
#     tabu_list = deque(maxlen=tabu_size)
#     tabu_set = set()
#
#     # Licznik iteracji bez globalnej poprawy - zwiększony dla większej eksploracji
#     no_improvement_count = 0
#     max_no_improvement = max(max_iterations, n * 2)
#     i = 0
#     for iteration in range(max_iterations):
#
#         best_move = None
#         best_move_cost = float('inf')
#         best_i, best_j = -1, -1
#
#         # Dla dużych n, sprawdzamy tylko próbkę swapów dla wydajności
#         # Dla małych n sprawdzamy wszystkie
#         if n > 50:
#             # Losowa próbka swapów - ograniczona liczba dla wydajności
#             # Dla większych n zmniejszamy liczbę próbek
#             if n > 150:
#                 num_samples = min(n * 5, 1000)
#             elif n > 100:
#                 num_samples = min(n * 7, 1500)
#             else:
#                 num_samples = min(n * 10, (n * (n - 1)) // 2)
#             moves_to_check = []
#
#             # Generuj losową próbkę unikalnych swapów
#             seen = set()
#             attempts = 0
#             max_attempts = num_samples * 10  # Ograniczenie prób
#
#             while len(moves_to_check) < num_samples and attempts < max_attempts:
#                 i = random.randint(0, n - 2)
#                 # j musi być co najmniej i+2 i maksymalnie n-1
#                 if i + 2 > n - 1:
#                     attempts += 1
#                     continue
#                 j = random.randint(i + 2, n - 1)
#                 if i == 0 and j == n - 1:
#                     continue
#                 move = (i, j)
#                 if move not in seen:
#                     seen.add(move)
#                     moves_to_check.append((i, j))
#                 attempts += 1
#         else:
#             # Dla małych n - wszystkie możliwe swapy
#             moves_to_check = []
#             for i in range(n - 1):
#                 for j in range(i + 2, n):
#                     if i == 0 and j == n - 1:
#                         continue
#                     moves_to_check.append((i, j))
#
#         # Przeglądaj wybrane swapy
#         for i, j in moves_to_check:
#             new_tour = two_opt_swap(current_tour, i, j)
#             new_cost = calculate_tour_cost(new_tour)
#
#             move = (i, j)
#             is_tabu = move in tabu_set
#
#             # Kryterium aspiracji: pozwól na ruch z listy tabu,
#             # jeśli prowadzi do najlepszego dotychczas rozwiązania
#             aspiration = new_cost < best_cost
#
#             if (not is_tabu or aspiration) and new_cost < best_move_cost:
#                 best_move = move
#                 best_move_cost = new_cost
#                 best_i, best_j = i, j
#
#         if best_move is None:
#             # Jeśli nie ma dozwolonego ruchu, wybierz najlepszy nawet z tabu
#             # Dla dużych n sprawdzamy tylko próbkę
#             if n > 50:
#                 # Sprawdź losową próbkę
#                 for _ in range(min(100, len(moves_to_check))):
#                     if not moves_to_check:
#                         break
#                     i, j = random.choice(moves_to_check)
#                     new_tour = two_opt_swap(current_tour, i, j)
#                     new_cost = calculate_tour_cost(new_tour)
#                     if new_cost < best_move_cost:
#                         best_move = (i, j)
#                         best_move_cost = new_cost
#                         best_i, best_j = i, j
#             else:
#                 # Dla małych n sprawdź wszystkie
#                 for i in range(n - 1):
#                     for j in range(i + 2, n):
#                         if i == 0 and j == n - 1:
#                             continue
#                         new_tour = two_opt_swap(current_tour, i, j)
#                         new_cost = calculate_tour_cost(new_tour)
#                         if new_cost < best_move_cost:
#                             best_move = (i, j)
#                             best_move_cost = new_cost
#                             best_i, best_j = i, j
#
#         if best_move is None:
#             break  # Brak możliwych ruchów
#
#         # Wykonaj ruch
#         current_tour = two_opt_swap(current_tour, best_i, best_j)
#         current_cost = best_move_cost
#
#         # Dodaj ruch do listy tabu
#         if best_move in tabu_set:
#             # Usuń stary wpis
#             tabu_list = deque([m for m in tabu_list if m != best_move], maxlen=tabu_size)
#             tabu_set.discard(best_move)
#
#         # Dodaj na koniec listy tabu
#         if len(tabu_list) >= tabu_size:
#             old_move = tabu_list.popleft()
#             tabu_set.discard(old_move)
#
#         tabu_list.append(best_move)
#         tabu_set.add(best_move)
#
#         # Aktualizuj najlepsze rozwiązanie
#         if current_cost < best_cost:
#             best_tour = list(current_tour)
#             best_cost = current_cost
#             no_improvement_count = 0
#         else:
#             no_improvement_count += 1
#             if no_improvement_count >= max_no_improvement:
#                 break
#
#     # Upewnij się, że koszt jest poprawnie obliczony
#     final_cost = calculate_tour_cost(best_tour)
#
#     # Zawsze zwróć najlepsze znalezione (nie gorsze niż początkowe)
#     if final_cost > initial_cost:
#         return initial_cost, tour + [tour[0]]
#
#     return final_cost, best_tour + [best_tour[0]]
#
#
# def tsp_tabu_search_with_restart(matrix, initial_path=None, max_iterations=1000,
#                                   tabu_size=None, num_restarts=3):
#     """
#     Rozwiązuje TSP metodą Tabu Search z wieloma restartami.
#
#     Wykonuje kilka przebiegów Tabu Search z różnymi punktami startowymi
#     i zwraca najlepsze znalezione rozwiązanie.
#     """
#     n = len(matrix)
#     if n == 0:
#         return 0, []
#     if n == 1:
#         return 0, [0, 0]
#     if n == 2:
#         return matrix[0][1] + matrix[1][0], [0, 1, 0]
#
#     best_overall_cost = float('inf')
#     best_overall_path = None
#
#     iterations_per_restart = max_iterations // num_restarts
#
#     for restart in range(num_restarts):
#         if restart == 0 and initial_path is not None:
#             start_path = initial_path
#         else:
#             # Losowy punkt startowy
#             start_path = list(range(n))
#             random.shuffle(start_path)
#             start_path.append(start_path[0])
#
#         cost, path = tsp_tabu_search(matrix, start_path, iterations_per_restart, tabu_size)
#
#         if cost < best_overall_cost:
#             best_overall_cost = cost
#             best_overall_path = path
#
#     return best_overall_cost, best_overall_path
import random
import copy


# 1. Funkcja generująca macierz (z poprzedniego kroku, dla kompletności)
def generuj_macierz(n, seed):
    random.seed(seed)
    max_waga = 10 * n
    return [[0 if i == j else random.randint(1, max_waga) for j in range(n)] for i in range(n)]


# 2. Funkcja obliczająca koszt ścieżki
def oblicz_koszt(sciezka, macierz):
    koszt = 0
    # Sumujemy odległości między kolejnymi miastami
    for i in range(len(sciezka) - 1):
        u = sciezka[i]
        v = sciezka[i + 1]
        koszt += macierz[u][v]
    return koszt


# 3. Główny algorytm Tabu Search
def tabu_search(sciezka_startowa, macierz, max_iter=1000, kadencja_tabu=15):
    """
    sciezka_startowa: lista np. [0, 21, ..., 0]
    macierz: macierz odległości NxN
    max_iter: liczba iteracji algorytmu
    kadencja_tabu: jak długo ruch pozostaje na liście zabronionej
    """

    # Kopiujemy, żeby nie psuć oryginału i usuwamy ostatnie '0' dla łatwiejszych obliczeń
    # Operujemy na liście [0, 21, 36, ..., 23] (bez powtórzonego startu na końcu)
    obecna_trasa = sciezka_startowa[:-1]
    n = len(obecna_trasa)

    najlepsza_trasa = list(obecna_trasa)

    # Dodajemy 0 na koniec tylko do obliczenia kosztu
    obecny_koszt = oblicz_koszt(obecna_trasa + [obecna_trasa[0]], macierz)
    najlepszy_koszt = obecny_koszt

    # Lista Tabu - przechowuje ruchy (pary indeksów), które są zabronione
    lista_tabu = []  # format: [(index1, index2), ...]



    for it in range(max_iter):
        kandydat_trasa = []
        kandydat_koszt = float('inf')
        wykonany_ruch = None

        # Generowanie sąsiedztwa (SWAP)
        # Pętla od 1, bo nie ruszamy miasta startowego (index 0)
        for i in range(1, n):
            for j in range(i + 1, n):

                # Tworzymy sąsiada przez zamianę
                sasiad = list(obecna_trasa)
                sasiad[i], sasiad[j] = sasiad[j], sasiad[i]

                koszt_sasiada = oblicz_koszt(sasiad + [sasiad[0]], macierz)
                ruch = (i, j)

                # Sprawdzamy czy ruch jest dozwolony
                jest_w_tabu = False
                # Sprawdzamy czy para (i,j) lub (j,i) jest w tabu
                if ruch in lista_tabu or (j, i) in lista_tabu:
                    jest_w_tabu = True

                # Warunki wyboru kandydata:
                # 1. Nie jest w tabu I jest lepszy od obecnego najlepszego kandydata w tej iteracji
                # LUB
                # 2. Jest w tabu, ALE spełnia kryterium aspiracji (jest lepszy niż globalne optimum)

                if (not jest_w_tabu and koszt_sasiada < kandydat_koszt) or \
                        (jest_w_tabu and koszt_sasiada < najlepszy_koszt):
                    kandydat_trasa = sasiad
                    kandydat_koszt = koszt_sasiada
                    wykonany_ruch = ruch

        # Jeśli nie znaleziono żadnego ruchu (teoretycznie niemożliwe przy swap), przerywamy
        if wykonany_ruch is None:
            print("Brak dostępnych ruchów, przerywam...")
            break

        # Aktualizacja obecnego rozwiązania
        obecna_trasa = kandydat_trasa

        # Aktualizacja najlepszego globalnie rozwiązania
        if kandydat_koszt < najlepszy_koszt:
            najlepszy_koszt = kandydat_koszt
            najlepsza_trasa = list(kandydat_trasa)


        # Aktualizacja listy Tabu
        lista_tabu.append(wykonany_ruch)
        if len(lista_tabu) > kadencja_tabu:
            lista_tabu.pop(0)  # Usuwamy najstarszy element

    # Zwracamy trasę w formacie wejściowym (zamknięty cykl z zerem na końcu)
    return najlepsza_trasa + [najlepsza_trasa[0]], najlepszy_koszt
