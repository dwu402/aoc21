from collections import deque

# input_file = 'test.input'
input_file = 'inputs/day_16.input'

hex2bin = {
    "0": "0000",
    "1": "0001",
    "2": "0010",
    "3": "0011",
    "4": "0100",
    "5": "0101",
    "6": "0110",
    "7": "0111",
    "8": "1000",
    "9": "1001",
    "A": "1010",
    "B": "1011",
    "C": "1100",
    "D": "1101",
    "E": "1110",
    "F": "1111",
}

def read_file():
    with open(input_file, 'r') as fp:
        data = fp.read().strip().split('\n')

    hex_pack = data[0]
    for h in hex_pack:
        yield hex2bin[h]

class Packet():
    def __init__(self):
        self.version = None
        self.type = None
        self.value = None

    def __repr__(self):
        return f"Packet [{self.version}] <{self.type}>"

class Parser():
    def __init__(self, stream):
        self.stream = stream
        self.count = 0
        self.accumulator = []
        self.packets = []

        self._bitstream = deque()

    def stream_bits(self):
        if len(self._bitstream) < 1:
            self._bitstream.extend(next(self.stream))
        self.count += 1
        return int(self._bitstream.popleft())

    def flush(self):
        self._bitstream = deque()

    @staticmethod
    def binlist2int(binlist):
        return sum(2**i*b for i,b in enumerate(reversed(binlist)))

    def parse_version(self, packet):
        v = [self.stream_bits() for _ in range(3)]
        packet.version = self.binlist2int(v)

    def parse_type(self, packet):
        t = [self.stream_bits() for _ in range(3)]
        packet.type = self.binlist2int(t)

    def parse_literal(self, packet):
        go_on = True
        accumulated = []
        while go_on:
            subpack = [self.stream_bits() for _ in range(5)]
            go_on = subpack[0]
            accumulated.extend(subpack[1:5])
        packet.value = self.binlist2int(accumulated)

    def parse_length(self):
        ltype = self.stream_bits()
        if ltype == 0:
            lz = [self.stream_bits() for _ in range(15)]
            lval = self.binlist2int(lz)
        elif ltype == 1:
            lz = [self.stream_bits() for _ in range(11)]
            lval = self.binlist2int(lz)
        return ltype, lval

    def parse_new_packet(self):
        packet = Packet()

        self.parse_version(packet)
        self.parse_type(packet)

        if packet.type == 4: # Literal
            self.parse_literal(packet)
        else: # Operator
            length_type, length_val = self.parse_length()
            packet.value = []
            if length_type == 0:
                c0 = int(self.count)
                while self.count - c0 < length_val:
                    packet.value.append(self.parse_new_packet())
            elif length_type == 1:
                for _ in range(length_val):
                    packet.value.append(self.parse_new_packet())
            

        # self.flush()
        return packet

def sum_versions(packet):
    vsum = packet.version
    if packet.type == 4:
        return vsum
    else:
        for subpacket in packet.value:
            vsum += sum_versions(subpacket)
        return vsum

def resolve_value(packet):
    if packet.type == 0:
        return sum(resolve_value(subpacket) for subpacket in packet.value)
    elif packet.type == 1:
        start = 1
        for subpacket in packet.value:
            start = start * resolve_value(subpacket)
        return start
    elif packet.type == 2:
        return min(resolve_value(subpacket) for subpacket in packet.value)
    elif packet.type == 3:
        return max(resolve_value(subpacket) for subpacket in packet.value)
    elif packet.type == 4:
        return packet.value
    elif packet.type == 5:
        return int(resolve_value(packet.value[0]) > resolve_value(packet.value[1]))
    elif packet.type == 6:
        return int(resolve_value(packet.value[0]) < resolve_value(packet.value[1]))
    elif packet.type == 7:
        return int(resolve_value(packet.value[0]) == resolve_value(packet.value[1]))
    else:
        raise TypeError


def part_a():
    parser = Parser(read_file())
    packet = parser.parse_new_packet()
    return(sum_versions(packet))

def part_b():
    parser = Parser(read_file())
    packet = parser.parse_new_packet()
    return(resolve_value(packet))


if __name__ == "__main__":
    print(part_a())
    print(part_b())