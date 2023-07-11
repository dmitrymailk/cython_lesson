import pandas as pd
import numpy as np
import time


def f(x):
    return x * (x - 1)


def integrate_f(a, b, N):
    s = 0
    dx = (b - a) / N
    for i in range(N):
        s += f(a + i * dx)
    result = s * dx
    return result


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
    df["x"] = df.apply(lambda x: integrate_f(x["a"], x["b"], x["N"]), axis=1)
    total_time = time.time() - start
    print(df.head(5))

    print(f"Total integration time = {total_time}")


if __name__ == "__main__":
    simple_integration()
