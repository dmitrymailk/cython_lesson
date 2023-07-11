import pandas as pd
import numpy as np
import time
from cython_pandas import integrate_f_plain, integrate_f_typed


def simple_integration():
    amount = 10**4 * 2
    df = pd.DataFrame(
        {
            "a": -1 * np.abs(np.random.randn(amount)),
            "b": np.abs(np.random.randn(amount)),
            "N": np.random.randint(100, amount, (amount)),
            "x": np.float64,
        }
    )
    print(df.head(5))
    start = time.time()
    df["x"] = df.apply(lambda x: integrate_f_plain(x["a"], x["b"], x["N"]), axis=1)
    total_time = time.time() - start
    print(df.head(5))

    print(f"Total integration time = {total_time}")


def simple_integration_typed():
    amount = 10**4 * 2
    df = pd.DataFrame(
        {
            "a": -1 * np.abs(np.random.randn(amount)),
            "b": np.abs(np.random.randn(amount)),
            "N": np.random.randint(100, amount, (amount)),
            "x": np.float64,
        }
    )
    print(df.head(5))
    start = time.time()
    df["x"] = df.apply(lambda x: integrate_f_typed(x["a"], x["b"], x["N"]), axis=1)
    total_time = time.time() - start
    print(df.head(5))

    print(f"Total integration time = {total_time}")


if __name__ == "__main__":
    simple_integration_typed()
