"""Два мешка в палатке: перебор всех раскладок и проверка симуляцией."""

import random
from fractions import Fraction

N = 100  # номерных и пустых шаров поровну


def bag_success(numbered: int, blank: int) -> Fraction:
    """Вероятность вытащить номерной шар из мешка; из пустого мешка — проигрыш."""
    total = numbered + blank
    return Fraction(numbered, total) if total else Fraction(0)


def win_probability(a: int, b: int) -> Fraction:
    """В первом мешке a номерных и b пустых, во втором — остальные."""
    return (bag_success(a, b) + bag_success(N - a, N - b)) / 2


def simulate(a: int, b: int, trials: int, rng: random.Random) -> float:
    bags = [[1] * a + [0] * b, [1] * (N - a) + [0] * (N - b)]
    wins = 0
    for _ in range(trials):
        bag = bags[rng.randrange(2)]
        if bag:
            wins += bag[rng.randrange(len(bag))]
    return wins / trials


def main() -> None:
    # при равной вероятности первым идёт мешок с меньшим числом шаров
    results = sorted(
        ((win_probability(a, b), a, b) for a in range(N + 1) for b in range(N + 1)),
        key=lambda r: (-r[0], r[1] + r[2]),
    )

    print("Лучшие раскладки (номерных, пустых в первом мешке):")
    for p, a, b in results[:3]:
        print(f"  a={a:3d}, b={b:3d}:  P = {p} = {float(p):.4f}")

    best_p, best_a, best_b = results[0]
    print(f"\nОптимум: a={best_a}, b={best_b}, P = {best_p} ~ {float(best_p):.4f}")

    trap = win_probability(0, 0)
    print(f"\nЛовушка 'переложить все 100 номерных': первый мешок пуст, P = {trap} = {float(trap):.2f}")
    print("  если из пустого мешка разрешено перейти в другой: P = 100/200 = 0.50")

    rng = random.Random(42)
    trials = 1_000_000
    sim = simulate(best_a, best_b, trials, rng)
    print(f"\nСимуляция оптимума, {trials:,} игр: {sim:.4f} (теория {float(best_p):.4f})")


if __name__ == "__main__":
    main()
