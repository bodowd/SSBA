package main

import (
	"fmt"
	"time"
)

const ITERS = 20000

type f func()

func v1() {
	x := [ITERS][ITERS]int{}
	var i, j int
	for i = 0; i < ITERS; i++ {
		for j = 0; j < ITERS; j++ {
			x[j][i] = i + j
		}
	}
}

func v2() {
	x := [ITERS][ITERS]int{}
	var i, j int
	for j = 0; j < ITERS; j++ {
		for i = 0; i < ITERS; i++ {
			x[j][i] = i + j
		}
	}
}

func printSpeed(fn f, version string) {
	start := time.Now()
	fn()
	end := time.Now()
	elapsed := end.Sub(start).Seconds()
	fmt.Printf("%s time: %.3f\n", version, elapsed)
}

func main() {
	printSpeed(v1, "v1")
	printSpeed(v2, "v2")
}
