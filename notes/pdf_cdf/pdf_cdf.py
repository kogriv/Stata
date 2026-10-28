"""PDF, CDF и квантили нормального распределения: таблица, проверки и картинки."""

import sys
from pathlib import Path
from statistics import NormalDist

STD = NormalDist(0, 1)
IMG = Path(__file__).parent / "img"


def print_table() -> None:
    print("    x      pdf      cdf")
    for i in range(9):
        x = -3 + 0.75 * i
        print(f"{x:6.2f}   {STD.pdf(x):.4f}   {STD.cdf(x):.4f}")


def print_checks() -> None:
    dx = 0.01
    exact = STD.cdf(dx) - STD.cdf(0)
    print(f"\nP(0 < X <= {dx}) = {exact:.6f};  f(0)*dx = {STD.pdf(0) * dx:.6f}")
    for k in (1, 2, 3):
        print(f"P(|X| <= {k}) = {STD.cdf(k) - STD.cdf(-k):.4f}")
    print(f"inv_cdf(0.975) = {STD.inv_cdf(0.975):.4f}")
    print(f"N(0, 0.1): f(0) = {NormalDist(0, 0.1).pdf(0):.4f}  (плотность больше 1)")


def draw_plots() -> None:
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    IMG.mkdir(exist_ok=True)
    xs = [-4 + 8 * i / 400 for i in range(401)]

    fig, (ax_pdf, ax_cdf) = plt.subplots(1, 2, figsize=(10, 3.8))
    ax_pdf.plot(xs, [STD.pdf(x) for x in xs], color="#2563eb")
    band = [x for x in xs if -1 <= x <= 1]
    ax_pdf.fill_between(band, [STD.pdf(x) for x in band], color="#2563eb", alpha=0.2)
    ax_pdf.text(0, 0.12, "площадь\n= P(-1 < X ≤ 1)\n≈ 0.683", ha="center", fontsize=9)
    ax_pdf.set_title("Плотность f(x)")
    ax_cdf.plot(xs, [STD.cdf(x) for x in xs], color="#dc2626")
    for x in (-1, 1):
        ax_cdf.plot([x, x], [0, STD.cdf(x)], ":", color="gray")
        ax_cdf.plot([-4, x], [STD.cdf(x), STD.cdf(x)], ":", color="gray")
    ax_cdf.annotate("", xy=(-3.6, STD.cdf(1)), xytext=(-3.6, STD.cdf(-1)),
                    arrowprops={"arrowstyle": "<->", "color": "#2563eb"})
    ax_cdf.text(-3.45, 0.5, "F(1) - F(-1)", fontsize=9, color="#2563eb")
    ax_cdf.set_title("Функция распределения F(x) = P(X ≤ x)")
    for ax in (ax_pdf, ax_cdf):
        ax.grid(alpha=0.3)
        ax.set_xlabel("x")
    fig.tight_layout()
    fig.savefig(IMG / "pdf_cdf.png", dpi=120)
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(7, 3.8))
    xs = [-3 + 6 * i / 600 for i in range(601)]
    for sigma, color in ((1, "#2563eb"), (0.3, "#16a34a"), (0.1, "#dc2626")):
        dist = NormalDist(0, sigma)
        ax.plot(xs, [dist.pdf(x) for x in xs], color=color, label=f"σ = {sigma}")
    ax.axhline(1, color="gray", linestyle="--", linewidth=1)
    ax.text(1.8, 1.08, "f = 1", color="gray", fontsize=9)
    ax.set_title("Плотность может быть больше 1, а площадь под ней всегда 1")
    ax.set_xlabel("x")
    ax.grid(alpha=0.3)
    ax.legend()
    fig.tight_layout()
    fig.savefig(IMG / "density_above_one.png", dpi=120)
    plt.close(fig)
    print(f"\nКартинки сохранены в {IMG}")


def main() -> None:
    print_table()
    print_checks()
    if "--plots" in sys.argv:
        draw_plots()


if __name__ == "__main__":
    main()
