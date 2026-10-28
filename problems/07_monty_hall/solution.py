"""Монти Холл при разных протоколах ведущего: теория в точных дробях и симуляция.

Игрок всегда выбирает дверь 0 (по симметрии это не ограничивает общности).
Ведущий возвращает номер открытой двери или None, если смену не предлагает.
"""

import random
import sys
from fractions import Fraction
from pathlib import Path

DOORS = (0, 1, 2)
PICK = 0
IMG = Path(__file__).parent / "img"


def goat_doors(car: int) -> list[int]:
    return [d for d in DOORS if d not in (PICK, car)]


def classic(car, rng):
    return rng.choice(goat_doors(car))


def ignorant(car, rng):
    """Открывает наугад; если за дверью автомобиль, смены не будет."""
    door = rng.choice([1, 2])
    return None if door == car else door


def evil(car, rng):
    return goat_doors(car)[0] if car == PICK else None


def angel(car, rng):
    return goat_doors(car)[0] if car != PICK else None


def offers(a, b):
    """Предлагает смену с вероятностью a, если игрок угадал, и b, если нет."""
    def host(car, rng):
        return classic(car, rng) if rng.random() < (a if car == PICK else b) else None
    return host


def favourite(q):
    """Всегда предлагает смену; при выборе из двух коз открывает дверь 2 с вероятностью q."""
    def host(car, rng):
        if car == PICK:
            return 2 if rng.random() < q else 1
        return goat_doors(car)[0]
    return host


def mixture(pi):
    """С вероятностью pi ведущий классический, иначе — вредный."""
    def host(car, rng):
        return classic(car, rng) if rng.random() < pi else evil(car, rng)
    return host


def final_door(opened: int | None, switch_prob: float, rng) -> int:
    """Без предложения смены игрок остаётся при своей двери."""
    if opened is not None and rng.random() < switch_prob:
        return next(d for d in DOORS if d not in (PICK, opened))
    return PICK


def simulate(host, switch_prob, games, rng, condition=lambda opened: opened is not None):
    """Доля выигрышей среди игр, где выполнено condition(открытая дверь)."""
    hits = wins = 0
    for _ in range(games):
        car = rng.randrange(3)
        opened = host(car, rng)
        if condition(opened):
            hits += 1
            wins += final_door(opened, switch_prob, rng) == car
    return wins / hits


def switch_wins(a, b) -> Fraction:
    """P(смена выигрывает | смену предложили) = 2b / (2b + a)."""
    a, b = Fraction(a), Fraction(b)
    return 2 * b / (2 * b + a)


def total_win(p, a, b) -> Fraction:
    """Полная вероятность выигрыша: W(p) = (1 + p(2b - a)) / 3."""
    return (1 + Fraction(p) * (2 * Fraction(b) - Fraction(a))) / 3


def main() -> None:
    rng = random.Random(42)
    games = 300_000
    half = Fraction(1, 2)

    rows = [
        ("классический", classic, Fraction(2, 3), None),
        ("не знает, где авто", ignorant, half, None),
        ("вредный", evil, switch_wins(1, 0), None),
        ("добрый", angel, switch_wins(0, 1), None),
        ("a=1, b=1/2", offers(1, 0.5), switch_wins(1, half), None),
        ("любимая дверь, q=1", favourite(1), half, lambda o: o == 2),
        ("любимая дверь, q=0", favourite(0), Fraction(1), lambda o: o == 2),
        ("смесь, pi=0.8", mixture(0.8), switch_wins(1, Fraction(4, 5)), None),
    ]
    print("P(выигрыш | смену предложили)")
    print(f"{'ведущий':22s} {'менять: теория':>15s} {'менять':>8s} {'оставаться':>11s} {'монетка':>8s}")
    for name, host, theory, cond in rows:
        cond = cond or (lambda opened: opened is not None)
        sim = [simulate(host, p, games, rng, cond) for p in (1, 0, 0.5)]
        print(f"{name:22s} {str(theory):>8s} = {float(theory):.3f} {sim[0]:8.3f} {sim[1]:11.3f} {sim[2]:8.3f}")

    print("\nНеизвестные правила: полная вероятность выигрыша W(p) = (1 + p(2b - a)) / 3")
    corners = [(a, b) for a in (0, 1) for b in (0, 1)]
    for label, p in (("оставаться", 0), ("монетка", half), ("менять", 1)):
        worst = min(total_win(p, a, b) for a, b in corners)
        sim = simulate(evil, float(p), games, rng, condition=lambda opened: True) if p else None
        line = f"  {label:10s} гарантирует {str(worst):>4s}"
        if sim is not None:
            line += f"   (симуляция против вредного: {sim:.3f})"
        print(line)
    print("  против вредного ведущего 'оставаться' выигрывает ровно 1/3 — когда игрок угадал сразу")

    if "--plots" in sys.argv:
        draw_plots()


def draw_plots() -> None:
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.colors import LinearSegmentedColormap

    ink, muted, grid, surface = "#0b0b0b", "#52514e", "#e1e0d9", "#fcfcfb"
    plt.rcParams.update({
        "figure.facecolor": surface, "axes.facecolor": surface, "axes.edgecolor": "#c3c2b7",
        "axes.labelcolor": muted, "xtick.color": muted, "ytick.color": muted, "text.color": ink,
    })
    IMG.mkdir(exist_ok=True)

    # карта протоколов: P(смена выигрывает | предложили) по (a, b)
    blues = LinearSegmentedColormap.from_list(
        "blues", ["#cde2fb", "#86b6ef", "#3987e5", "#256abf", "#104281", "#0d366b"])
    n = 201
    grid_vals = [[float(switch_wins(i / (n - 1), j / (n - 1))) if i or j else 0.5
                  for i in range(n)] for j in range(n)]
    fig, ax = plt.subplots(figsize=(6.6, 5.4))
    im = ax.imshow(grid_vals, origin="lower", extent=(0, 1, 0, 1), cmap=blues, vmin=0, vmax=1)
    xs = [i / (n - 1) for i in range(n)]
    ax.plot(xs, [x / 2 for x in xs], color=ink, linewidth=2)
    ax.text(0.62, 0.21, "2b = a: менять = оставаться", fontsize=9, ha="center", va="center",
            rotation=26.6, rotation_mode="anchor", color=ink,
            bbox={"boxstyle": "round,pad=0.25", "fc": surface, "ec": "none", "alpha": 0.9})
    points = [((1, 1), "классический\n2/3"), ((1, 0), "вредный\n0"),
              ((0, 1), "добрый\n1"), ((1, 0.5), "a=1, b=1/2\n1/2")]
    for (a, b), label in points:
        ax.plot(a, b, "o", markersize=9, color="#eb6834", markeredgecolor=surface,
                markeredgewidth=2, clip_on=False, zorder=3)
        ha = "right" if a == 1 else "left"
        ax.annotate(label, (a, b), xytext=(-12 if a == 1 else 12, -14 if b == 1 else 8),
                    textcoords="offset points", ha=ha, fontsize=9,
                    bbox={"boxstyle": "round,pad=0.25", "fc": surface, "ec": "none", "alpha": 0.9})
    ax.set_xlabel("a — P(предложить смену | игрок угадал)")
    ax.set_ylabel("b — P(предложить смену | игрок не угадал)")
    ax.set_title("P(смена выигрывает | смену предложили) = 2b / (2b + a)", fontsize=11, pad=14)
    cbar = fig.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
    cbar.outline.set_visible(False)
    fig.tight_layout()
    fig.savefig(IMG / "protocol_map.png", dpi=120)
    plt.close(fig)

    # смесь честного и вредного ведущего
    pis = [i / 200 for i in range(201)]
    series = [
        ("менять", "#eb6834", "-", lambda pi: 2 * pi / (2 * pi + 1)),
        ("оставаться", "#2a78d6", "-", lambda pi: 1 / (2 * pi + 1)),
        ("монетка", "#1baf7a", "--", lambda pi: 0.5),
    ]
    fig, ax = plt.subplots(figsize=(7, 4.6))
    for label, color, style, f in series:
        ax.plot(pis, [f(pi) for pi in pis], style, color=color, linewidth=2, label=label)
        ax.text(1.02, f(1), label, color=ink, fontsize=9, va="center")
    ax.axvline(0.5, color=muted, linestyle=":", linewidth=1)
    ax.text(0.51, 0.04, "π = 1/2: менять\nстановится выгодно", fontsize=9, color=muted)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.set_xlabel("π — вероятность, что ведущий честный (иначе — вредный)")
    ax.set_ylabel("P(выигрыш | смену предложили)")
    ax.set_title("Чем больше доверия ведущему, тем выгоднее менять", fontsize=11)
    ax.grid(color=grid, linewidth=0.8)
    ax.spines[["top", "right"]].set_visible(False)
    ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.17), ncol=3, frameon=False)
    fig.tight_layout()
    fig.savefig(IMG / "mixture.png", dpi=120)
    plt.close(fig)
    print(f"\nКартинки сохранены в {IMG}")


if __name__ == "__main__":
    main()
