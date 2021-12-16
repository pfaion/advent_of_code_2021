from pathlib import Path
from math import prod

# load data
packet_hex = Path(__file__).with_name("data.txt").read_text()
packet_bin = f"{int(packet_hex, 16):0>{len(packet_hex)*4}b}"


def pop_front(l: list[str], n: int) -> list[str]:
    return [l.pop(0) for _ in range(n)]


def pop_int(l: list[str], n: int) -> int:
    return int("".join(pop_front(l, n)), 2)


def get_packet_value(packet_bin: list[str]) -> int:
    pop_front(packet_bin, 3)  # just discard version
    type_id = pop_int(packet_bin, 3)

    if type_id == 4:
        # parse literal packet value
        groups = []
        while not groups or groups[-5] != "0":
            groups += pop_front(packet_bin, 5)
        del groups[::5]
        return int("".join(groups), 2)

    else:
        # collect values from sub-packages
        values = []
        type_length_id = pop_int(packet_bin, 1)
        if type_length_id == 0:
            subpacket_length = pop_int(packet_bin, 15)
            target_length = len(packet_bin) - subpacket_length
            while len(packet_bin) != target_length:
                values.append(get_packet_value(packet_bin))
        else:
            n_packets = pop_int(packet_bin, 11)
            for _ in range(n_packets):
                values.append(get_packet_value(packet_bin))

        # apply operator
        match type_id:
            case 0:
                return sum(values)
            case 1:
                return prod(values)
            case 2:
                return min(values)
            case 3:
                return max(values)
            case 5:
                return int(values[0] > values[1])
            case 6:
                return int(values[0] < values[1])
            case 7:
                return int(values[0] == values[1])


print("Solution:", get_packet_value(list(packet_bin)))
