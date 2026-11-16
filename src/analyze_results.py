from pathlib import Path
import numpy as np
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent.parent
FILE = BASE_DIR / "results" / "experiment_results_reproduced.csv"

df = pd.read_csv(FILE)

print("DATA VALIDATION")
print("-" * 45)

print("Rows:", len(df))
print("Missing values:", df.isnull().sum().sum())
print("Duplicate rows:", df.duplicated().sum())
print("Negative regret values:", (df["mean_regret"] < -1e-9).sum())

assert len(df) == 256
assert df.isnull().sum().sum() == 0
assert df.duplicated().sum() == 0
assert (df["mean_regret"] >= -1e-9).all()

print("\nAll validation checks passed!")

print("\nOVERALL STRATEGY COMPARISON")
print("-" * 65)

summary = df.groupby("strategy").agg(
    average_cost=("mean_expected_cost", "mean"),
    average_regret=("mean_regret", "mean"),
    average_oracle_agreement=("oracle_agreement", "mean")
).sort_values("average_cost")

print(summary.round(4).to_string())

print("\nSAMPLE SIZE ANALYSIS")
print("-" * 65)

sample_summary = df.groupby(
    ["sample_size", "strategy"]
).agg(
    average_cost=("mean_expected_cost", "mean"),
    average_regret=("mean_regret", "mean"),
    oracle_agreement=("oracle_agreement", "mean")
).reset_index()

print(sample_summary.round(4).to_string(index=False))

print("\nENVIRONMENT-WISE COMPARISON")
print("-" * 65)

environment_summary = df.groupby(
    ["environment", "strategy"]
).agg(
    average_cost=("mean_expected_cost", "mean"),
    average_regret=("mean_regret", "mean")
).reset_index()

print(environment_summary.round(4).to_string(index=False))

print("\nSHORTAGE PENALTY ANALYSIS")
print("-" * 65)

penalty_summary = df.groupby(
    ["shortage_penalty", "strategy"]
).agg(
    average_cost=("mean_expected_cost", "mean"),
    average_regret=("mean_regret", "mean")
).reset_index()

print(penalty_summary.round(4).to_string(index=False))
