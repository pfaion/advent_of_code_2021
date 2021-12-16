from pathlib import Path

# load data
packet_hex = Path(__file__).with_name("data.txt").read_text()
packet_bin = f"{int(packet_hex, 16):0>{len(packet_hex)*4}b}"


def pop_front(l: list[str], n: int) -> list[str]:
    return [l.pop(0) for _ in range(n)]


def pop_int(l: list[str], n: int) -> int:
    return int("".join(pop_front(l, n)), 2)


def get_packet_version_sum(packet_bin: list[str]) -> int:
    version_sum = pop_int(packet_bin, 3)
    type_id = pop_int(packet_bin, 3)
    if type_id == 4:
        # consume literal packet bits
        while pop_front(packet_bin, 5)[0] != "0":
            continue
    else:
        type_length_id = pop_int(packet_bin, 1)
        if type_length_id == 0:
            subpacket_length = pop_int(packet_bin, 15)
            target_length = len(packet_bin) - subpacket_length
            while len(packet_bin) != target_length:
                version_sum += get_packet_version_sum(packet_bin)
        else:
            n_packets = pop_int(packet_bin, 11)
            for _ in range(n_packets):
                version_sum += get_packet_version_sum(packet_bin)
    return version_sum


print("Solution:", get_packet_version_sum(list(packet_bin)))
