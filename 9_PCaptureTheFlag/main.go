package main

import (
	"encoding/binary"
	"encoding/hex"
	"fmt"
	"os"
)

const (
	// number of bytes of each section in the header
	MAGIC_NUMBER        = 4 // number of bytes that are in the magic number
	MAJOR_VERSION       = 2
	MINOR_VERSION       = 2
	TIME_ZONE_OFFSET    = 4
	TIME_STAMP_ACCURACY = 4
	SNAPSHOT_LENGTH     = 4
	LINK_LAYER_TYPE     = 4
)

// number of bytes of each section in per packet header
const (
	TIME_STAMP_SEC     = 4
	TIME_STAMP_M_NSEC  = 4
	LENGTH_CAPTURED    = 4
	UNTRUNCATED_LENGTH = 4
)

const (
	MAIN_HEADER   = 24
	PACKET_HEADER = 16
)

var LITTLE_ENDIAN_FLAG = false

func bytesToUint64(bytes []byte) uint64 {
	if LITTLE_ENDIAN_FLAG {
		return binary.LittleEndian.Uint64(bytes)
	}
	return binary.BigEndian.Uint64(bytes)

}

func readPacketLength(bytes []byte, cur int) uint64 {
	packetLength := bytesToUint64(bytes[cur : cur+LENGTH_CAPTURED])
	// untruncatedLength := bytesToUint16(bytes[cur+LENGTH_CAPTURED : cur+LENGTH_CAPTURED+UNTRUNCATED_LENGTH])

	// if packetLength != untruncatedLength {
	// 	panic("There was a truncation")
	// }

	return packetLength

}

func main() {
	bytes, err := os.ReadFile("net.cap")
	if err != nil {
		panic("error reading file")
	}

	// first 24 bytes are the main header
	magicNumber := bytes[:MAGIC_NUMBER]
	fmt.Printf("Magic number: 0x%x\n", magicNumber)
	if hex.EncodeToString(magicNumber) == "d4c3b2a1" {
		fmt.Println("My machine is in reverse order of the machine that wrote the file")
		// this machine has a different byte order as the host that wrote the file
		// need to reverse the byte order of everything we parse
		LITTLE_ENDIAN_FLAG = true

	}

	// go to first packet header length of packet
	cur := MAIN_HEADER + TIME_STAMP_SEC + TIME_STAMP_M_NSEC
	packetsCount := 0

	for cur < len(bytes) {
		packetLength := binary.LittleEndian.Uint16(bytes[cur : cur+LENGTH_CAPTURED])
		untruncatedLength := binary.LittleEndian.Uint16(bytes[cur+LENGTH_CAPTURED : cur+LENGTH_CAPTURED+UNTRUNCATED_LENGTH])
		if packetLength != untruncatedLength {
			panic("packet was truncated")
		}

		// advance to the next packet length field of the next packet header
		cur += LENGTH_CAPTURED + UNTRUNCATED_LENGTH + int(packetLength) + TIME_STAMP_SEC + TIME_STAMP_M_NSEC
		packetsCount++
	}

	fmt.Printf("Number of packets: %d\n", packetsCount)

}
