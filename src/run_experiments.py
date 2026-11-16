import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))

from problem_setup import (
    CAPACITIES,
    DEMANDS,
    CONFIG,
    cost_matrix
)

from decision_engine import (
    expected_cost_strategy,
    most_likely_strategy,
    minimax_strategy,
    equal_likelihood_strategy
)


# Load all experiment parameters from JSON
EXPERIMENT = CONFIG["experiment"]

ENVIRONMENTS = CONFIG["demand_environments"]
PENALTIES = CONFIG["decision_model"]["shortage_penalties"]
SAMPLE_SIZES = EXPERIMENT["sample_sizes"]

REPETITIONS = EXPERIMENT["repetitions"]
MASTER_SEED = EXPERIMENT["master_seed"]


def evaluate_action(action, matrix, probabilities):
    index = np.where(CAPACITIES == action)[0][0]
    return float(matrix[index] @ probabilities)


def run_simulation():

    records = []

    total = (
        len(ENVIRONMENTS)
        * len(PENALTIES)
        * len(SAMPLE_SIZES)
        * REPETITIONS
    )

    completed = 0

    for env_index, (environment, probabilities) in enumerate(
        ENVIRONMENTS.items()
    ):

        true_probabilities = np.array(probabilities, dtype=float)

        if not np.isclose(true_probabilities.sum(), 1.0):
            raise ValueError(
                f"Probabilities for {environment} must sum to 1."
            )

        for penalty_index, lam in enumerate(PENALTIES):

            matrix = cost_matrix(lam)

            true_expected_costs = matrix @ true_probabilities
            oracle_minimum = float(np.min(true_expected_costs))

            oracle_actions = CAPACITIES[
                np.isclose(true_expected_costs, oracle_minimum)
            ]

            for sample_index, sample_size in enumerate(SAMPLE_SIZES):

                seed = (
                    MASTER_SEED
                    + env_index * 100000
                    + penalty_index * 10000
                    + sample_index * 1000
                )

                rng = np.random.default_rng(seed)

                strategy_costs = {
                    "Expected Cost": [],
                    "Most Likely State": [],
                    "Minimax": [],
                    "Equal Likelihood": []
                }

                strategy_regrets = {
                    name: [] for name in strategy_costs
                }

                oracle_agreements = {
                    name: [] for name in strategy_costs
                }

                for _ in range(REPETITIONS):

                    observations = rng.choice(
                        DEMANDS,
                        size=sample_size,
                        p=true_probabilities
                    )

                    actions = {
                        "Expected Cost": expected_cost_strategy(
                            observations, lam
                        ),
                        "Most Likely State": most_likely_strategy(
                            observations, lam
                        ),
                        "Minimax": minimax_strategy(lam),
                        "Equal Likelihood": equal_likelihood_strategy(lam)
                    }

                    for name, action in actions.items():

                        true_cost = evaluate_action(
                            action, matrix, true_probabilities
                        )

                        regret = true_cost - oracle_minimum

                        strategy_costs[name].append(true_cost)
                        strategy_regrets[name].append(regret)

                        oracle_agreements[name].append(
                            int(action in oracle_actions)
                        )

                    completed += 1

                for name in strategy_costs:

                    costs = np.array(strategy_costs[name])
                    regrets = np.array(strategy_regrets[name])
                    agreements = np.array(oracle_agreements[name])

                    mean_cost = float(np.mean(costs))
                    std_cost = float(np.std(costs, ddof=1))

                    ci = 1.96 * std_cost / np.sqrt(REPETITIONS)

                    records.append({
                        "environment": environment,
                        "shortage_penalty": lam,
                        "sample_size": sample_size,
                        "strategy": name,
                        "mean_expected_cost": mean_cost,
                        "std_expected_cost": std_cost,
                        "ci_lower": mean_cost - ci,
                        "ci_upper": mean_cost + ci,
                        "mean_regret": float(np.mean(regrets)),
                        "oracle_agreement": float(np.mean(agreements)),
                        "oracle_minimum_cost": oracle_minimum
                    })

                if completed % 1200 == 0:
                    print(f"Progress: {completed}/{total}")

    results = pd.DataFrame(records)

    output_path = (
        Path(__file__).resolve().parent.parent
        / "results"
        / "experiment_results_reproduced.csv"
    )

    results.to_csv(output_path, index=False)

    print("\nSimulation completed!")
    print("Master seed:", MASTER_SEED)
    print("Repetitions:", REPETITIONS)
    print("Total simulation repetitions:", total)
    print("Result configurations:", len(results))
    print("Saved to:", output_path)


if __name__ == "__main__":
    run_simulation()
