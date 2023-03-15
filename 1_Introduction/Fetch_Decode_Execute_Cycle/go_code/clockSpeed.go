package main

import (
	"fmt"
	"time"
)

const ITERS = 1000000000

type f func()

func sumLoop() {
	sum := 0
	for i := 0; i < ITERS; i++ {
		sum += i
	}
}

func multLoop() {
	sum := 1
	for i := 1; i < ITERS; i++ {
		sum *= i
	}
}

func divLoop() {
	sum := 1
	for i := 1; i < ITERS; i++ {
		sum /= i
	}
	// fmt.Printf("%d", sum)
}

func printSpeed(fn f) {
	start := time.Now()
	fn()
	end := time.Now()
	elapsed := end.Sub(start)
	ops := float64(ITERS) / elapsed.Seconds()
	fmt.Printf("Clock speed approx %.3f GHz\n", ops/float64(ITERS))

}

func main() {
	fmt.Printf("SUM\n")
	printSpeed(sumLoop)
	fmt.Printf("MULT\n")
	printSpeed(multLoop)
	fmt.Printf("DIV\n")
	printSpeed(divLoop)
}
