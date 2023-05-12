package main

import (
	"encoding/binary"
	"fmt"
	"math/rand"
	"strconv"
	"strings"
)

var qtypes = map[string]int{
	"A":     1,
	"NS":    2,
	"CNAME": 5,
	"SOA":   6,
	"MX":    15,
	"TXT":   16,
}

var typeNames = map[uint16]string{
	1:  "A",
	2:  "NS",
	5:  "CNAME",
	6:  "SOA",
	15: "MX",
	16: "TXT",
}

type ResourceRecord struct {
	// rtype is just type in RFC, but type is a restricted word in Go
	rtype, class, rdlength uint16
	ttl                    uint32
	name, rdata            string
}

// https://datatracker.ietf.org/doc/html/rfc1035#section-4.1.1
type DNSMessage struct {
	xid, flags, qdcount, ancount, nscount, arcount uint16
	questions, answers, authority, additional      []ResourceRecord
}

func NewQuery(name, qtype string) *DNSMessage {
	return &DNSMessage{
		xid: uint16(rand.Intn(0xffff)),
		// not sure why flags is 0x100
		flags:   0x100,
		qdcount: 1,
		// class 1 is the internet (see section 3.2.4 in RFC)
		questions: []ResourceRecord{{name: name, rtype: uint16(qtypes[qtype]), class: 1}},
	}
}

func get16(bs []byte, ip *int) uint16 {
	x := binary.BigEndian.Uint16(bs[*ip:])
	*ip += 2
	return x
}

func get32(bs []byte, ip *int) uint32 {
	x := binary.BigEndian.Uint32(bs[*ip:])
	// +4 bytes = +32 bits
	*ip += 4
	return x
}

func put16(bs []byte, ip *int, val uint16) {
	binary.BigEndian.PutUint16(bs[*ip:], val)
	// use a pointer to ip so that each time we call this func we advance
	// the same pointer
	*ip += 2
}

func Serialize(msg *DNSMessage) []byte {
	data := make([]byte, 12)
	i := 0
	ip := &i
	// Serialize the header
	put16(data, ip, msg.xid)
	put16(data, ip, msg.flags)
	put16(data, ip, msg.qdcount)
	put16(data, ip, msg.ancount)
	put16(data, ip, msg.nscount)
	put16(data, ip, msg.arcount)

	// Serialize the question
	for _, q := range msg.questions {
		for _, s := range strings.Split(q.name, ".") {
			data = append(data, byte(len(s)))
			// ... seems to allow something like variadic function; variable number of arguments
			data = append(data, []byte(s)...)
			i += len(s) + 1
		}
		data = append(data, 0x00)
		i += 1
		data = append(data, []byte{0, 0, 0, 0}...)
		put16(data, ip, q.rtype)
		put16(data, ip, q.class)

	}
	return data
}

func Deserialize(data []byte) *DNSMessage {
	// parse header
	i := 0
	ip := &i
	msg := DNSMessage{
		xid:     get16(data, ip),
		flags:   get16(data, ip),
		qdcount: get16(data, ip),
		ancount: get16(data, ip),
		nscount: get16(data, ip),
		arcount: get16(data, ip),
	}

	// Parse questions
	var name string
	// qdcount is 16 bit number specifying the number of entries in the
	// question section
	for qi := uint16(0); qi < msg.qdcount; qi += 1 {
		name, i = ParseName(data, i)
		msg.questions = append(msg.questions, ResourceRecord{
			name:  name,
			rtype: get16(data, ip),
			class: get16(data, ip),
		})
	}

	// parse each resource record for each section
	for ai := uint16(0); ai < msg.ancount; ai += 1 {
		name, i = ParseName(data, i)
		rtype := get16(data, ip)
		rclass := get16(data, ip)
		ttl := get32(data, ip)
		length := get16(data, ip)
		data := ParseRecordData(data, i, rtype, length)
		msg.answers = append(msg.answers, ResourceRecord{
			name: name, rtype: rtype, class: rclass, ttl: ttl, rdlength: length, rdata: data,
		})
	}
	return &msg
}

// See RFC 1035 section 4.1.4 for details
//
// Parse name such as 'ns1.google.com' from a point in a DNS message.
//
// Note that names can be expressed in two forms: a sequence of labels,
// or zero or more labels followed by a pointer to the suffix of an existing
// list of labels. For instance, if "ns1.google.com" has been expressed
// early, then "ns2.google.com" can be encoded as either:
//
//	["ns2", "google", "com"]
//
// or:
//
//	["ns2", <pointer to ["google", "com"]>].
//
// The labels themselves are Pascal strings: the first byte encodes the
// length. Since each label must be 63 octets or less, the first two bits of
// this byte can be used to distinguish between label lengths and pointers.
// If the first two bits are `11`, it is a pointer.
func ParseName(bs []byte, i int) (string, int) {
	labels := []string{}
	for {
		b := int(bs[i])
		if b == 0 {
			break
		}

		// if the first two bits are `11`, then the remaining 14 bits are a pointer
		// 0x3 == 0b11 == 3
		if b>>6 == 0x3 {
			pointer := ((b & 0x3f) << 8) | int(bs[i+1])
			result, _ := ParseName(bs, pointer)
			labels = append(labels, result)
			return strings.Join(labels, "."), i + 2
		}
		labels = append(labels, string(bs[i+1:i+b+1]))
		i += b + 1
	}
	return strings.Join(labels, ","), i + 1 // +1 for null terminator
}

func ParseRecordData(bs []byte, i int, rtype uint16, length uint16) string {
	switch rtype {
	case uint16(1):
		// Show A record as dotted decimal
		parts := make([]string, length)
		for ii, _ := range parts {
			parts[ii] = strconv.Itoa(int(bs[i+ii]))
		}
		return strings.Join(parts, ".")
	case uint16(2):
		// show NS record as name
		name, _ := ParseName(bs, i)
		return name
	default:
		// otherwise just show bytes
		return string(bs[i : i+int(length)])
	}
}

func QueryResponseMatch(q, r *DNSMessage) bool {
	return q.xid == r.xid
}

func (x *ResourceRecord) String() string {
	if x.rdata != "" {
		return fmt.Sprintf("%s\t\t%d\tIN\t%s\t%s", x.name, x.ttl, typeNames[x.rtype], x.rdata)
	}
	return fmt.Sprintf("%s\t\t\tIN\t%s", x.name, typeNames[x.rtype])
}

func join(xs []ResourceRecord) string {
	if len(xs) == 0 {
		return "<empty>"
	}
	parts := make([]string, len(xs))
	for i := 0; i < len(xs); i++ {
		parts[i] = xs[i].String()
	}
	return strings.Join(parts, "\n")
}

func (x *DNSMessage) String() string {
	return fmt.Sprintf(`;; ->>HEADER<<- id: %data
;; flags: %b; QUERY: %d, ANSWER: %d, AUTHORITY: %d, ADDITIONAL: %d

;; QUESTION SECTION:
%s

;; ANSWER SECTION:
%s

;; AUTHORITY SECTION:
%s

;; ADDITIONAL SECTION:
%s
`, x.xid, x.flags, x.qdcount, x.ancount, x.nscount, x.arcount, join(x.questions), join(x.answers), join(x.authority), join(x.additional))

}
