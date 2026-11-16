import json
from pathlib import Path

import numpy as np

BASE_DIR = Path(__file__).resolve().parent.parent
CONFIG_PATH = BASE_DIR / "data" / "simulation_config.json"

with open(CONFIG_PATH, "r", encoding="utf-8-sig") as file:
    CONFIG = json.load(file)

MODEL_CONFIG = CONFIG["decision_model"]

CAPACITIES = np.array(MODEL_CONFIG["capacities"])
DEMANDS = np.array(MODEL_CONFIG["demand_states"])
OVERAGE = MODEL_CONFIG["overcapacity_penalty"]


def cost(q, d, lam):
    shortage = max(d - q, 0)
    excess = max(q - d, 0)

    return lam * shortage + OVERAGE * excess


def cost_matrix(lam):
    return np.array([
        [cost(q, d, lam) for d in DEMANDS]
        for q in CAPACITIES
    ], dtype=float)


if __name__ == "__main__":
    M = cost_matrix(3)

    print("Loaded model parameters from simulation_config.json")
    print("Capacities:", CAPACITIES)
    print("Demand states:", DEMANDS)
    print("Overcapacity penalty:", OVERAGE)
    print("\nCost matrix:")
    print(M)
