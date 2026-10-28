"""Красные мячи: нормальное приближение против точного биномиального распределения."""

import math
import random
from statistics import NormalDist

N, P = 100, 0.15
LEVEL = 0.95


def binom_cdf_table(n: int, p: float) -> list[float]:
    cdf, acc = [], 0.0
    for k in range(n + 1):
        acc += math.comb(n, k) * p**k * (1 - p) ** (n - k)
        cdf.append(acc)
    return cdf


def quantile(cdf: list[float], q: float) -> int:
    """Наименьшее k, для которого P(X <= k) >= q."""
    return next(k for k, c in enumerate(cdf) if c >= q)


def main() -> None:
    alpha = (1 - LEVEL) / 2
    mu, sigma = N * P, math.sqrt(N * P * (1 - P))
    z = NormalDist().inv_cdf(1 - alpha)
    lo, hi = mu - z * sigma, mu + z * sigma
    print(f"Нормальное приближение: {mu:.0f} +- {z:.3f}*{sigma:.4f} = [{lo:.4f}; {hi:.4f}]")
    print(f"  левая граница вниз: {math.floor(lo)}")

    cdf = binom_cdf_table(N, P)
    q_lo, q_hi = quantile(cdf, alpha), quantile(cdf, 1 - alpha)
    coverage = cdf[q_hi] - cdf[q_lo - 1]
    print(f"\nТочные квантили Bin({N}, {P}): [{q_lo}; {q_hi}], покрытие {coverage:.4f}")

    rng = random.Random(42)
    samples = sorted(sum(rng.random() < P for _ in range(N)) for _ in range(200_000))
    emp_lo = samples[int(alpha * len(samples))]
    emp_hi = samples[int((1 - alpha) * len(samples))]
    print(f"Симуляция, 200 000 серий по {N}: эмпирические квантили [{emp_lo}; {emp_hi}]")


if __name__ == "__main__":
    main()
