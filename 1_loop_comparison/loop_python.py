import time


def big_loop_print():
    amount = 10**4 * 5
    start = time.time()

    for i in range(amount):
        print(i)

    now = time.time()
    total = now - start

    print(f"Total loop time = {total}")


def big_loop_sum():
    amount = 10**8 * 5
    start = time.time()
    total_sum = 0

    for i in range(amount):
        total_sum += i

    now = time.time()
    total = now - start

    print(f"Total Sum = {total_sum} Total loop time = {total}")


if __name__ == "__main__":
    # big_loop_print()
    big_loop_sum()
