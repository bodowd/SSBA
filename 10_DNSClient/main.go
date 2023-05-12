package main

import (
	"fmt"
	"log"
	"os"
	"syscall"
)

func main() {
	if len(os.Args) != 3 {
		log.Fatal("Usage: go run dns.go [domain] [type] (e.g `google.com A`)")
	}

	query := NewQuery(os.Args[1], os.Args[2])

	googlePublicDNS := syscall.SockaddrInet4{
		Port: 53,
		Addr: [4]byte{8, 8, 8, 8},
	}

	// check man 2 syscall for documentation on Socket
	// nothing really there in golang website. Guessing that they implemented
	// so that it's the same as the C implementation

	// AF_INET: IPv4 Internet protocols
	// SOCK_DGRAM: supports datagrams (connectionless, unreliable messages of
	// a fixed max length)
	// Protocol: Normally only a single protocol exists to support a particular
	// socket type within a given protocol family, in which case protocol can be
	// specified as 0.
	// Since many protocols could be used in networking, we need to tell Socket
	// what to expect.
	// Since our socket is handling only one protocol, I think 0 here means that
	// it should expect only one protocol type. Therefore we use 0 according to
	// the man page
	fd, e := syscall.Socket(syscall.AF_INET, syscall.SOCK_DGRAM, 0)
	check(e)

	defer syscall.Close(fd)

	// bind to any available port
	// From man bind:
	// When a socket is created with socket(2), it exists in a name space
	// (address family) but has no address assigned to it.
	// bind() assigns the address specified
	//
	// OS needs to be instructed to route any appropriate messages to this process
	// bind does this
	// expects a SockaddrInet4 pointer
	e = syscall.Bind(fd, &syscall.SockaddrInet4{Port: 0, Addr: [4]byte{0, 0, 0, 0}})
	check(e)

	e = syscall.Sendto(fd, Serialize(query), 0, &googlePublicDNS)
	check(e)

	// Receive/print response
	out := make([]byte, 4096)
	for {
		_, from, e := syscall.Recvfrom(fd, out, 0)
		check(e)

		fromip4, ok := from.(*syscall.SockaddrInet4)
		if !ok {
			continue
		}

		// ignore responses from other hosts
		if fromip4.Addr != googlePublicDNS.Addr || fromip4.Port != googlePublicDNS.Port {
			continue
		}

		response := Deserialize(out)

		// ignore responses to other queries
		if !QueryResponseMatch(query, response) {
			continue
		}

		fmt.Println(";; Got answer:")
		fmt.Print(response)
		break
	}

}

func check(e error) {
	if e != nil {
		panic(e)
	}
}
