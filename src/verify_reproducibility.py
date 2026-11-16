from pathlib import Path
import pandas as pd
import numpy as np

BASE = Path(__file__).resolve().parent.parent
RESULTS = BASE / "results"

original = pd.read_csv(RESULTS / "experiment_results_original.csv")
reproduced = pd.read_csv(RESULTS / "experiment_results_reproduced.csv")

print("Original rows:", len(original))
print("Reproduced rows:", len(reproduced))

same_shape = original.shape == reproduced.shape
same_columns = list(original.columns) == list(reproduced.columns)

if same_shape and same_columns:
    identical = True

    for column in original.columns:
        if pd.api.types.is_numeric_dtype(original[column]):
            if not np.allclose(
                original[column],
                reproduced[column],
                rtol=1e-12,
                atol=1e-12
            ):
                identical = False
                print("Difference found in:", column)
        else:
            if not original[column].equals(reproduced[column]):
                identical = False
                print("Difference found in:", column)

    print("\nResults identical:", identical)

else:
    identical = False
    print("\nShape or column mismatch!")

if identical:
    print("REPRODUCIBILITY TEST PASSED!")
else:
    print("REPRODUCIBILITY TEST FAILED!")
