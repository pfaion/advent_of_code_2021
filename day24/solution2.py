from pathlib import Path

instructions = Path(__file__).with_name("data.txt").read_text().splitlines()

batches: list[list[str]] = []
for instr in instructions:
    if instr.startswith("inp"):
        batches.append([])
    batches[-1].append(instr)
n_digits = len(batches)

free_digits = []
digit_dependencies = {}
stack = []
for i, batch in enumerate(batches):
    divisor = int(batch[4].split()[-1])
    A = int(batch[5].split()[-1])
    B = int(batch[15].split()[-1])
    if divisor == 1:
        free_digits.append(i)
        stack.append((i, B))
    else:
        dependant, offset = stack.pop()
        digit_dependencies[dependant] = (i, offset + A)

digits = [0] * n_digits
for free_i in free_digits:
    dep_i, offset = digit_dependencies[free_i]
    for digit_pick in range(1, 10):
        dependent_digit = digit_pick + offset
        if not 0 < dependent_digit <= 9:
            continue
        digits[free_i] = digit_pick
        digits[dep_i] = dependent_digit
        break

min_number = int("".join(str(d) for d in digits))


# def validate(number: Sequence[int]) -> bool:
#     input_stream = iter(number)
#     registers = {r: 0 for r in "xyzw"}

#     for instruction in instructions:
#         operation, *operands = instruction.split()
#         a: str = operands[0]
#         if len(operands) > 1:
#             _b = operands[1]
#             if _b in registers:
#                 b = registers[_b]
#             else:
#                 b = int(_b)

#         match operation:
#             case "inp":
#                 registers[a] = next(input_stream)
#             case "add":
#                 registers[a] += b
#             case "mul":
#                 registers[a] *= b
#             case "div":
#                 registers[a] //= b
#             case "mod":
#                 registers[a] %= b
#             case "eql":
#                 registers[a] = int(registers[a] == b)

#     return registers["z"] == 0

# print(validate(digits))

print("Solution:", min_number)
