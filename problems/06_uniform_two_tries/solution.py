"""Число из [0, 1], две попытки: подбор порога симуляцией и обобщение на n попыток."""

import random
from fractions import Fraction


def expected(t: float) -> float:
    """Ожидаемый выигрыш порога t: E W(t) = (1 - t^2)/2 + t/2."""
    return (1 - t * t) / 2 + t / 2


def simulate(t: float, games: int, rng: random.Random) -> float:
    total = 0.0
    for _ in range(games):
        x = rng.random()
        total += x if x >= t else rng.random()
    return total / games


def main() -> None:
    rng = random.Random(42)
    games = 400_000
    print(" порог   теория   симуляция")
    for t in (0.0, 0.25, 0.4, 0.5, 0.6, 0.75, 1.0):
        print(f"  {t:4.2f}   {expected(t):.4f}   {simulate(t, games, rng):.4f}")

    v = [Fraction(1, 2)]
    for _ in range(4):
        v.append((1 + v[-1] ** 2) / 2)
    print("\nV_n для n попыток:")
    for n, vn in enumerate(v, start=1):
        print(f"  n={n}: {vn} ~ {float(vn):.4f}")


if __name__ == "__main__":
    main()
