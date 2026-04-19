# BSC 26L Lab 1

- Andrzej Pultyn
- 325213
- [andrzej.pultyn.stud@pw.edu.pl]
- bsc26

## Zadanie

- typ PUF - FF Arbiter PUF
- analizowana metryka - Reliability

Raport projektowy znajduje się w pliku [RAPORT.md](RAPORT.md).

## Uruchamianie

Projekt można uruchomić przez `uv`:

```bash
uv run python main.py
```

Program wykonuje pełny zestaw eksperymentów opisanych w raporcie i zapisuje wykres zbiorczy do pliku:

```text
output/puf_reliability_report.png
```

Dodatkowo generowane są osobne wykresy i pliki CSV z wynikami:

```text
output/reliability_vs_n.png
output/reliability_vs_ff.png
output/noise_results.csv
output/n_results.csv
output/ff_results.csv
```
