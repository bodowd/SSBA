import time

ITERS = 4000


x = [[i for i in range(ITERS)] for j in range(ITERS)]


def v1():
    for i in range(ITERS):
        for j in range(ITERS):
            x[j][i] = i + j


def v2():
    for j in range(ITERS):
        for i in range(ITERS):
            x[j][i] = i + j


def print_time(f, version):
    start = time.time()
    f()
    end = time.time()
    print("{} Time: {:.1f}".format(version, end - start))


def main():
    print_time(v1, "v1")
    print_time(v2, "v2")


main()
