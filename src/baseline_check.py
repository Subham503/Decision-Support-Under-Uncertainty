import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from problem_setup import cost_matrix, CAPACITIES

for lam in [1.2, 2, 3, 5]:
    matrix = cost_matrix(lam)

    worst_case = matrix.max(axis=1)
    equal_likelihood = matrix.mean(axis=1)

    print(f"\nShortage penalty: {lam}")
    print("Capacities:", CAPACITIES)
    print("Worst-case costs:", worst_case)
    print("Equal-likelihood costs:", equal_likelihood)
    print("Minimax choice:", CAPACITIES[worst_case.argmin()])
    print("Equal-likelihood choice:", CAPACITIES[equal_likelihood.argmin()])
