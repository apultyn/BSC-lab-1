import numpy as np
import matplotlib.pyplot as plt

from pypuf.simulation import FeedForwardArbiterPUF
from pypuf.io import random_inputs


def calculate_reliability(n, ff, noisiness, seed=42, N_challenges=1000, N_evals=10):
    puf = FeedForwardArbiterPUF(n=n, ff=ff, seed=seed, noisiness=noisiness)
    challenges = random_inputs(n=n, N=N_challenges, seed=seed)
    responses = [puf.eval(challenges) for _ in range(N_evals)]

    intra_hds = []
    for i in range(N_evals):
        for j in range(i + 1, N_evals):
            hd = np.mean(responses[i] != responses[j])
            intra_hds.append(hd)

    mean_intra_hd = np.mean(intra_hds)

    reliability = 1.0 - mean_intra_hd
    return reliability


def run_experiments():
    print("Rozpoczęcie badań FF Arbiter PUF...\n")

    print("1. Badanie wpływu parametru noisiness...")
    noise_levels = np.linspace(0.0, 0.5, 10)
    rel_noise = [
        calculate_reliability(n=64, ff=[(16, 32), (32, 48)], noisiness=nz)
        for nz in noise_levels
    ]

    print("2. Badanie wpływu długości łańcucha opóźnień (n)...")
    n_values = [32, 64, 128, 256]
    ff_configs = [[(n // 4, n // 2), (n // 2, 3 * n // 4)] for n in n_values]
    rel_n = [
        calculate_reliability(n=n_values[i], ff=ff_configs[i], noisiness=0.1)
        for i in range(len(n_values))
    ]

    print("3. Badanie wpływu sprzężeń w przód (liczby pętli)...")
    ff_variations = [
        [],
        [(10, 30)],
        [(10, 30), (30, 50)],
        [(10, 20), (20, 30), (30, 40), (40, 50)],
    ]
    rel_ff = [calculate_reliability(n=64, ff=ff, noisiness=0.1) for ff in ff_variations]

    fig, axs = plt.subplots(1, 3, figsize=(15, 5))

    axs[0].plot(noise_levels, rel_noise, marker="o", color="blue")
    axs[0].set_title("Niezawodność vs Noisiness")
    axs[0].set_xlabel("Poziom szumu (noisiness)")
    axs[0].set_ylabel("Reliability")
    axs[0].grid(True)

    axs[1].plot(n_values, rel_n, marker="s", color="green")
    axs[1].set_title("Niezawodność vs Liczba stadiów (n)")
    axs[1].set_xlabel("n (długość łańcucha)")
    axs[1].grid(True)

    x_labels = ["0", "1", "2", "4"]
    axs[2].bar(x_labels, rel_ff, color="orange")
    axs[2].set_title("Niezawodność vs Liczba pętli FF")
    axs[2].set_xlabel("Liczba sprzężeń w przód")
    axs[2].set_ylim(min(rel_ff) - 0.05, 1.0)
    axs[2].grid(axis="y")

    plt.tight_layout()
    plt.savefig("output/puf_reliability_report.png")
    print(
        "Analiza zakończona. Wygenerowano wykresy do pliku 'puf_reliability_report.png'."
    )
