"""Кубик с перебросами: обратная индукция в точных дробях и симуляция стратегии."""

import random
from fractions import Fraction

STAKE = 475
FACES = [100 * d for d in range(1, 7)]


def values(max_rerolls: int) -> list[Fraction]:
    """V[n] — ожидаемый выигрыш при оптимальной игре с n перебросами в запасе."""
    v = [Fraction(sum(FACES), 6)]
    for _ in range(max_rerolls):
        v.append(sum(max(Fraction(f), v[-1]) for f in FACES) / 6)
    return v


def play(rerolls: int, v: list[Fraction], rng: random.Random) -> int:
    for left in range(rerolls, -1, -1):
        x = rng.choice(FACES)
        if left == 0 or x >= v[left - 1]:
            return x
    raise AssertionError("unreachable")


def main() -> None:
    v = values(5)
    for n, vn in enumerate(v):
        keep = [f // 100 for f in FACES if n == 0 or f >= v[n - 1]]
        mark = "  > ставки" if vn > STAKE else ""
        print(f"N={n}: оставляем {keep}, V = {vn} ~ {float(vn):.2f}{mark}")

    answer = next(n for n, vn in enumerate(v) if vn > STAKE)
    print(f"\nМинимальное N: {answer}")

    rng = random.Random(42)
    games = 1_000_000
    for n in (answer - 1, answer):
        mean = sum(play(n, v, rng) for _ in range(games)) / games
        print(f"Симуляция N={n}, {games:,} игр: средний выигрыш {mean:.2f} (теория {float(v[n]):.2f})")


if __name__ == "__main__":
    main()
