import csv
from pathlib import Path

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


def summarize_reliability(n, ff, noisiness, seeds, N_challenges=1000, N_evals=10):
    results = [
        calculate_reliability(
            n=n,
            ff=ff,
            noisiness=noisiness,
            seed=seed,
            N_challenges=N_challenges,
            N_evals=N_evals,
        )
        for seed in seeds
    ]
    return float(np.mean(results)), float(np.std(results, ddof=1)), results


def proportional_ff(n):
    return [(n // 4, n // 2), (n // 2, 3 * n // 4)]


def evenly_spaced_ff(n, count):
    if count == 0:
        return []

    span = max(4, n // (2 * count + 2))
    starts = np.linspace(max(2, n // 12), n - span - 2, count, dtype=int)
    return [(int(start), int(start + span)) for start in starts]


def save_csv(path, header, rows):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(header)
        writer.writerows(rows)


def run_experiments():
    print("Rozpoczęcie badań FF Arbiter PUF...\n")
    output_dir = Path("output")
    output_dir.mkdir(parents=True, exist_ok=True)

    N_CHALLENGES = 1000
    N_EVALS = 10
    BASE_SEED = 42
    EXTENDED_SEEDS = [42, 43, 44, 45, 46]

    print("1. Badanie wpływu parametru noisiness...")
    noise_levels = np.linspace(0.0, 0.5, 10)
    rel_noise = [
        calculate_reliability(
            n=64,
            ff=[(16, 32), (32, 48)],
            noisiness=nz,
            seed=BASE_SEED,
            N_challenges=N_CHALLENGES,
            N_evals=N_EVALS,
        )
        for nz in noise_levels
    ]

    print("2. Badanie wpływu długości łańcucha opóźnień (n)...")
    n_values = [16, 24, 32, 48, 64, 96, 128, 192, 256, 384, 512]
    ff_configs = [proportional_ff(n) for n in n_values]
    n_summaries = [
        summarize_reliability(
            n=n,
            ff=ff,
            noisiness=0.1,
            seeds=EXTENDED_SEEDS,
            N_challenges=N_CHALLENGES,
            N_evals=N_EVALS,
        )
        for n, ff in zip(n_values, ff_configs)
    ]
    rel_n = [summary[0] for summary in n_summaries]
    rel_n_std = [summary[1] for summary in n_summaries]

    print("3. Badanie wpływu sprzężeń w przód (liczby pętli)...")
    ff_counts = list(range(0, 9))
    ff_variations = [evenly_spaced_ff(64, count) for count in ff_counts]
    ff_summaries = [
        summarize_reliability(
            n=64,
            ff=ff,
            noisiness=0.1,
            seeds=EXTENDED_SEEDS,
            N_challenges=N_CHALLENGES,
            N_evals=N_EVALS,
        )
        for ff in ff_variations
    ]
    rel_ff = [summary[0] for summary in ff_summaries]
    rel_ff_std = [summary[1] for summary in ff_summaries]

    fig, axs = plt.subplots(1, 3, figsize=(15, 5))

    axs[0].plot(noise_levels, rel_noise, marker="o", color="blue")
    axs[0].set_title("Niezawodność vs Noisiness")
    axs[0].set_xlabel("Poziom szumu (noisiness)")
    axs[0].set_ylabel("Reliability")
    axs[0].grid(True)

    axs[1].errorbar(n_values, rel_n, yerr=rel_n_std, marker="s", color="green", capsize=4)
    axs[1].set_title("Niezawodność vs Liczba stadiów (n)")
    axs[1].set_xlabel("n (długość łańcucha)")
    axs[1].set_ylabel("Reliability")
    axs[1].grid(True)

    x_labels = [str(count) for count in ff_counts]
    axs[2].bar(x_labels, rel_ff, yerr=rel_ff_std, color="orange", capsize=4)
    axs[2].set_title("Niezawodność vs Liczba pętli FF")
    axs[2].set_xlabel("Liczba sprzężeń w przód")
    axs[2].set_ylabel("Reliability")
    axs[2].set_ylim(min(rel_ff) - 0.05, 1.0)
    axs[2].grid(axis="y")

    output_path = output_dir / "puf_reliability_report.png"

    plt.tight_layout()
    plt.savefig(output_path)

    plt.figure(figsize=(7, 5))
    plt.errorbar(n_values, rel_n, yerr=rel_n_std, marker="s", color="green", capsize=4)
    plt.title("Niezawodność vs Liczba stadiów (n)")
    plt.xlabel("n (długość łańcucha)")
    plt.ylabel("Reliability")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(output_dir / "reliability_vs_n.png")

    plt.figure(figsize=(7, 5))
    plt.bar(x_labels, rel_ff, yerr=rel_ff_std, color="orange", capsize=4)
    plt.title("Niezawodność vs Liczba pętli FF")
    plt.xlabel("Liczba sprzężeń w przód")
    plt.ylabel("Reliability")
    plt.ylim(min(rel_ff) - 0.05, 1.0)
    plt.grid(axis="y")
    plt.tight_layout()
    plt.savefig(output_dir / "reliability_vs_ff.png")

    save_csv(
        output_dir / "noise_results.csv",
        ["noisiness", "reliability"],
        [(f"{noise:.4f}", f"{reliability:.6f}") for noise, reliability in zip(noise_levels, rel_noise)],
    )
    save_csv(
        output_dir / "n_results.csv",
        ["n", "ff", "mean_reliability", "std_reliability", "seeds"],
        [
            (
                n,
                repr(ff),
                f"{mean:.6f}",
                f"{std:.6f}",
                repr(EXTENDED_SEEDS),
            )
            for n, ff, (mean, std, _) in zip(n_values, ff_configs, n_summaries)
        ],
    )
    save_csv(
        output_dir / "ff_results.csv",
        ["ff_count", "ff", "mean_reliability", "std_reliability", "seeds"],
        [
            (
                count,
                repr(ff),
                f"{mean:.6f}",
                f"{std:.6f}",
                repr(EXTENDED_SEEDS),
            )
            for count, ff, (mean, std, _) in zip(ff_counts, ff_variations, ff_summaries)
        ],
    )
    print(
        "Analiza zakończona. Wygenerowano wykresy do pliku "
        "'output/puf_reliability_report.png' oraz osobne wykresy dla badań n i ff."
    )
