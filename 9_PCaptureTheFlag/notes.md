# The Global pcap-savefile Header

https://www.tcpdump.org/manpages/pcap-savefile.5.txt

- What’s the magic number? What does it tell you about the byte ordering in the pcap-specific aspects of the file?
  - tells you the endianness based off your machine
- What are the major and minor versions? Don’t forget about the byte ordering!
  - I think it's telling you the version of libpcap
- Are the values that ought to be zero in fact zero?
- What is the snapshot length?
  - packets longer than the snapshot length are truncated to the snapshot length
  - if snapshot length = n, only the first n bytes of a packet of length > n will be saved in the capture
- What is the link layer header type?
  - 4 byte number giving the link-layer header type
  - see pcap-linktype(7) for the LINKTYPE\_ values that can appear here
  - https://linux.die.net/man/7/pcap-linktype

+------------------------------+
| Magic number |
+--------------+---------------+
|Major version | Minor version |
+--------------+---------------+
| Time zone offset |
+------------------------------+
| Time stamp accuracy |
+------------------------------+
| Snapshot length |
+------------------------------+
| Link-layer header type |
+------------------------------+
The per-file header length is 24 octets (bytes)

Following the per-file header are zero or more packets which each begin with a header
followed by the raw data.
+----------------------------------------------+
| Time stamp, seconds value |
+----------------------------------------------+
|Time stamp, microseconds or nanoseconds value |
+----------------------------------------------+
| Length of captured packet data |
+----------------------------------------------+
| Un-truncated length of the packet data |
+----------------------------------------------+
The per-packet header length is 16 octets.

# Parsing by hand:

### Header:

```console
00000000: d4c3 b2a1 0200 0400 0000 0000 0000 0000 ................
00000010: ea05 0000 0100 0000
```

Magic Number: is written d4c3b2a1 which means my computer is in the opposite byte order as the host
Therefore, I need to reverse the byte order
Major version: 0200 -> 0002 (reverse the order )-> 2
Minor version: 0400 -> 0004 -> 4

### First packet header:

```console
00000010:... 4098 d057 0a1f 0300  ........@..W....
00000020: 4e00 0000 4e00 0000
```

Size of the first packet:
4e00 0000 --> 0000004e --> 78

truncated:
4e00 0000 --> 0000004e --> 78
Since this number is equal to the size of the packet, no data was truncated
