from loop_cpython import big_loop_print, big_loop_sum
import time


def loop_print():
    amount = 10**4 * 5
    start = time.time()
    big_loop_print(amount)
    now = time.time()
    total = now - start

    print(f"Total loop time = {total}")


def loop_sum():
    amount = 10**8 * 5
    start = time.time()
    total_sum = big_loop_sum(amount)
    now = time.time()
    total = now - start

    print(f"Total Sum = {total_sum} Total loop time = {total}")


if __name__ == "__main__":
    # loop_print()
    loop_sum()
