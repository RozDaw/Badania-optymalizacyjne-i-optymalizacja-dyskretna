"""
Funkcje pomocnicze do generowania i wczytywania danych TSP.
"""
import math


def tsp_rand(size, seed):
    """
    Generuje macierz kosztów dla problemu TSP.
    Wykorzystuje pseudolosowy generator z podanym seedem.
    """
    print(f"data: {size}")
    matrix = []
    for a in range(size):
        row = []
        for b in range(size):
            seed = (seed * 69069 + 1) & 0xFFFFFFFF
            d = (seed % 99 + 1) * (a != b)
            print('{:2d}'.format(d), end=" ")
            row.append(d)
        print()
        matrix.append(row)
    print()
    return matrix, seed


def generate_tsp_data(size, seed):
    """
    Generuje macierz kosztów dla problemu TSP.
    Zwraca macierz kosztów bez drukowania.
    """
    matrix = []
    for a in range(size):
        row = []
        for b in range(size):
            seed = (seed * 69069 + 1) & 0xFFFFFFFF
            d = (seed % (size*10) + 1) * (a != b)
            row.append(d)
        matrix.append(row)
    return matrix, seed


import random


def generuj_macierz(n, seed):
    # Ustawiamy ziarno losowości
    random.seed(seed)

    max_waga = 10 * n

    # Generujemy macierz: 0 na przekątnej, losowa liczba w pozostałych polach
    macierz = [
        [0 if i == j else random.randint(1, max_waga) for j in range(n)]
        for i in range(n)
    ]

    return macierz



def load_cost_matrix(filename):
    """
    Wczytuje macierz kosztów z pliku tekstowego.
    Format pliku:
    data: N
    d11 d12 ... d1N
    d21 d22 ... d2N
    ...
    dN1 dN2 ... dNN
    """
    with open(filename, 'r') as f:
        lines = f.read().strip().splitlines()

    # Pierwsza linia: "data: N"
    first_line = lines[0].strip()
    if first_line.startswith("data:"):
        n = int(first_line.split(":")[1].strip())
    else:
        n = int(first_line)

    matrix = []
    for i in range(1, n + 1):
        row = list(map(int, lines[i].split()))
        matrix.append(row)

    return matrix


def load_cost_matrix_raw(text):
    """
    Wczytuje macierz kosztów z tekstu.
    Format:
    data: N
    d11 d12 ... d1N
    ...
    """
    lines = text.strip().splitlines()

    first_line = lines[0].strip()
    if first_line.startswith("data:"):
        n = int(first_line.split(":")[1].strip())
    else:
        n = int(first_line)

    matrix = []
    for i in range(1, n + 1):
        row = list(map(int, lines[i].split()))
        matrix.append(row)

    return matrix


def save_cost_matrix(filename, matrix):
    """
    Zapisuje macierz kosztów do pliku.
    """
    n = len(matrix)
    with open(filename, 'w') as f:
        f.write(f"data: {n}\n")
        for row in matrix:
            f.write(' '.join('{:2d}'.format(d) for d in row) + '\n')


def load_coordinates_raw(text):
    """
    Wczytuje współrzędne miast z tekstu i tworzy macierz kosztów.
    Format:
    data:
    N
    x1 y1   x2 y2   x3 y3   ...
    
    Zwraca macierz kosztów opartą na odległościach euklidesowych.
    """
    lines = text.strip().splitlines()
    
    # Znajdź liczbę miast
    idx = 0
    if lines[idx].strip().startswith("data"):
        idx += 1
    n = int(lines[idx].strip())
    idx += 1
    
    # Wczytaj współrzędne - wszystkie mogą być w jednej linii lub wielu
    coords_text = ' '.join(lines[idx:])
    values = list(map(int, coords_text.split()))
    
    # Parsuj pary współrzędnych (x, y)
    coords = []
    for i in range(0, n * 2, 2):
        x = values[i]
        y = values[i + 1]
        coords.append((x, y))
    
    # Twórz macierz kosztów opartą na odległościach euklidesowych
    matrix = []
    for i in range(n):
        row = []
        for j in range(n):
            if i == j:
                row.append(0)
            else:
                dist = math.hypot(coords[i][0] - coords[j][0],
                                  coords[i][1] - coords[j][1])
                row.append(int(round(dist)))
        matrix.append(row)
    
    return matrix, coords


def print_matrix(matrix):
    """Wyświetla macierz kosztów."""
    for row in matrix:
        print(' '.join('{:2d}'.format(d) for d in row))


def verify_solution(matrix, path, expected_cost):
    """Weryfikuje poprawność rozwiązania."""
    if not path:
        return expected_cost == 0

    cost = 0
    for i in range(len(path) - 1):
        cost += matrix[path[i]][path[i + 1]]

    return cost == expected_cost

