from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_FILE = BASE_DIR / "results" / "experiment_results_reproduced.csv"
FIGURE_DIR = BASE_DIR / "results" / "figures"

FIGURE_DIR.mkdir(parents=True, exist_ok=True)

df = pd.read_csv(DATA_FILE)

strategies = [
    "Expected Cost",
    "Most Likely State",
    "Minimax",
    "Equal Likelihood"
]


def save_figure(filename):
    plt.tight_layout()
    plt.savefig(FIGURE_DIR / filename, dpi=300, bbox_inches="tight")
    plt.close()
    print("Saved:", filename)


# Figure 1: Overall strategy comparison
summary = df.groupby("strategy")["mean_expected_cost"].mean()
summary = summary.reindex(strategies)

plt.figure(figsize=(9, 5))
summary.plot(kind="bar")
plt.title("Overall Strategy Performance")
plt.xlabel("Decision Strategy")
plt.ylabel("Average Expected Cost")
plt.xticks(rotation=15)
save_figure("01_strategy_comparison.png")


# Figure 2: Effect of sample size
sample_summary = df.groupby(
    ["sample_size", "strategy"]
).agg(
    average_cost=("mean_expected_cost", "mean"),
    average_regret=("mean_regret", "mean")
).reset_index()

fig, axes = plt.subplots(1, 2, figsize=(12, 5))

for strategy in strategies:
    subset = sample_summary[
        sample_summary["strategy"] == strategy
    ]

    axes[0].plot(
        subset["sample_size"],
        subset["average_cost"],
        marker="o",
        label=strategy
    )

    axes[1].plot(
        subset["sample_size"],
        subset["average_regret"],
        marker="o",
        label=strategy
    )

axes[0].set_title("Sample Size vs Expected Cost")
axes[0].set_xlabel("Number of Observations")
axes[0].set_ylabel("Average Expected Cost")

axes[1].set_title("Sample Size vs Regret")
axes[1].set_xlabel("Number of Observations")
axes[1].set_ylabel("Average Regret")

axes[0].legend()
axes[1].legend()

fig.tight_layout()
fig.savefig(
    FIGURE_DIR / "02_sample_size_analysis.png",
    dpi=300,
    bbox_inches="tight"
)
plt.close(fig)
print("Saved: 02_sample_size_analysis.png")


# Figure 3: Shortage penalty sensitivity
penalty_summary = df.groupby(
    ["shortage_penalty", "strategy"]
)["mean_expected_cost"].mean().reset_index()

plt.figure(figsize=(9, 5))

for strategy in strategies:
    subset = penalty_summary[
        penalty_summary["strategy"] == strategy
    ]

    plt.plot(
        subset["shortage_penalty"],
        subset["mean_expected_cost"],
        marker="o",
        label=strategy
    )

plt.title("Sensitivity to Shortage Penalty")
plt.xlabel("Shortage Penalty")
plt.ylabel("Average Expected Cost")
plt.legend()
save_figure("03_penalty_sensitivity.png")


# Figure 4: Demand environment comparison
environment_summary = df.groupby(
    ["environment", "strategy"]
)["mean_expected_cost"].mean().unstack()

environment_summary = environment_summary[strategies]

environment_summary.plot(
    kind="bar",
    figsize=(11, 6)
)

plt.title("Strategy Performance Across Demand Environments")
plt.xlabel("Demand Environment")
plt.ylabel("Average Expected Cost")
plt.xticks(rotation=15)
plt.legend(title="Strategy")

save_figure("04_environment_comparison.png")


print("\nAll four figures generated successfully!")
