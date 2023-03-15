import time

GIGA = 1000000000
ITERS = 1000000


def main():
    print("SUM")
    measure_loop(sum_loop)
    print("MULT")
    measure_loop(mult_loop)
    print("DIV")
    measure_loop(div_loop)


def sum_loop():
    sum = 0
    for i in range(ITERS):
        sum += i


def mult_loop():
    sum = 1
    for i in range(1, ITERS):
        sum *= i


def div_loop():
    sum = 1
    for i in range(1, ITERS):
        sum /= i


def measure_loop(func):
    start = time.process_time()
    func()
    end = time.process_time()
    ops = ITERS / (end - start)
    print("Clock speed approx {:.3f} GHz".format(ops / GIGA))

    s = time.time()
    func()
    e = time.time()
    ops = ITERS / (e - s)
    print("time.time speed {:.3f} GHz".format(ops / GIGA))


main()
