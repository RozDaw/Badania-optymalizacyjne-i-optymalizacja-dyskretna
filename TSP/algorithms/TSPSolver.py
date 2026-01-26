
import random
import math
import copy


# 1. Funkcja generująca macierz (bez zmian)
def generuj_macierz(n, seed):
    random.seed(seed)
    max_waga = 10 * n
    return [[0 if i == j else random.randint(1, max_waga) for j in range(n)] for i in range(n)]


# 2. Funkcja obliczająca koszt ścieżki (bez zmian)
def oblicz_koszt(sciezka, macierz):
    koszt = 0
    for i in range(len(sciezka) - 1):
        u = sciezka[i]
        v = sciezka[i + 1]
        koszt += macierz[u][v]
    return koszt


# 3. Zmodyfikowany algorytm Symulowanego Wyżarzania
def simulated_annealing(sciezka_startowa, macierz, temp_pocz=10, temp_konc=0.01, alpha=0.995, iteracje_na_temp=100):
    """
    iteracje_na_temp: ile prób wykonujemy dla jednej temperatury przed ochłodzeniem
    """

    # Przygotowanie trasy (usuwamy ostatnie 0)
    obecna_trasa = sciezka_startowa[:-1]
    n = len(obecna_trasa)
    no_improvement = 0
    max_no_improvement = 100

    # Koszt początkowy
    obecny_koszt = oblicz_koszt(obecna_trasa + [obecna_trasa[0]], macierz)

    # Inicjalizacja najlepszego rozwiązania
    najlepsza_trasa = list(obecna_trasa)
    najlepszy_koszt = obecny_koszt

    T = temp_pocz
    nr_epoki = 0  # Licznik schłodzeń
    calkowita_liczba_iteracji = 0

    print(f"Koszt początkowy: {obecny_koszt}")

    # Pętla zewnętrzna: chłodzenie
    while T > temp_konc:
        nr_epoki += 1

        # Pętla wewnętrzna: stabilizacja w danej temperaturze (Metropolis)
        for _ in range(iteracje_na_temp):
            calkowita_liczba_iteracji += 1

            # 1. Losujemy dwa indeksy do zamiany (z pominięciem startowego 0)
            i = random.randint(1, n - 1)
            j = random.randint(1, n - 1)
            while i == j:
                j = random.randint(1, n - 1)

            # 2. Tworzymy sąsiada (Swap)
            nowa_trasa = list(obecna_trasa)
            nowa_trasa[i], nowa_trasa[j] = nowa_trasa[j], nowa_trasa[i]

            # 3. Obliczamy koszt (pełna rekalkulacja)
            nowy_koszt = oblicz_koszt(nowa_trasa + [nowa_trasa[0]], macierz)

            # 4. Delta
            delta = nowy_koszt - obecny_koszt




            # 5. Decyzja o akceptacji
            zaakceptowano = False
            if delta < 0:
                zaakceptowano = True
            else:
                prawdopodobienstwo = math.exp(-delta / T)
                if random.random() < prawdopodobienstwo:
                    zaakceptowano = True
                else:
                    no_improvement += 1
            if no_improvement >= max_no_improvement:
                obecna_trasa = najlepsza_trasa
                no_improvement = 0



            if zaakceptowano:
                obecna_trasa = nowa_trasa
                obecny_koszt = nowy_koszt

                # Sprawdzamy rekord globalny
                if obecny_koszt < najlepszy_koszt:
                    najlepszy_koszt = obecny_koszt
                    najlepsza_trasa = list(obecna_trasa)
                    # Wypisujemy info - dodalem nr epoki dla czytelności
                    print(f"Epoka {nr_epoki} (T={T:.2f}): Nowy rekord! Koszt: {najlepszy_koszt}")

        # 6. Chłodzenie po wykonaniu serii iteracji
        T *= alpha

    return najlepsza_trasa + [najlepsza_trasa[0]], najlepszy_koszt