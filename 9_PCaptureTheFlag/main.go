package main

import (
	"encoding/binary"
	"encoding/hex"
	"fmt"
	"os"
	"strconv"
	"strings"
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

func convertIp(ipBytes []byte) string {
	var sb strings.Builder
	for i := range ipBytes {
		sb.WriteString(strconv.Itoa(int(ipBytes[i])))
		sb.WriteString(".")
	}
	return sb.String()
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

	// if the link layer is 01 00 00 00 in little endian then all packets in that file
	// should be parsed as ethernet packets
	linkLayerType := binary.LittleEndian.Uint16(bytes[MAIN_HEADER-LINK_LAYER_TYPE : MAIN_HEADER])
	fmt.Printf("Link Layer Type: 0x%x\n", linkLayerType)

	// go to first packet header length of packet
	cur := MAIN_HEADER + TIME_STAMP_SEC + TIME_STAMP_M_NSEC
	packetsCount := 0

	for cur < len(bytes) {
		packetLength := binary.LittleEndian.Uint16(bytes[cur : cur+LENGTH_CAPTURED])
		untruncatedLength := binary.LittleEndian.Uint16(bytes[cur+LENGTH_CAPTURED : cur+LENGTH_CAPTURED+UNTRUNCATED_LENGTH])
		if packetLength != untruncatedLength {
			panic("packet was truncated")
		}

		// network data is big endian
		startOfPacket := cur + LENGTH_CAPTURED + UNTRUNCATED_LENGTH
		// first 6 bytes is MAC Desitnation
		macDest := bytes[startOfPacket : startOfPacket+6]
		fmt.Printf("MAC destination: %x\n", macDest)

		macSrc := bytes[startOfPacket+6 : startOfPacket+12]
		fmt.Printf("MAC source: %x\n", macSrc)

		// our packet doesn't use 802.1Q tag
		// Ethertype is 2 bytes
		// Then it's payload

		startOfpayload := startOfPacket + 14

		// ip version
		ipVersion := bytes[startOfpayload] & 0b11110000 >> 4
		fmt.Printf("IP Version: %d\n", ipVersion)

		// extract the lowest order 4 bits of the first byte of the ipv4 header
		// get this by logical AND against 15
		// then multiply this number by 4 to get the header length in bytes
		ihl := (bytes[startOfpayload] & 0x0f) << 2
		fmt.Printf("IHL: %x\n", ihl)

		payloadLen := bytes[startOfpayload+2 : startOfpayload+4]
		fmt.Printf("Payload length: %x\n", payloadLen)

		protocolVal := bytes[startOfpayload+9 : startOfpayload+10]
		fmt.Printf("Protocol Value (should be 6 indicating TCP): %x\n", protocolVal)
		if protocolVal[0] != 6 {
			panic("Protocol should be TCP")
		}

		srcIp := bytes[startOfpayload+12 : startOfpayload+16]
		srcIpString := convertIp(srcIp)
		destIp := bytes[startOfpayload+16 : startOfpayload+20]
		destIpString := convertIp(destIp)

		fmt.Printf("Source IP: %s\n", srcIpString)
		fmt.Printf("Destination IP: %s\n", destIpString)

		// start of TCP header after IP options
		// ipHeaderSize := (int(ihl) * 32) / 8
		ipHeaderSize := int(ihl)
		startOfTCPHeader := bytes[startOfpayload+ipHeaderSize]
		srcPort := binary.BigEndian.Uint16(bytes[startOfTCPHeader : startOfTCPHeader+2])
		destPort := binary.BigEndian.Uint16(bytes[startOfTCPHeader+2 : startOfTCPHeader+4])
		fmt.Printf("TCP Source Port: %d\n", srcPort)
		fmt.Printf("TCP Dest Port: %d\n", destPort)

		seqNum := binary.BigEndian.Uint32(bytes[startOfTCPHeader+4 : startOfTCPHeader+8])
		fmt.Printf("Seq Num: %d\n", seqNum)

		// advance to the next packet length field of the next packet header
		cur += LENGTH_CAPTURED + UNTRUNCATED_LENGTH + int(packetLength) + TIME_STAMP_SEC + TIME_STAMP_M_NSEC
		packetsCount++
	}

	fmt.Printf("Number of packets: %d\n", packetsCount)

}
