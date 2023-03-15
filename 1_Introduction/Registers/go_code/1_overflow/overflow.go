package main

import "fmt"

func main() {
	var i uint64 = 1 << 63
	fmt.Printf("1<<63: %d %08b\n", i, i)
	fmt.Printf("1<<64: %d %08b\n", i<<64, i<<64)
}
