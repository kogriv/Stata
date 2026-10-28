"""Дождь в Москве: формула Байеса для трёх независимых свидетелей и симуляция."""

import random
from fractions import Fraction

P_RAIN = Fraction(30, 365)
P_TRUTH = Fraction(3, 5)
WITNESSES = 3


def posterior(witnesses: int) -> Fraction:
    """P(дождь | все witnesses сказали 'дождь')."""
    yes_if_rain = P_TRUTH ** witnesses
    yes_if_dry = (1 - P_TRUTH) ** witnesses
    return yes_if_rain * P_RAIN / (yes_if_rain * P_RAIN + yes_if_dry * (1 - P_RAIN))


def simulate(days: int, rng: random.Random) -> tuple[float, int]:
    p_rain, p_truth = float(P_RAIN), float(P_TRUTH)
    all_yes = rain_and_all_yes = 0
    for _ in range(days):
        rain = rng.random() < p_rain
        # правдивый свидетель называет погоду как есть, лжец — наоборот
        if all((rng.random() < p_truth) == rain for _ in range(WITNESSES)):
            all_yes += 1
            rain_and_all_yes += rain
    return rain_and_all_yes / all_yes, all_yes


def main() -> None:
    p3 = posterior(WITNESSES)
    print(f"Три свидетеля: P = {p3} ~ {float(p3):.4f}")
    p1 = posterior(1)
    print(f"Один свидетель (так считать неверно): P = {p1} ~ {float(p1):.4f}")

    rng = random.Random(42)
    sim, n = simulate(2_000_000, rng)
    print(f"\nСимуляция: дней, когда все трое сказали 'да': {n:,}; из них с дождём {sim:.4f}")


if __name__ == "__main__":
    main()
