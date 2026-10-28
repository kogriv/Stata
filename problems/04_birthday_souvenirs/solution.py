"""40 туристов и 400 сувениров: точный ответ, приближения и симуляция."""

import math
import random

K, N = 40, 400


def exact_collision(k: int, n: int) -> float:
    return 1 - math.prod((n - i) / n for i in range(k))


def simulate(k: int, n: int, trials: int, rng: random.Random) -> float:
    hits = sum(len({rng.randrange(n) for _ in range(k)}) < k for _ in range(trials))
    return hits / trials


def main() -> None:
    rows = [
        ("точное произведение", exact_collision(K, N)),
        ("1 - exp(-k(k-1)/2n)", 1 - math.exp(-K * (K - 1) / (2 * N))),
        ("1 - exp(-k^2/2n)", 1 - math.exp(-K * K / (2 * N))),
    ]
    for name, p in rows:
        print(f"{name:22s} {100 * p:8.4f}%  -> {math.floor(100 * p)}")

    rng = random.Random(42)
    trials = 500_000
    print(f"\nСимуляция, {trials:,} групп: {100 * simulate(K, N, trials, rng):.2f}%")


if __name__ == "__main__":
    main()
