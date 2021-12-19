input_file = 'inputs/day_3.input'

def bin2dec(bin_list):
    val = 0
    for i, bit in enumerate(bin_list[::-1]):
        val += 2**i * int(bit)
    return val


with open(input_file, 'r') as fp:
    data = fp.read().strip().split('\n')

n = len(data[0])

oxygen_data = [d for d in data]
co2_data = [d for d in data]

def reduce_data(data, n, keep_if_one_most_common):

    for i in range(n):
        if len(data) == 1:
            return bin2dec(data[0])
        classes = {0: [], 1: []}
        for d in data:
            bit = int(d[i])
            classes[bit].append(d)
        if len(classes[1]) >= len(classes[0]):
            data = classes[keep_if_one_most_common]
        else:
            data = classes[1-keep_if_one_most_common]

    if len(data) == 1:
        return bin2dec(data[0])
    else:
        raise RuntimeError("Non unique")

oxygen = reduce_data(oxygen_data, n, 1)
co2 = reduce_data(co2_data, n, 0)

print(oxygen, co2)
print(oxygen * co2)