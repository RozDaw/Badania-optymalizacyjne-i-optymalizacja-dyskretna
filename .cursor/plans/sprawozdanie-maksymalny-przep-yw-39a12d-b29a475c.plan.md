<!-- b29a475c-8a17-4347-8f0b-b834f0c2eecf efe1bffc-bcf1-42f1-98f6-bbf789bd1a67 -->
# Plan stworzenia sprawozdania o algorytmach maksymalnego przepływu

## Struktura dokumentu

### 1. Strona tytułowa

- Użycie tej samej strony tytułowej co w poprzednich sprawozdaniach
- Zmiana tytułu na "Algorytmy maksymalnego przepływu"
- Te same dane studentów: Konrad Pempera (263948), Dawid Różański (263524)
- Ten sam prowadzący: Dr inż. Mariusz Makuchowski
- Pliki logo: `pwr_logo.png`, `wit_logo.png` (już istnieją w projekcie)

### 2. Wstęp (sekcja 1)

- Opis problemu maksymalnego przepływu w grafie skierowanym
- Wspomnienie o trzech implementowanych algorytmach:
  - Edmonds-Karp (BFS)
  - Dinic
  - Ford-Fulkerson (DFS)
- Opis eksperymentów: pomiary czasów wykonania dla grafów o różnych rozmiarach
- Wspomnienie o reprezentacji grafu jako macierzy sąsiedztwa

### 3. Opis implementacji algorytmów (sekcja 2)

- **2.1 Algorytm Edmondsa-Karpa**
  - Opis działania: iteracyjne znajdowanie ścieżek powiększających za pomocą BFS
  - Złożoność: O(VE²)
  - Krótki opis implementacji z kodu

- **2.2 Algorytm Dinica**
  - Opis działania: budowa grafu poziomów + wielokrotne wysyłanie przepływu
  - Złożoność: O(V²E)
  - Wyjaśnienie różnicy względem Edmonds-Karp

- **2.3 Algorytm Forda-Fulkersona (DFS)**
  - Opis działania: iteracyjne znajdowanie ścieżek powiększających za pomocą DFS
  - Złożoność: O(E·max_flow) - może być wolny
  - Wspomnienie o możliwych problemach z wydajnością

- **2.4 Reprezentacja grafu i generowanie instancji**
  - Macierz sąsiedztwa z przepustowościami
  - Funkcja `generate_random_graph()` z parametrami: n, max_capacity=20, density=0.3
  - Opis formatu danych

### 4. Pomiary czasów (sekcja 3)

- **3.1 Analiza wyników pomiarów czasu wykonania**
  - Opis wykresu porównującego wszystkie trzy algorytmy
  - Wspomnienie o rozmiarach grafów: 20, 40, 60, 80, 100, 120, 140, 160, 180, 200 wierzchołków
  - Analiza trendów czasowych dla każdego algorytmu

- **3.2 Wnioski**
  - Porównanie wydajności algorytmów
  - Który algorytm jest najszybszy dla różnych rozmiarów grafów
  - Praktyczne zastosowania każdego algorytmu

- **3.3 Porównanie złożoności obliczeniowej**
  - Teoretyczna analiza złożoności: O(VE²) vs O(V²E) vs O(E·max_flow)
  - Wyjaśnienie różnic w praktycznej wydajności
  - Dla grafu o n wierzchołkach i gęstości 0.3: E ≈ 0.3·n²

- **Wykres** (osobny plik .tex)
  - Plik `max_flow_chart.tex` z wykresem TikZ/PGFPlots
  - Trzy serie danych: Edmonds-Karp, Dinic, Ford-Fulkerson
  - Oś X: liczba wierzchołków n
  - Oś Y: czas wykonania [s]

### 5. Podsumowanie (sekcja 4)

- Podsumowanie wyników badań
- Porównanie algorytmów pod kątem wydajności
- Wnioski praktyczne: kiedy użyć którego algorytmu
- Zgodność wyników z teoretyczną złożonością

## Pliki do utworzenia

1. **`max_flow/main.tex`** - główny plik sprawozdania
2. **`max_flow/max_flow_chart.tex`** - plik z wykresem TikZ

## Instrukcje dotyczące danych do wykresu

**Jak uzyskać dane do wykresu:**

1. Uruchomić kod `max_flow/main.py` (już zawiera pętlę pomiarową)
2. Po wykonaniu kodu, dane są w listach: `times_ek`, `times_dinic`, `times_ff`
3. Wartości `sizes` to: [20, 40, 60, 80, 100, 120, 140, 160, 180, 200]
4. Należy wydrukować lub zapisać wartości z list czasów i użyć ich w pliku `max_flow_chart.tex` w formacie:
   ```
   \addplot + [mark = *, thick] coordinates
       {
       (20, czas1)(40, czas2)(60, czas3)...
       };
   ```


**Alternatywnie:** Można zmodyfikować kod, aby automatycznie zapisywał dane do pliku .tex, ale na razie założymy ręczne wprowadzenie danych.

## Długość dokumentu

- Cel: 5-10 stron
- Struktura podobna do poprzednich sprawozdań
- Zwięzłe, ale kompletne opisy algorytmów
- Szczegółowa analiza wyników pomiarów

### To-dos

- [ ] Utworzyć plik główny algorytm maksymalnego przepływu.tex ze stroną tytułową, spisem treści i sekcją Wstęp
- [ ] Napisać sekcję Opis implementacji algorytmów z podsekcjami dla Edmonds-Karp, Dinic i Ford-Fulkerson
- [ ] Zmodyfikować max_flow/main.py aby eksportował dane pomiarowe w formacie TikZ coordinates lub do pliku tekstowego
- [ ] Utworzyć plik max_flow_chart.tex z wykresem TikZ/PGFPlots zawierającym dane z pomiarów
- [ ] Napisać sekcję Pomiary czasów z analizą wyników, wnioskami i włączeniem wykresu
- [ ] Napisać sekcję Podsumowanie z porównaniem algorytmów i wnioskami końcowymi