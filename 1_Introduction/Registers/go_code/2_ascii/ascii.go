package main

import "fmt"

func main() {
	char := 'a'
	ascii := int(char)

	for string(ascii) != "z" {
		fmt.Printf("%s - %d\n", string(ascii), ascii)
		ascii += 1
	}
}
