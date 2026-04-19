# Raport projektowy

## Cel projektu

Celem projektu było przebadanie niezawodności układu typu **Feed-Forward Arbiter PUF**
(FF Arbiter PUF) w zależności od jego typowych parametrów konstrukcyjnych. W ramach
analizy uwzględniono również parametr `noisiness`, który modeluje niestabilność odpowiedzi
PUF wynikającą z zakłóceń pomiarowych lub zmian warunków pracy.

Badanie zostało wykonane symulacyjnie z użyciem biblioteki `pypuf`. Dla każdej konfiguracji
PUF wielokrotnie ewaluowano ten sam zestaw wyzwań, a następnie porównywano otrzymane
odpowiedzi.

## Badany typ PUF

W projekcie analizowany jest **Feed-Forward Arbiter PUF**, czyli wariant Arbiter PUF, w którym
część sygnałów pośrednich jest zawracana do dalszych etapów jako dodatkowa informacja
sterująca. Taka konstrukcja zwiększa złożoność zależności pomiędzy wyzwaniem a odpowiedzią,
ponieważ odpowiedź nie zależy wyłącznie od liniowej akumulacji opóźnień w kolejnych stadiach.

W symulacji wykorzystywana jest klasa:

```python
FeedForwardArbiterPUF(n=n, ff=ff, seed=seed, noisiness=noisiness)
```

gdzie:

- `n` oznacza liczbę stadiów, czyli długość łańcucha opóźnień,
- `ff` określa położenie sprzężeń feed-forward,
- `seed` zapewnia powtarzalność eksperymentów,
- `noisiness` określa poziom zaszumienia odpowiedzi.

## Analizowana metryka

Analizowaną metryką jest **Reliability**, czyli miara powtarzalności odpowiedzi PUF dla tych
samych wyzwań. Dla stabilnego, idealnego układu ta sama próbka powinna przy każdej ewaluacji
zwracać tę samą odpowiedź.

W implementacji dla jednej konfiguracji generowanych jest `1000` wyzwań, a następnie PUF jest
ewaluowany `10` razy dla tego samego zbioru wyzwań. Dla każdej pary ewaluacji obliczana jest
średnia odległość Hamminga odpowiedzi:

```text
intra_hd = mean(response_i != response_j)
```

Niezawodność jest następnie liczona jako:

```text
Reliability = 1 - mean(intra_hd)
```

Wartość `1.0` oznacza pełną powtarzalność odpowiedzi, natomiast niższe wartości oznaczają
większą niestabilność.

## Metodyka eksperymentów

Przeprowadzono trzy serie eksperymentów:

1. Wpływ parametru `noisiness` na niezawodność.
2. Wpływ długości łańcucha opóźnień `n` na niezawodność.
3. Wpływ liczby sprzężeń feed-forward na niezawodność.

Stałe parametry symulacji:

- liczba wyzwań: `1000`,
- liczba ewaluacji dla tego samego zbioru wyzwań: `10`,
- ziarno losowości dla badania `noisiness`: `42`.

W porównaniu z pierwotną wersją zwiększono liczbę testów dla badania długości łańcucha oraz
badania liczby sprzężeń. Dla tych dwóch serii każda konfiguracja była badana dla pięciu
niezależnych seedów: `42`, `43`, `44`, `45`, `46`. W tabelach podano średnią wartość
`Reliability` oraz odchylenie standardowe między tymi pięcioma instancjami PUF.

## Wyniki: wpływ parametru noisiness

Dla pierwszej serii eksperymentów przyjęto:

- `n = 64`,
- `ff = [(16, 32), (32, 48)]`,
- `noisiness` zmieniane w zakresie od `0.0` do `0.5`.

| Noisiness | Reliability |
| ---: | ---: |
| 0.0000 | 1.000000 |
| 0.0556 | 0.962467 |
| 0.1111 | 0.927378 |
| 0.1667 | 0.896333 |
| 0.2222 | 0.867311 |
| 0.2778 | 0.841933 |
| 0.3333 | 0.817111 |
| 0.3889 | 0.792978 |
| 0.4444 | 0.771111 |
| 0.5000 | 0.756489 |

Wyniki pokazują jednoznaczny spadek niezawodności wraz ze wzrostem parametru `noisiness`.
Dla braku szumu (`0.0`) odpowiedzi są w pełni powtarzalne. Przy maksymalnym badanym poziomie
szumu (`0.5`) niezawodność spada do około `0.7565`, co oznacza znacznie większy udział
niezgodności pomiędzy kolejnymi ewaluacjami tych samych wyzwań.

## Wyniki: wpływ długości łańcucha opóźnień

Dla drugiej serii eksperymentów przyjęto:

- `noisiness = 0.1`,
- pięć seedów dla każdej konfiguracji: `42`, `43`, `44`, `45`, `46`,
- dwa sprzężenia feed-forward rozmieszczone proporcjonalnie do długości łańcucha:
  `[(n/4, n/2), (n/2, 3n/4)]`.

| Liczba stadiów `n` | Konfiguracja `ff` | Średnia Reliability | Odchylenie std. |
| ---: | --- | ---: | ---: |
| 16 | `[(4, 8), (8, 12)]` | 0.938778 | 0.020313 |
| 24 | `[(6, 12), (12, 18)]` | 0.922271 | 0.024166 |
| 32 | `[(8, 16), (16, 24)]` | 0.925484 | 0.017360 |
| 48 | `[(12, 24), (24, 36)]` | 0.920693 | 0.006264 |
| 64 | `[(16, 32), (32, 48)]` | 0.926009 | 0.007441 |
| 96 | `[(24, 48), (48, 72)]` | 0.922871 | 0.007204 |
| 128 | `[(32, 64), (64, 96)]` | 0.922640 | 0.006725 |
| 192 | `[(48, 96), (96, 144)]` | 0.918222 | 0.006828 |
| 256 | `[(64, 128), (128, 192)]` | 0.922147 | 0.007830 |
| 384 | `[(96, 192), (192, 288)]` | 0.925271 | 0.004888 |
| 512 | `[(128, 256), (256, 384)]` | 0.921080 | 0.006555 |

![Wpływ długości łańcucha opóźnień na niezawodność](output/reliability_vs_n.png)

Rozszerzona seria testów nie wskazuje na silną monotoniczną zależność między długością
łańcucha a niezawodnością. Najwyższą średnią wartość uzyskano dla `n = 16` (`0.938778`), ale
dla tej konfiguracji wystąpiło też relatywnie duże odchylenie standardowe. Dla większości
pozostałych długości wyniki skupiają się w wąskim zakresie około `0.918-0.926`.

Można więc uznać, że przy `noisiness = 0.1` długość łańcucha wpływa na wynik słabiej niż sam
poziom szumu. Dodatkowe punkty pomiarowe pokazują, że pojedyncze porównanie kilku wartości
`n` może łatwo sugerować trend, który po uśrednieniu po większej liczbie instancji okazuje się
raczej lokalną fluktuacją.

## Wyniki: wpływ liczby sprzężeń feed-forward

Dla trzeciej serii eksperymentów przyjęto:

- `n = 64`,
- `noisiness = 0.1`,
- pięć seedów dla każdej konfiguracji: `42`, `43`, `44`, `45`, `46`,
- liczba sprzężeń feed-forward zmieniana od `0` do `8`.

| Liczba sprzężeń FF | Konfiguracja `ff` | Średnia Reliability | Odchylenie std. |
| ---: | --- | ---: | ---: |
| 0 | `[]` | 0.957324 | 0.002438 |
| 1 | `[(5, 21)]` | 0.942044 | 0.012953 |
| 2 | `[(5, 15), (52, 62)]` | 0.921538 | 0.003522 |
| 3 | `[(5, 13), (29, 37), (54, 62)]` | 0.918093 | 0.006711 |
| 4 | `[(5, 11), (22, 28), (39, 45), (56, 62)]` | 0.929222 | 0.015286 |
| 5 | `[(5, 10), (18, 23), (31, 36), (44, 49), (57, 62)]` | 0.921742 | 0.010725 |
| 6 | `[(5, 9), (15, 19), (26, 30), (36, 40), (47, 51), (58, 62)]` | 0.927276 | 0.011573 |
| 7 | `[(5, 9), (13, 17), (22, 26), (31, 35), (40, 44), (49, 53), (58, 62)]` | 0.921813 | 0.009824 |
| 8 | `[(5, 9), (12, 16), (20, 24), (27, 31), (35, 39), (42, 46), (50, 54), (58, 62)]` | 0.921516 | 0.011300 |

![Wpływ liczby sprzężeń feed-forward na niezawodność](output/reliability_vs_ff.png)

Najwyższą niezawodność osiąga układ bez sprzężeń feed-forward (`0.957324`). Dodanie jednego
sprzężenia obniża średnią do `0.942044`, a dalsze zwiększanie liczby sprzężeń utrzymuje wyniki
głównie w zakresie około `0.918-0.929`. Po rozszerzeniu testów zależność nie jest idealnie
monotoniczna: konfiguracje z `4` i `6` sprzężeniami wypadają lepiej niż sąsiednie warianty.

Wynik nadal pokazuje jednak wyraźną różnicę między klasycznym układem bez sprzężeń a wariantami
ze sprzężeniami. Sprzężenia feed-forward zwiększają złożoność struktury, ale przy obecności
szumu mogą pogarszać powtarzalność odpowiedzi.

## Wykres zbiorczy i dane

Wygenerowany wykres zbiorczy znajduje się poniżej:

![Wykres niezawodności FF Arbiter PUF](output/puf_reliability_report.png)

Program zapisuje również dane liczbowe do plików:

- `output/noise_results.csv`,
- `output/n_results.csv`,
- `output/ff_results.csv`.

## Wnioski

Najsilniejszy wpływ na badaną metrykę ma parametr `noisiness`. Wzrost poziomu szumu prowadzi
do wyraźnego i monotonicznego spadku niezawodności, co jest zgodne z intuicją: im większa
niestabilność symulowanego układu, tym większa szansa, że ta sama próbka zwróci inną odpowiedź
przy kolejnej ewaluacji.

Długość łańcucha opóźnień `n` wpływa na wynik słabiej. Po zwiększeniu liczby punktów pomiarowych
i uśrednieniu po pięciu instancjach PUF wartości `Reliability` pozostają dla większości
konfiguracji blisko siebie. Nie zaobserwowano jednoznacznej zależności monotonicznej.

Liczba sprzężeń feed-forward ma zauważalny wpływ przede wszystkim przy przejściu od układu bez
sprzężeń do układów ze sprzężeniami. Dalsze zwiększanie liczby sprzężeń nie powoduje już
prostego, liniowego spadku niezawodności, ale wszystkie badane warianty ze sprzężeniami były
mniej niezawodne niż wariant bez sprzężeń.

Podsumowując, badany FF Arbiter PUF zachowuje wysoką niezawodność dla niskich poziomów szumu,
jednak jego stabilność maleje wraz ze wzrostem `noisiness` oraz po dodaniu sprzężeń
feed-forward. Rozszerzenie liczby testów pokazało, że dla parametrów konstrukcyjnych takich jak
`n` i liczba sprzężeń warto analizować wiele konfiguracji i kilka instancji losowych, ponieważ
pojedyncze wyniki mogą być podatne na fluktuacje wynikające z konkretnego rozkładu opóźnień.

## Możliwe rozszerzenia

Projekt można rozszerzyć o:

- większą liczbę losowych instancji PUF dla każdej konfiguracji,
- analizę dodatkowych metryk, takich jak uniqueness lub uniformity,
- badanie wpływu różnych położeń sprzężeń feed-forward przy tej samej liczbie sprzężeń,
- porównanie wyników dla kilku wartości `noisiness` w badaniach `n` oraz `ff`.
