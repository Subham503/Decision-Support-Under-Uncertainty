import numpy as np

from problem_setup import (
    CAPACITIES,
    DEMANDS,
    cost_matrix,
    CONFIG
)

ALPHA = CONFIG["decision_model"]["laplace_smoothing_alpha"]


def estimate_probabilities(observations):
    counts = np.array([
        np.sum(observations == demand)
        for demand in DEMANDS
    ])

    return (counts + ALPHA) / (
        len(observations) + ALPHA * len(DEMANDS)
    )


def expected_cost_strategy(observations, lam):
    probabilities = estimate_probabilities(observations)
    matrix = cost_matrix(lam)
    expected_costs = matrix @ probabilities

    return int(CAPACITIES[np.argmin(expected_costs)])


def most_likely_strategy(observations, lam):
    counts = np.array([
        np.sum(observations == demand)
        for demand in DEMANDS
    ])

    most_likely_demand = DEMANDS[np.argmax(counts)]
    demand_index = np.where(DEMANDS == most_likely_demand)[0][0]

    matrix = cost_matrix(lam)

    return int(CAPACITIES[np.argmin(matrix[:, demand_index])])


def minimax_strategy(lam):
    matrix = cost_matrix(lam)
    worst_case_costs = np.max(matrix, axis=1)

    return int(CAPACITIES[np.argmin(worst_case_costs)])


def equal_likelihood_strategy(lam):
    probabilities = np.ones(len(DEMANDS)) / len(DEMANDS)
    matrix = cost_matrix(lam)
    expected_costs = matrix @ probabilities

    return int(CAPACITIES[np.argmin(expected_costs)])


def oracle_strategy(true_probabilities, lam):
    matrix = cost_matrix(lam)
    expected_costs = matrix @ true_probabilities

    return int(CAPACITIES[np.argmin(expected_costs)])


if __name__ == "__main__":
    observations = np.array([
        20, 20, 50, 20, 80, 50, 20, 20, 50, 20
    ])

    lam = 3

    print("Test observations:", observations)
    print("Laplace alpha:", ALPHA)
    print("Estimated probabilities:", estimate_probabilities(observations))

    print("\nDecision recommendations:")
    print("Expected Cost:", expected_cost_strategy(observations, lam))
    print("Most Likely State:", most_likely_strategy(observations, lam))
    print("Minimax:", minimax_strategy(lam))
    print("Equal Likelihood:", equal_likelihood_strategy(lam))

    true_probabilities = np.array([0.70, 0.25, 0.05])
    print("Oracle:", oracle_strategy(true_probabilities, lam))
